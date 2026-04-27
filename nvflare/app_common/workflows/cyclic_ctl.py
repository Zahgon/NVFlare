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

import random
from typing import List, Union

from nvflare.apis.client import Client
from nvflare.apis.controller_spec import ClientTask, Task
from nvflare.apis.fl_constant import ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.impl.controller import Controller
from nvflare.apis.shareable import Shareable
from nvflare.apis.signal import Signal
from nvflare.app_common.abstract.learnable_persistor import LearnablePersistor
from nvflare.app_common.abstract.shareable_generator import ShareableGenerator
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.app_event_type import AppEventType
from nvflare.fuel.utils.memory_utils import cleanup_memory
from nvflare.fuel.utils.validation_utils import check_non_negative_int
from nvflare.security.logging import secure_format_exception


class RelayOrder:
    FIXED = "FIXED"
    RANDOM = "RANDOM"
    RANDOM_WITHOUT_SAME_IN_A_ROW = "RANDOM_WITHOUT_SAME_IN_A_ROW"


SUPPORTED_ORDERS = (RelayOrder.FIXED, RelayOrder.RANDOM, RelayOrder.RANDOM_WITHOUT_SAME_IN_A_ROW)


class CyclicController(Controller):
    def __init__(
        self,
        num_rounds: int = 5,
        task_assignment_timeout: int = 10,
        persistor_id="persistor",
        shareable_generator_id="shareable_generator",
        task_name="train",
        task_check_period: float = 0.5,
        persist_every_n_rounds: int = 1,
        snapshot_every_n_rounds: int = 1,
        order: Union[str, List[str]] = RelayOrder.FIXED,
        allow_early_termination=False,
        memory_gc_rounds: int = 1,
    ):
        """A sample implementation to demonstrate how to use relay method for Cyclic Federated Learning.

        Args:
            num_rounds (int, optional): number of rounds this controller should perform. Defaults to 5.
            task_assignment_timeout (int, optional): timeout (in sec) to determine if one client fails to
                request the task which it is assigned to . Defaults to 10.
            persistor_id (str, optional): id of the persistor so this controller can save a global model.
                Defaults to "persistor".
            shareable_generator_id (str, optional): id of shareable generator. Defaults to "shareable_generator".
            task_name (str, optional): the task name that clients know how to handle. Defaults to "train".
            task_check_period (float, optional): interval for checking status of tasks. Defaults to 0.5.
            persist_every_n_rounds (int, optional): persist the global model every n rounds. Defaults to 1.
                If n is 0 then no persist.
            snapshot_every_n_rounds (int, optional): persist the server state every n rounds. Defaults to 1.
                If n is 0 then no persist.
            order (Union[str, List[str]], optional): The order of relay.

                - If a string is provided:

                    - "FIXED": Same order for every round.
                    - "RANDOM": Random order for every round.
                    - "RANDOM_WITHOUT_SAME_IN_A_ROW": Shuffled order, no repetition in consecutive rounds.

                - If a list of strings is provided, it represents a custom order for relay.

            allow_early_termination: whether to allow early workflow termination from clients
            memory_gc_rounds (int, optional): Run memory cleanup (gc.collect + malloc_trim) every N rounds.
                Set to 0 to disable. Defaults to 1 (every round).

        Raises:
            TypeError: when any of input arguments does not have correct type

        """
        super().__init__(task_check_period=task_check_period)

        if not isinstance(num_rounds, int):
            raise TypeError("num_rounds must be int but got {}".format(type(num_rounds)))
        if not isinstance(task_assignment_timeout, int):
            raise TypeError("task_assignment_timeout must be int but got {}".format(type(task_assignment_timeout)))
        if not isinstance(persistor_id, str):
            raise TypeError("persistor_id must be a string but got {}".format(type(persistor_id)))
        if not isinstance(shareable_generator_id, str):
            raise TypeError("shareable_generator_id must be a string but got {}".format(type(shareable_generator_id)))
        if not isinstance(task_name, str):
            raise TypeError("task_name must be a string but got {}".format(type(task_name)))

        if order not in SUPPORTED_ORDERS and not isinstance(order, list):
            raise ValueError(f"order must be in {SUPPORTED_ORDERS} or a list")

        self._num_rounds = num_rounds
        self._start_round = 0
        self._end_round = self._start_round + self._num_rounds
        self._current_round = 0
        self._is_done = False
        self._last_learnable = None
        self.persistor_id = persistor_id
        self.shareable_generator_id = shareable_generator_id
        self.task_assignment_timeout = task_assignment_timeout
        self.task_name = task_name
        self.persistor = None
        self.shareable_generator = None
        self._persist_every_n_rounds = persist_every_n_rounds
        self._snapshot_every_n_rounds = snapshot_every_n_rounds
        check_non_negative_int("memory_gc_rounds", memory_gc_rounds)
        self._memory_gc_rounds = memory_gc_rounds
        self._participating_clients = None
        self._last_client = None
        self._order = order
        self._allow_early_termination = allow_early_termination

    def _maybe_cleanup_memory(self):
        """Perform memory cleanup if configured (every N rounds based on memory_gc_rounds)."""
        pass

    def start_controller(self, fl_ctx: FLContext):
        pass

    def _get_relay_orders(self, fl_ctx: FLContext) -> Union[List[Client], None]:
        pass

    def _stop_workflow(self, task: Task):
        pass

    def _process_result(self, client_task: ClientTask, fl_ctx: FLContext):
        # submitted shareable is stored in client_task.result
        # we need to update task.data with that shareable so the next target
        # will get the updated shareable
        pass

    def control_flow(self, abort_signal: Signal, fl_ctx: FLContext):
        pass

    def stop_controller(self, fl_ctx: FLContext):
        pass

    def process_result_of_unknown_task(
        self,
        client: Client,
        task_name: str,
        client_task_id: str,
        result: Shareable,
        fl_ctx: FLContext,
    ):
        pass

    def get_persist_state(self, fl_ctx: FLContext) -> dict:
        pass

    def restore(self, state_data: dict, fl_ctx: FLContext):
        pass
