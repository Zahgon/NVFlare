# Copyright (c) 2023, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import threading
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Event, Lock
from typing import Any, Optional

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.app_common.abstract.launcher import Launcher, LauncherRunStatus
from nvflare.app_common.abstract.params_converter import ParamsConverter
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.executors.task_exchanger import TaskExchanger
from nvflare.app_common.utils.fl_model_utils import FLModelUtils
from nvflare.fuel.utils.validation_utils import check_object_type
from nvflare.security.logging import secure_format_exception

LAUNCHER_EXCEPTION = "launcher_exception"


class LauncherExecutor(TaskExchanger):
    def __init__(
        self,
        pipe_id: str,
        launcher_id: Optional[str] = None,
        launch_timeout: Optional[float] = None,
        task_wait_timeout: Optional[float] = None,
        last_result_transfer_timeout: float = 300.0,
        external_pre_init_timeout: float = 60.0,
        peer_read_timeout: Optional[float] = 60.0,
        monitor_interval: float = 0.1,
        read_interval: float = 0.5,
        heartbeat_interval: float = 5.0,
        heartbeat_timeout: float = 60.0,
        workers: int = 4,
        train_with_evaluation: bool = False,
        train_task_name: str = AppConstants.TASK_TRAIN,
        evaluate_task_name: str = AppConstants.TASK_VALIDATION,
        submit_model_task_name: str = AppConstants.TASK_SUBMIT_MODEL,
        from_nvflare_converter_id: Optional[str] = None,
        to_nvflare_converter_id: Optional[str] = None,
    ) -> None:
        """Initializes the LauncherExecutor.

        Args:
            pipe_id (str): Identifier for obtaining the Pipe from NVFlare components.
            launcher_id (Optional[str]): Identifier for obtaining the Launcher from NVFlare components.
            launch_timeout (Optional[float]): Timeout for the Launcher's "launch_task" method to complete (None for no timeout).
            task_wait_timeout (Optional[float]): Timeout for retrieving the task result (None for no timeout).
            last_result_transfer_timeout (float): Timeout for transmitting the last result from an external process.
                This value should be greater than the time needed for sending the whole result.
            external_pre_init_timeout (float): Time to wait for external process before it calls flare.init().
            peer_read_timeout (float, optional): time to wait for peer to accept sent message.
            monitor_interval (float): Interval for monitoring the launcher.
            read_interval (float): Interval for reading from the pipe.
            heartbeat_interval (float): Interval for sending heartbeat to the peer.
            heartbeat_timeout (float): Timeout for waiting for a heartbeat from the peer.
            workers (int): Number of worker threads needed.
            train_with_evaluation (bool): Whether to run training with global model evaluation.
            train_task_name (str): Task name of train mode.
            evaluate_task_name (str): Task name of evaluate mode.
            submit_model_task_name (str): Task name of submit_model mode.
            from_nvflare_converter_id (Optional[str]): Deprecated in LauncherExecutor path.
                Parameter conversion for launcher-based external execution now happens in the subprocess agent.
            to_nvflare_converter_id (Optional[str]): Deprecated in LauncherExecutor path.
                Parameter conversion for launcher-based external execution now happens in the subprocess agent.
        """
        TaskExchanger.__init__(
            self,
            pipe_id=pipe_id,
            read_interval=read_interval,
            heartbeat_interval=heartbeat_interval,
            heartbeat_timeout=heartbeat_timeout,
            peer_read_timeout=peer_read_timeout,
            task_wait_time=task_wait_timeout,
        )
        self.launcher: Optional[Launcher] = None
        self._launcher_id = launcher_id
        self._launch_timeout = launch_timeout

        self._launcher_finish = False
        self._launcher_finish_time = None
        self._last_result_transfer_timeout = last_result_transfer_timeout
        self._external_pre_init_timeout = external_pre_init_timeout
        self._received_result = Event()
        self._job_end = False

        self._thread_pool_executor = ThreadPoolExecutor(max_workers=workers, thread_name_prefix=self.__class__.__name__)

        self._monitor_interval = monitor_interval

        # flags to indicate whether the launcher side will send back trained model and/or metrics
        self._train_with_evaluation = train_with_evaluation
        self._train_task_name = train_task_name
        self._evaluate_task_name = evaluate_task_name
        self._submit_model_task_name = submit_model_task_name

        self._from_nvflare_converter_id = from_nvflare_converter_id
        self._from_nvflare_converter: Optional[ParamsConverter] = None
        self._to_nvflare_converter_id = to_nvflare_converter_id
        self._to_nvflare_converter: Optional[ParamsConverter] = None

        self._monitor_launcher_thread = None
        self._abort_signal = None
        self._current_task = None
        self._lock = Lock()

        # Subclasses can set this to a positive float to defer stop_task() to a
        # background thread, polling for the subprocess to exit naturally first.
        # This is required when the subprocess holds a DownloadService transaction
        # that the server must pull (reverse PASS_THROUGH / large-model upload).
        # Default 0 preserves the original synchronous behaviour.
        self._stop_task_wait_timeout: float = 0.0

        # Coordinates deferred stop_task() with the next round's launch_task().
        # Starts "set" (no deferred stop in progress). Cleared when a deferred stop
        # thread starts; set again (in a finally block) when that thread completes.
        # _initialize_external_execution() waits on this before calling launch_task()
        # so that the launcher's internal _process reference is cleared before a new
        # subprocess is started (prevents "run status becomes success" in round N+1).
        self._deferred_stop_event = threading.Event()
        self._deferred_stop_event.set()
        self._deferred_stop_task_name: str = ""  # task name captured when deferred stop starts

    def initialize(self, fl_ctx: FLContext) -> None:
        pass

    def finalize(self, fl_ctx: FLContext) -> None:
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext) -> None:
        pass

    def execute(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def check_input_shareable(self, task_name: str, shareable: Shareable, fl_ctx: FLContext) -> bool:
        pass

    def check_output_shareable(self, task_name: str, shareable: Shareable, fl_ctx: FLContext) -> bool:
        pass

    def _init_launcher(self, fl_ctx: FLContext):
        pass

    def _init_converter(self, fl_ctx: FLContext):
        pass

    def _initialize_external_execution(
        self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal
    ) -> bool:
        pass

    def _execute_launcher_method_in_thread_executor(self, method_name: str, **kwargs) -> Any:
        pass

    def _wait_external_setup(self, task_name: str, fl_ctx: FLContext, abort_signal: Signal):
        pass

    def _finalize_external_execution(
        self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal
    ) -> bool:
        def _deferred_stop_task():
            pass
        pass

    def _check_result_shareable(self, task_name: str, result) -> str:
        """Checks if exchange should be exited."""
        pass

    def _monitor_launcher(self, fl_ctx: FLContext):
        """Monitors the launcher.

        Trigger the abort signal if "_launcher_finish" is set and "_launcher_finish_time" has passed,
        so TaskExchanger will stop waiting.

        Note:
            If we don't wait extra time after the Launcher finishes, then there is possibility
            that the result is still in transmission, but we will mark it as failed.
            (for example: when using FilePipe, if result has been written out but not read.)
        """
        pass

    def _clear_state(self):
        pass
