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

import random
from abc import ABC, abstractmethod
from typing import Callable, List, Optional, Union

from nvflare.apis.client import Client
from nvflare.apis.controller_spec import ClientTask, OperatorMethod, Task, TaskOperatorKey
from nvflare.apis.fl_constant import ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.impl.controller import Controller
from nvflare.apis.shareable import Shareable
from nvflare.apis.signal import Signal
from nvflare.app_common.abstract.fl_model import FLModel, ParamsType
from nvflare.app_common.abstract.learnable_persistor import LearnablePersistor
from nvflare.app_common.abstract.model import ModelLearnable, ModelLearnableKey, make_model_learnable
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.app_event_type import AppEventType
from nvflare.app_common.utils.error_handling_utils import get_error_handling_message, should_ignore_result_error
from nvflare.app_common.utils.fl_component_wrapper import FLComponentWrapper
from nvflare.app_common.utils.fl_model_utils import FLModelUtils
from nvflare.fuel.utils.validation_utils import check_non_negative_int, check_positive_int, check_str
from nvflare.security.logging import secure_format_exception


class BaseModelController(Controller, FLComponentWrapper, ABC):
    def __init__(
        self,
        persistor_id: str = AppConstants.DEFAULT_PERSISTOR_ID,
        ignore_result_error: Optional[bool] = None,
        allow_empty_global_weights: bool = False,
        task_check_period: float = 0.5,
    ):
        """FLModel based controller.

        Args:
            persistor_id (str, optional): ID of the persistor component. Defaults to AppConstants.DEFAULT_PERSISTOR_ID ("persistor").
            ignore_result_error (bool or None, optional): How to handle client result errors.
                - None: Dynamic mode (default) - ignore errors if min_responses still reachable, panic otherwise.
                - False: Strict mode - panic on any client error.
                - True: Resilient mode - always ignore client errors.
            allow_empty_global_weights (bool, optional): whether to allow empty global weights. Some pipelines can have
                empty global weights at first round, such that clients start training from scratch without any global info.
                Defaults to False.
            task_check_period (float, optional): interval for checking status of tasks. Defaults to 0.5.
        """
        super().__init__(task_check_period=task_check_period)

        # Check arguments
        check_str("persistor_id", persistor_id)
        if not isinstance(task_check_period, (int, float)):
            raise TypeError(f"task_check_period must be an int or float but got {type(task_check_period)}")
        elif task_check_period <= 0:
            raise ValueError("task_check_period must be greater than 0.")
        self._task_check_period = task_check_period
        self._persistor_id = persistor_id
        self.persistor = None

        # config data
        self._ignore_result_error = ignore_result_error
        self._allow_empty_global_weights = allow_empty_global_weights

        # model related
        self._results = []

        # Task context for dynamic ignore_result_error mode (when ignore_result_error=None).
        # These are reset per send_model() call to track error tolerance for the current task.
        self._current_min_responses = 0  # Minimum successful responses needed for this task
        self._current_num_targets = 0  # Total number of clients targeted for this task
        self._current_failed_clients = set()  # Set of client names that returned errors in this task

    def start_controller(self, fl_ctx: FLContext) -> None:
        pass

    def _build_shareable(self, data: FLModel = None) -> Shareable:
        pass

    def broadcast_model(
        self,
        data,
        task_name: str = AppConstants.TASK_TRAIN,
        targets: Union[List[Client], List[str], None] = None,
        min_responses: int = None,
        timeout: int = 0,
        wait_time_after_min_received: int = 0,
        blocking: bool = True,
        callback: Callable[[FLModel], None] = None,
    ) -> List:
        """Send a task with data to a list of targets.

        Args:
            data: FLModel to be sent to clients. It must be a FLModel object. It will raise an exception if None.
            task_name (str, optional): name of the task. Defaults to "train".
            targets (List[str], optional): the list of target client names or None (all clients). Defaults to None.
            min_responses (int, optional): the minimum number of responses expected. If None, must receive responses from
              all clients that the task has been sent to. Defaults to None.
            timeout (int, optional): time to wait for clients to perform task. Defaults to 0, i.e., never time out.
            wait_time_after_min_received (int, optional): time to wait after
                minimum number of clients responses has been received. Defaults to 0.
            blocking (bool, optional): whether to block to wait for task result. Defaults to True.
            callback (Callable[[FLModel], None], optional): callback when a result is received, only called when blocking=False. Defaults to None.

        Returns:
            List[FLModel] if blocking=True else None
        """
        pass

    def _prepare_task(
        self,
        data: FLModel,
        task_name: str,
        timeout: int,
        callback: Callable,
    ):
        # Create task
        pass

    def _prepare_task_data(self, client_task: ClientTask, fl_ctx: FLContext) -> None:
        pass

    @staticmethod
    def _set_ctx_prop_preserving_attrs(
        fl_ctx: FLContext, key: str, value, default_private: bool = True, default_sticky: bool = False
    ) -> None:
        pass

    def _process_result(self, client_task: ClientTask, fl_ctx: FLContext) -> None:
        pass
        # Note: Memory cleanup (gc.collect + malloc_trim) is handled by subclasses
        # via _maybe_cleanup_memory() based on memory_gc_rounds setting

    def process_result_of_unknown_task(
        self, client: Client, task_name: str, client_task_id: str, result: Shareable, fl_ctx: FLContext
    ) -> None:
        pass

    def _accept_train_result(
        self, client_name: str, result: Shareable, fl_ctx: FLContext, is_unknown_task: bool = False
    ) -> bool:
        """Accept or reject a training result based on error handling policy.

        Args:
            client_name: Name of the client that sent the result.
            result: The Shareable result from the client.
            fl_ctx: The FLContext.
            is_unknown_task: Whether this result is from an unknown/late task.

        Returns:
            True if the result was accepted, False if it was rejected (error ignored or panic triggered).
        """
        pass

    @abstractmethod
    def run(self):
        """Main `run` routine called by the Controller's `control_flow` to execute the workflow.

        Returns: None.

        """
        pass

    def control_flow(self, abort_signal: Signal, fl_ctx: FLContext) -> None:
        pass

    def load_model(self):
        # initialize global model
        pass

    def get_run_dir(self):
        """Get current run directory."""
        pass

    def get_app_dir(self):
        """Get current app directory."""
        pass

    def save_model(self, model):
        pass

    def sample_clients(self, num_clients: int = None) -> List[str]:
        pass

    def set_fl_context(self, data: FLModel):
        """Set fl_ctx CURRENT_ROUND and NUM_ROUNDS from FLModel so they stay current each round.

        Uses existing (private, sticky) attributes when the prop is already set so set_prop()
        accepts the update without warning; otherwise uses private=True, sticky=False. Required
        for flows like FedAvg that do not set CURRENT_ROUND in fl_ctx before send; downstream
        (e.g. aggregators) rely on it.
        """
        pass

    def get_component(self, component_id: str):
        pass

    def build_component(self, config_dict: dict):
        pass

    def stop_controller(self, fl_ctx: FLContext):
        pass
