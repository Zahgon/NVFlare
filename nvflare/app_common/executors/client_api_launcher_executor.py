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

import logging
import os
from typing import Optional

from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.executors.launcher_executor import LauncherExecutor
from nvflare.app_common.utils.export_utils import update_export_props
from nvflare.client.config import ConfigKey, ExchangeFormat, TransferType, write_config_to_file
from nvflare.client.constants import CLIENT_API_CONFIG, EXTERNAL_PRE_INIT_TIMEOUT, PEER_READ_TIMEOUT
from nvflare.fuel.utils.attributes_exportable import ExportMode
from nvflare.fuel.utils.fobs.decomposers.via_downloader import MIN_DOWNLOAD_TIMEOUT_DEFAULT
from nvflare.utils.configs import get_client_config_value

logger = logging.getLogger(__name__)


class ClientAPILauncherExecutor(LauncherExecutor):
    def __init__(
        self,
        pipe_id: str,
        launcher_id: Optional[str] = None,
        launch_timeout: Optional[float] = None,
        task_wait_timeout: Optional[float] = None,
        last_result_transfer_timeout: float = 300.0,
        external_pre_init_timeout: float = 300.0,
        peer_read_timeout: Optional[float] = 300.0,
        monitor_interval: float = 0.01,
        read_interval: float = 0.5,
        heartbeat_interval: float = 5.0,
        heartbeat_timeout: float = 300.0,
        workers: int = 4,
        train_with_evaluation: bool = False,
        train_task_name: str = AppConstants.TASK_TRAIN,
        evaluate_task_name: str = AppConstants.TASK_VALIDATION,
        submit_model_task_name: str = AppConstants.TASK_SUBMIT_MODEL,
        from_nvflare_converter_id: Optional[str] = None,
        to_nvflare_converter_id: Optional[str] = None,
        params_exchange_format: str = ExchangeFormat.NUMPY,
        params_transfer_type: str = TransferType.FULL,
        config_file_name: str = CLIENT_API_CONFIG,
        server_expected_format: str = ExchangeFormat.NUMPY,
        memory_gc_rounds: int = 0,
        cuda_empty_cache: bool = False,
        submit_result_timeout: float = 300.0,
        max_resends: int = 3,
        download_complete_timeout: float = 1800.0,
    ) -> None:
        """Initializes the ClientAPILauncherExecutor.

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
            from_nvflare_converter_id (Optional[str]): Identifier used to get the ParamsConverter from NVFlare components.
                This ParamsConverter will be called when model is sent from nvflare controller side to executor side.
            to_nvflare_converter_id (Optional[str]): Identifier used to get the ParamsConverter from NVFlare components.
                This ParamsConverter will be called when model is sent from nvflare executor side to controller side.
            server_expected_format (str): What format to exchange the parameters between server and client.
            params_exchange_format (str): What format to exchange the parameters between client and script.
            params_transfer_type (str): How to transfer the parameters. FULL means the whole model parameters are sent.
                DIFF means that only the difference is sent.
            config_file_name (str): The config file name to write attributes into, the client api will read in this file.
            submit_result_timeout (float): How long (seconds) the subprocess waits for CJ to acknowledge each result
                pipe message.  With reverse PASS_THROUGH enabled CJ ACKs immediately (LazyDownloadRef creation is
                microseconds), so 300 s is a very generous allowance.  Without reverse PASS_THROUGH, CJ must
                download the full result before ACKing; in that case this should be at least as large as the
                expected transfer time.  Configurable via recipe.add_client_config({"submit_result_timeout": N}).
            max_resends (int): Maximum number of times the subprocess retries sending the result if CJ does not
                ACK within submit_result_timeout.  Defaults to 3.  None means unlimited (unsafe for large models
                — each retry creates a new download transaction).  Configurable via
                recipe.add_client_config({"max_resends": N}).
            download_complete_timeout (float): How long (seconds) the subprocess waits after send_to_peer() ACKs
                for the server to finish downloading its tensors from the subprocess DownloadService.  Without
                this gate, the subprocess may exit before the download completes and the server gets
                "no ref found".  Defaults to 1800 s.  Configurable via
                recipe.add_client_config({"download_complete_timeout": N}).
        """
        LauncherExecutor.__init__(
            self,
            pipe_id=pipe_id,
            launcher_id=launcher_id,
            launch_timeout=launch_timeout,
            task_wait_timeout=task_wait_timeout,
            last_result_transfer_timeout=last_result_transfer_timeout,
            external_pre_init_timeout=external_pre_init_timeout,
            peer_read_timeout=peer_read_timeout,
            monitor_interval=monitor_interval,
            read_interval=read_interval,
            heartbeat_interval=heartbeat_interval,
            heartbeat_timeout=heartbeat_timeout,
            workers=workers,
            train_with_evaluation=train_with_evaluation,
            train_task_name=train_task_name,
            evaluate_task_name=evaluate_task_name,
            submit_model_task_name=submit_model_task_name,
            from_nvflare_converter_id=from_nvflare_converter_id,
            to_nvflare_converter_id=to_nvflare_converter_id,
        )

        self._server_expected_format = server_expected_format
        self._params_exchange_format = params_exchange_format
        self._params_transfer_type = params_transfer_type
        self._config_file_name = config_file_name
        self._memory_gc_rounds = memory_gc_rounds
        self._cuda_empty_cache = cuda_empty_cache
        self._submit_result_timeout = submit_result_timeout
        self._max_resends = max_resends
        self._download_complete_timeout = download_complete_timeout
        self._cj_round_count = 0

        # Allow the subprocess to exit naturally after Fix 16's download_done.wait()
        # before stop_task() sends SIGTERM.  Without this, _finalize_external_execution()
        # kills the subprocess immediately, tearing down its cell connection before the
        # server can download tensors from it ("no path" / deadlock).
        self._stop_task_wait_timeout = download_complete_timeout
        self._cell_with_pass_through = None  # track cell so finalize() can clean up
        self._pass_through_channel = None  # channel name registered in decode_pass_through_channels

    def finalize(self, fl_ctx: FLContext) -> None:
        pass

    def initialize(self, fl_ctx: FLContext) -> None:
        pass

    def _decomposer_prefix(self) -> str:
        """Return the config-var prefix for the active decomposer type.

        The prefix must match what the ViaDownloaderDecomposer subclass uses
        (e.g. NumpyArrayDecomposer → "np_") so that _validate_timeout_config()
        reads the same job-config keys as the download infrastructure.

        Framework-specific subclasses (e.g. PTClientAPILauncherExecutor) should
        override this method to return their decomposer's prefix (e.g. "tensor_"),
        keeping this base class free of framework-specific knowledge.
        """
        pass

    def _validate_timeout_config(self, fl_ctx: FLContext):
        """Warn at job start if timeout parameters are inconsistent.

        Checks are advisory (log_warning, not raise) so a misconfigured job
        can still run — the messages give the operator actionable guidance
        before the first download attempt.
        """
        pass

    def check_output_shareable(self, task_name: str, shareable: Shareable, fl_ctx: FLContext) -> bool:
        pass

    def _maybe_cleanup_cj_memory(self, fl_ctx: FLContext):
        """Call cleanup_memory() every memory_gc_rounds rounds on the client job process.

        Mirrors the subprocess-side cleanup in APISpec._maybe_cleanup_memory().
        Runs at the point the client job process has finished relaying the
        subprocess result to the server — the result Shareable and any tensors
        it referenced are no longer needed, making this the right moment to
        force a GC cycle.
        """
        pass

    def _resolve_launch_once(self, fl_ctx: FLContext) -> bool:
        """Return True if the subprocess is launched once for the whole job.

        self.launcher may be None when prepare_config_for_launch() is called during
        initialize() (before _initialize_external_execution() assigns it), so we
        fetch the launcher component directly from the engine.
        """
        pass

    def prepare_config_for_launch(self, fl_ctx: FLContext):
        pass

    def _get_external_config_file_path(self, fl_ctx: FLContext):
        pass
