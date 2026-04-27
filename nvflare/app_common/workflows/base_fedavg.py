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

from typing import List

from nvflare.apis.fl_constant import FLMetaKey
from nvflare.app_common.abstract.fl_model import FLModel
from nvflare.app_common.abstract.model import make_model_learnable
from nvflare.app_common.aggregators.weighted_aggregation_helper import (
    WeightedAggregationHelper,
    filter_aggregatable_metrics,
)
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.app_event_type import AppEventType
from nvflare.app_common.utils.fl_model_utils import FLModelUtils
from nvflare.fuel.utils.memory_utils import cleanup_memory
from nvflare.fuel.utils.validation_utils import check_non_negative_int
from nvflare.security.logging import secure_format_exception

from .model_controller import ModelController


class BaseFedAvg(ModelController):
    def __init__(
        self,
        *args,
        num_clients: int = 3,
        num_rounds: int = 5,
        start_round: int = 0,
        memory_gc_rounds: int = 0,
        **kwargs,
    ):
        """The base controller for FedAvg Workflow. *Note*: This class is based on the `ModelController`.

        Implements [FederatedAveraging](https://arxiv.org/abs/1602.05629).

        A model persistor can be configured via the `persistor_id` argument of the `ModelController`.
        The model persistor is used to load the initial global model which is sent to a list of clients.
        Each client sends it's updated weights after local training which is aggregated.
        Next, the global model is updated.
        The model_persistor will also save the model after training.

        Provides the default implementations for the follow routines:
            - def aggregate(self, results: List[FLModel], aggregate_fn=None) -> FLModel
            - def update_model(self, aggr_result)

        The `run` routine needs to be implemented by the derived class:

            - def run(self)

        Args:
            num_clients (int, optional): The number of clients. Defaults to 3. NOTE: this argument should not be here
            we will remove this argument in next release.
            num_rounds (int, optional): The total number of training rounds. Defaults to 5.
            start_round (int, optional): The starting round number.
            memory_gc_rounds (int, optional): Run memory cleanup (gc.collect + malloc_trim) every N rounds.
                Set to 0 to disable. Defaults to 0 (disabled).
        """
        super().__init__(*args, **kwargs)

        check_non_negative_int("memory_gc_rounds", memory_gc_rounds)

        self.num_clients = num_clients
        self.num_rounds = num_rounds
        self.start_round = start_round
        self.memory_gc_rounds = memory_gc_rounds

        self.current_round = None

    def _maybe_cleanup_memory(self):
        """Perform memory cleanup if configured (every N rounds based on memory_gc_rounds)."""
        pass

    @staticmethod
    def _check_results(results: List[FLModel]):
        pass

    @staticmethod
    def aggregate_fn(results: List[FLModel]) -> FLModel:
        """Aggregate model params and metrics across results with weighted averaging.

        Note:
            Metric values that do not support weighted arithmetic are skipped during
            aggregation. If no aggregatable metrics remain after filtering, the
            aggregated metrics are returned as ``None``.
        """
        pass

    def aggregate(self, results: List[FLModel], aggregate_fn=None) -> FLModel:
        """Called by the `run` routine to aggregate the training results of clients.

        Args:
            results: a list of FLModel containing training results of the clients.
            aggregate_fn: a function that turns the list of FLModel into one resulting (aggregated) FLModel.

        Returns: aggregated FLModel.

        """
        pass

    def update_model(self, model, aggr_result):
        """Called by the `run` routine to update the current global model (self.model) given the aggregated result.

        Args:
            model: FLModel to be updated.
            aggr_result: aggregated FLModel.

        Returns: None.

        """
        pass
