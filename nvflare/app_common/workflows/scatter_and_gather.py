# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
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

from nvflare.apis.client import Client
from nvflare.apis.controller_spec import ClientTask, OperatorMethod, Task, TaskOperatorKey
from nvflare.apis.fl_constant import ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.impl.controller import Controller
from nvflare.apis.shareable import Shareable
from nvflare.apis.signal import Signal
from nvflare.app_common.abstract.aggregator import Aggregator
from nvflare.app_common.abstract.learnable_persistor import LearnablePersistor
from nvflare.app_common.abstract.model import ModelLearnable, make_model_learnable
from nvflare.app_common.abstract.shareable_generator import ShareableGenerator
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.app_event_type import AppEventType
from nvflare.app_common.utils.error_handling_utils import get_error_handling_message, should_ignore_result_error
from nvflare.fuel.utils.memory_utils import cleanup_memory
from nvflare.fuel.utils.validation_utils import check_non_negative_int
from nvflare.security.logging import secure_format_exception
from nvflare.widgets.info_collector import GroupInfoCollector, InfoCollector


class ScatterAndGather(Controller):
    def __init__(
        self,
        min_clients: int = 1000,
        num_rounds: int = 5,
        start_round: int = 0,
        wait_time_after_min_received: int = 10,
        aggregator_id=AppConstants.DEFAULT_AGGREGATOR_ID,
        persistor_id="",
        shareable_generator_id=AppConstants.DEFAULT_SHAREABLE_GENERATOR_ID,
        train_task_name=AppConstants.TASK_TRAIN,
        train_timeout: int = 0,
        ignore_result_error: bool = None,
        allow_empty_global_weights: bool = False,
        task_check_period: float = 0.5,
        persist_every_n_rounds: int = 1,
        snapshot_every_n_rounds: int = 1,
        memory_gc_rounds: int = 1,
    ):
        """The controller for ScatterAndGather Workflow.

        The ScatterAndGather workflow defines FederatedAveraging on all clients.
        The model persistor (persistor_id) is used to load the initial global model which is sent to all clients.
        Each client sends it's updated weights after local training which is aggregated (aggregator_id). The
        shareable generator is used to convert the aggregated weights to shareable and shareable back to weight.
        The model_persistor also saves the model after training.

        Args:
            min_clients (int, optional): The minimum number of clients responses before
                SAG starts to wait for `wait_time_after_min_received`. Note that SAG will move forward when all
                available clients have responded regardless of this value. Defaults to 1000.
            num_rounds (int, optional): The total number of training rounds. Defaults to 5.
            start_round (int, optional): Start round for training. Defaults to 0.
            wait_time_after_min_received (int, optional): Time to wait before beginning aggregation after
                minimum number of clients responses has been received. Defaults to 10.
            aggregator_id (str, optional): ID of the aggregator component. Defaults to "aggregator".
            persistor_id (str, optional): ID of the persistor component. Defaults to "".
            shareable_generator_id (str, optional): ID of the shareable generator. Defaults to "shareable_generator".
            train_task_name (str, optional): Name of the train task. Defaults to "train".
            train_timeout (int, optional): Time to wait for clients to do local training.
            ignore_result_error (bool or None, optional): How to handle client result errors.
                - None: Dynamic mode (default) - ignore errors if min_clients still reachable, panic otherwise.
                - False: Strict mode - panic on any client error.
                - True: Resilient mode - always ignore client errors.
            allow_empty_global_weights (bool, optional): whether to allow empty global weights. Some pipelines can have
                empty global weights at first round, such that clients start training from scratch without any global info.
                Defaults to False.
            task_check_period (float, optional): interval for checking status of tasks. Defaults to 0.5.
            persist_every_n_rounds (int, optional): persist the global model every n rounds. Defaults to 1.
                If n is 0 then no persist.
            snapshot_every_n_rounds (int, optional): persist the server state every n rounds. Defaults to 1.
                If n is 0 then no persist.
            memory_gc_rounds (int, optional): Run memory cleanup (gc.collect + malloc_trim) every N rounds.
                Set to 0 to disable. Defaults to 1 (every round).

        Raises:
            TypeError: when any of input arguments does not have correct type
            ValueError: when any of input arguments is out of range
        """
        super().__init__(task_check_period=task_check_period)

        # Check arguments
        if not isinstance(min_clients, int):
            raise TypeError("min_clients must be int but got {}".format(type(min_clients)))
        elif min_clients <= 0:
            raise ValueError("min_clients must be greater than 0.")

        check_non_negative_int("num_rounds", num_rounds)
        check_non_negative_int("start_round", start_round)
        check_non_negative_int("wait_time_after_min_received", wait_time_after_min_received)
        check_non_negative_int("train_timeout", train_timeout)
        check_non_negative_int("persist_every_n_rounds", persist_every_n_rounds)
        check_non_negative_int("snapshot_every_n_rounds", snapshot_every_n_rounds)
        check_non_negative_int("memory_gc_rounds", memory_gc_rounds)

        if not isinstance(aggregator_id, str):
            raise TypeError("aggregator_id must be a string but got {}".format(type(aggregator_id)))
        if not isinstance(persistor_id, str):
            raise TypeError("persistor_id must be a string but got {}".format(type(persistor_id)))
        if not isinstance(shareable_generator_id, str):
            raise TypeError("shareable_generator_id must be a string but got {}".format(type(shareable_generator_id)))
        if not isinstance(train_task_name, str):
            raise TypeError("train_task_name must be a string but got {}".format(type(train_task_name)))

        if not isinstance(task_check_period, (int, float)):
            raise TypeError(f"task_check_period must be an int or float but got {type(task_check_period)}")
        elif task_check_period <= 0:
            raise ValueError("task_check_period must be greater than 0.")

        self.aggregator_id = aggregator_id
        self.persistor_id = persistor_id
        self.shareable_generator_id = shareable_generator_id
        self.train_task_name = train_task_name
        self.aggregator = None
        self.persistor = None
        self.shareable_gen = None

        # config data
        self._min_clients = min_clients
        self._num_rounds = num_rounds
        self._wait_time_after_min_received = wait_time_after_min_received
        self._start_round = start_round
        self._train_timeout = train_timeout
        self._persist_every_n_rounds = persist_every_n_rounds
        self._snapshot_every_n_rounds = snapshot_every_n_rounds
        self._memory_gc_rounds = memory_gc_rounds
        self.ignore_result_error = ignore_result_error
        self.allow_empty_global_weights = allow_empty_global_weights

        # workflow phases: init, train, validate
        self._phase = AppConstants.PHASE_INIT
        self._global_weights = make_model_learnable({}, {})
        self._current_round = None

        # Track failed clients for dynamic ignore_result_error mode
        self._current_failed_clients = set()
        self._current_num_targets = 0

    def _maybe_cleanup_memory(self):
        """Perform memory cleanup if configured (every N rounds based on memory_gc_rounds)."""
        pass

    def start_controller(self, fl_ctx: FLContext) -> None:
        pass

    def control_flow(self, abort_signal: Signal, fl_ctx: FLContext) -> None:
        pass

    def stop_controller(self, fl_ctx: FLContext):
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def _prepare_train_task_data(self, client_task: ClientTask, fl_ctx: FLContext) -> None:
        pass

    def _process_train_result(self, client_task: ClientTask, fl_ctx: FLContext) -> None:
        pass

    def process_result_of_unknown_task(
        self, client: Client, task_name, client_task_id, result: Shareable, fl_ctx: FLContext
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

    def _check_abort_signal(self, fl_ctx, abort_signal: Signal):
        pass

    def get_persist_state(self, fl_ctx: FLContext) -> dict:
        pass

    def restore(self, state_data: dict, fl_ctx: FLContext):
        pass
