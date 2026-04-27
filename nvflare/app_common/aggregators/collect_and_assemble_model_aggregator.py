# Copyright (c) 2026, NVIDIA CORPORATION.  All rights reserved.
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

from typing import Optional

from nvflare.apis.dxo import from_shareable
from nvflare.apis.shareable import ReturnCode
from nvflare.app_common.abstract.fl_model import FLModel, ParamsType
from nvflare.app_common.aggregators.assembler import Assembler
from nvflare.app_common.aggregators.model_aggregator import ModelAggregator
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.utils.fl_model_utils import FLModelUtils


class CollectAndAssembleModelAggregator(ModelAggregator):
    """ModelAggregator adapter for CollectAndAssemble pattern.

    This aggregator bridges the gap between FLModel-based workflows (FedAvg)
    and Assembler-based custom aggregation logic (e.g., K-Means, SVM).

    It wraps an Assembler component and:
    1. Collects FLModel results from clients
    2. Converts them to the format expected by the Assembler
    3. Delegates aggregation to the Assembler
    4. Returns the aggregated result as FLModel

    This enables custom aggregation algorithms to work with the modern
    FedAvg workflow while maintaining InTime aggregation where possible.

    Args:
        assembler_id: ID of the Assembler component to use for aggregation.
    """

    def __init__(self, assembler_id: str):
        super().__init__()
        self.assembler_id = assembler_id
        self.assembler: Optional[Assembler] = None

    def accept_model(self, model: FLModel) -> None:
        """Accept one FLModel from a client.

        Args:
            model: FLModel received from a client
        """
        pass

    def aggregate_model(self) -> FLModel:
        """Aggregate all accepted models using the Assembler.

        Returns:
            FLModel: Aggregated model
        """
        pass

    def reset_stats(self) -> None:
        """Reset aggregation statistics for next round."""
        pass
