# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
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

import copy
import gc

import numpy as np

from nvflare.apis.dxo import DXO, DataKind, from_shareable
from nvflare.apis.fl_context import FLContext
from nvflare.apis.impl.controller import Task
from nvflare.apis.signal import Signal
from nvflare.app_common.abstract.model import model_learnable_to_dxo
from nvflare.app_common.app_constant import AlgorithmConstants, AppConstants
from nvflare.app_common.app_event_type import AppEventType
from nvflare.app_common.workflows.scatter_and_gather import ScatterAndGather
from nvflare.security.logging import secure_format_exception


class ScatterAndGatherScaffold(ScatterAndGather):
    def __init__(
        self,
        min_clients: int = 1000,
        num_rounds: int = 5,
        start_round: int = 0,
        wait_time_after_min_received: int = 10,
        aggregator_id=AppConstants.DEFAULT_AGGREGATOR_ID,
        persistor_id=AppConstants.DEFAULT_PERSISTOR_ID,
        shareable_generator_id=AppConstants.DEFAULT_SHAREABLE_GENERATOR_ID,
        train_task_name=AppConstants.TASK_TRAIN,
        train_timeout: int = 0,
        ignore_result_error: bool = None,
        task_check_period: float = 0.5,
        persist_every_n_rounds: int = 1,
        snapshot_every_n_rounds: int = 1,
    ):
        """The controller for ScatterAndGatherScaffold workflow.

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
            persistor_id (str, optional): ID of the persistor component. Defaults to "persistor".
            shareable_generator_id (str, optional): ID of the shareable generator. Defaults to "shareable_generator".
            train_task_name (str, optional): Name of the train task. Defaults to "train".
            train_timeout (int, optional): Time to wait for clients to do local training.
            ignore_result_error (bool or None, optional): How to handle client result errors.
                - None: Dynamic mode (default) - ignore errors if min_clients still reachable, panic otherwise.
                - False: Strict mode - panic on any client error.
                - True: Resilient mode - always ignore client errors.
            task_check_period (float, optional): interval for checking status of tasks. Defaults to 0.5.
            persist_every_n_rounds (int, optional): persist the global model every n rounds. Defaults to 1.
                If n is 0 then no persist.
            snapshot_every_n_rounds (int, optional): persist the server state every n rounds. Defaults to 1.
                If n is 0 then no persist.
        """

        super().__init__(
            min_clients=min_clients,
            num_rounds=num_rounds,
            start_round=start_round,
            wait_time_after_min_received=wait_time_after_min_received,
            aggregator_id=aggregator_id,
            persistor_id=persistor_id,
            shareable_generator_id=shareable_generator_id,
            train_task_name=train_task_name,
            train_timeout=train_timeout,
            ignore_result_error=ignore_result_error,
            task_check_period=task_check_period,
            persist_every_n_rounds=persist_every_n_rounds,
            snapshot_every_n_rounds=snapshot_every_n_rounds,
        )

        # for SCAFFOLD
        self.aggregator_ctrl = None
        self._global_ctrl_weights = None

    def start_controller(self, fl_ctx: FLContext) -> None:
        pass
        # TODO: Print some stats of the correction magnitudes

    def control_flow(self, abort_signal: Signal, fl_ctx: FLContext) -> None:
        pass
