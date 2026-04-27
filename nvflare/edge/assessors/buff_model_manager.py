# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
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

import time
from typing import Dict, Optional, Set

import numpy as np

from nvflare.apis.dxo import DXO, DataKind
from nvflare.apis.fl_context import FLContext
from nvflare.app_common.abstract.model import make_model_learnable
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.app_event_type import AppEventType
from nvflare.edge.aggregators.model_update_dxo import ModelUpdateDXOAggregator
from nvflare.edge.assessors.model_manager import ModelManager
from nvflare.edge.mud import ModelUpdate


class _ModelState:
    def __init__(self, aggr: ModelUpdateDXOAggregator):
        self.aggregator = aggr
        self.devices = {}
        self.last_update_time = None

    def accept(self, model_update: ModelUpdate, fl_ctx: FLContext):
        pass


class BuffModelManager(ModelManager):
    def __init__(
        self,
        num_updates_for_model: int,
        max_model_history: Optional[int] = None,
        global_lr: float = 1.0,
        staleness_weight: bool = False,
    ):
        """Initialize the ModelManager.
        The aggregation scheme and weights are calculated following FedBuff paper "Federated Learning with Buffered Asynchronous Aggregation".
        The staleness_weight can be enabled to apply staleness weighting to model updates.

        Special cases for max_model_history:
        - If None: Keep every model versions, only remove a version when all devices processing it reports back (version no longer related with any device_id in the current_selection from device_manager).

        Args:
            num_updates_for_model (int): Number of updates required before generating a new model version.
            max_model_history (int): Maximum number of historical model versions to keep in memory.
                - None (default): keep every version until all devices processing a particular version report back.
                - positive integer: keep only the latest n versions
            global_lr (float): Global learning rate for model aggregation, default is 1.0.
            staleness_weight (bool): Whether to apply staleness weighting to model updates, default is False.
        """

        super().__init__()
        self.num_updates_for_model = num_updates_for_model
        self.num_updates_counter = 0
        self.max_model_history = max_model_history
        self.global_lr = global_lr
        self.staleness_weight = staleness_weight

    def initialize_model(self, model: DXO, fl_ctx: FLContext):
        pass

    def prune_model_versions(self, versions_to_keep: Set[int], fl_ctx: FLContext) -> None:
        # go through all versions and remove the ones:
        # - either not in versions_to_keep
        # - or too old (current_model_version - v >= max_model_history)
        pass

    def generate_new_model(self, fl_ctx: FLContext) -> None:
        # New model generated based on the current global weights and all updates
        pass

    def process_updates(self, model_updates: Dict[int, ModelUpdate], fl_ctx: FLContext) -> bool:
        pass
