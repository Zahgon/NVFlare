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

from typing import Any, Dict, Optional

from nvflare.apis.dxo import DXO, DataKind, MetaKey
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_context import FLContext
from nvflare.app_common.aggregators.weighted_aggregation_helper import WeightedAggregationHelper
from nvflare.app_common.app_constant import AppConstants
from nvflare.fuel.utils.log_utils import get_module_logger


class DXOAggregator(FLComponent):
    def __init__(
        self,
        exclude_vars: Optional[str] = None,
        aggregation_weights: Optional[Dict[str, Any]] = None,
        expected_data_kind: DataKind = DataKind.WEIGHT_DIFF,
        name_postfix: str = "",
        weigh_by_local_iter: bool = True,
    ):
        """Perform accumulated weighted aggregation for one kind of corresponding DXO from contributors.

        Args:
            exclude_vars (str, optional): Regex to match excluded vars during aggregation. Defaults to None.
            aggregation_weights (Dict[str, Any], optional): Aggregation weight for each contributor.
                                Defaults to None.
            expected_data_kind (DataKind): Expected DataKind for this DXO.
            name_postfix: optional postfix to give to class name and show in logger output.
            weigh_by_local_iter (bool, optional): Whether to weight the contributions by the number of iterations
                performed in local training in the current round. Defaults to `True`.
                Setting it to `False` can be useful in applications such as homomorphic encryption to reduce
                the number of computations on encrypted ciphertext.
                The aggregated sum will still be divided by the provided weights and `aggregation_weights` for the
                resulting weighted sum to be valid.
        """
        super().__init__()
        self.expected_data_kind = expected_data_kind
        self.aggregation_weights = aggregation_weights or {}
        self.logger.debug(f"aggregation weights control: {aggregation_weights}")

        self.aggregation_helper = WeightedAggregationHelper(
            exclude_vars=exclude_vars, weigh_by_local_iter=weigh_by_local_iter
        )

        self.warning_count = {}
        self.warning_limit = 10
        self.processed_algorithm = None

        if name_postfix:
            self._name += name_postfix
            self.logger = get_module_logger(self.__module__, f"{self.__class__.__qualname__}{name_postfix}")

    def reset_aggregation_helper(self):
        pass

    def accept(self, dxo: DXO, contributor_name, contribution_round, fl_ctx: FLContext) -> bool:
        """Store DXO and update aggregator's internal state
        Args:
            dxo: information from contributor
            contributor_name: name of the contributor
            contribution_round: round of the contribution
            fl_ctx: context provided by workflow
        Returns:
            The boolean to indicate if DXO is accepted.
        """
        pass

    def aggregate(self, fl_ctx: FLContext) -> DXO:
        """Called when workflow determines to generate DXO to send back to contributors
        Args:
            fl_ctx (FLContext): context provided by workflow
        Returns:
            DXO: the weighted mean of accepted DXOs from contributors
        """
        pass
