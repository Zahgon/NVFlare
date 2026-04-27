# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
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
from typing import Optional

from nvflare.apis.analytix import ANALYTIC_EVENT_TYPE
from nvflare.apis.event_type import EventType
from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import FLContextKey, FLMetaKey, ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.apis.utils.analytix_utils import create_analytic_dxo, send_analytic_dxo
from nvflare.apis.workspace import Workspace
from nvflare.app_common.abstract.params_converter import ParamsConverter
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.executors.task_script_runner import TaskScriptRunner
from nvflare.client.api_spec import CLIENT_API_KEY
from nvflare.client.config import ConfigKey, ExchangeFormat, TransferType
from nvflare.client.in_process.api import (
    TOPIC_ABORT,
    TOPIC_GLOBAL_RESULT,
    TOPIC_LOCAL_RESULT,
    TOPIC_LOG_DATA,
    TOPIC_STOP,
    InProcessClientAPI,
)
from nvflare.fuel.data_event.data_bus import DataBus
from nvflare.fuel.data_event.event_manager import EventManager
from nvflare.fuel.utils.validation_utils import check_object_type
from nvflare.security.logging import secure_format_traceback


class InProcessClientAPIExecutor(Executor):
    def __init__(
        self,
        task_script_path: str,
        task_script_args: str = "",
        task_wait_time: Optional[float] = None,
        result_pull_interval: float = 0.5,
        log_pull_interval: Optional[float] = None,
        params_exchange_format: str = ExchangeFormat.NUMPY,
        params_transfer_type: TransferType = TransferType.FULL,
        from_nvflare_converter_id: Optional[str] = None,
        to_nvflare_converter_id: Optional[str] = None,
        train_with_evaluation: bool = False,
        train_task_name: str = AppConstants.TASK_TRAIN,
        evaluate_task_name: str = AppConstants.TASK_VALIDATION,
        submit_model_task_name: str = AppConstants.TASK_SUBMIT_MODEL,
        server_expected_format: str = ExchangeFormat.NUMPY,
        memory_gc_rounds: int = 0,
        cuda_empty_cache: bool = False,
    ):
        super(InProcessClientAPIExecutor, self).__init__()
        self._memory_gc_rounds = memory_gc_rounds
        self._cuda_empty_cache = cuda_empty_cache
        self._abort = False
        self._client_api = None
        self._result_pull_interval = result_pull_interval
        self._log_pull_interval = log_pull_interval
        self._params_exchange_format = params_exchange_format
        self._server_expected_format = server_expected_format
        self._params_transfer_type = params_transfer_type

        if not task_script_path or not task_script_path.endswith(".py"):
            raise ValueError(f"invalid task_script_path '{task_script_path}'")

        # only support main() for backward compatibility
        self._task_script_path = task_script_path
        self._task_script_args = task_script_args
        self._task_wait_time = task_wait_time

        # flags to indicate whether the launcher side will send back trained model and/or metrics
        self._train_with_evaluation = train_with_evaluation
        self._train_task_name = train_task_name
        self._evaluate_task_name = evaluate_task_name
        self._submit_model_task_name = submit_model_task_name

        self._from_nvflare_converter_id = from_nvflare_converter_id
        self._from_nvflare_converter: Optional[ParamsConverter] = None
        self._to_nvflare_converter_id = to_nvflare_converter_id
        self._to_nvflare_converter: Optional[ParamsConverter] = None

        self._engine = None
        self._task_fn_thread = None
        self._log_thread = None
        self._data_bus = DataBus()
        self._event_manager = EventManager(self._data_bus)
        self._data_bus.subscribe([TOPIC_LOCAL_RESULT], self.local_result_callback)
        self._data_bus.subscribe([TOPIC_LOG_DATA], self.log_result_callback)
        self._data_bus.subscribe([TOPIC_ABORT, TOPIC_STOP], self.to_abort_callback)
        self.local_result = None
        self._fl_ctx = None
        self._task_fn_path = None
        self._task_fn_wrapper = None

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def execute(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def _prepare_task_meta(self, fl_ctx, task_name):
        pass

    def send_data_to_peer(self, shareable, fl_ctx: FLContext):
        pass

    def _init_converter(self, fl_ctx: FLContext):
        pass

    def check_output_shareable(self, task_name: str, shareable, fl_ctx: FLContext):
        """Checks output shareable after execute."""
        pass

    def local_result_callback(self, topic, data, databus):
        pass

    def log_result_callback(self, topic, data, databus):
        pass

    def to_abort_callback(self, topic, data, databus):
        pass
