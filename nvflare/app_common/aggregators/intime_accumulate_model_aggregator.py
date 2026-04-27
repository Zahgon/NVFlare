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

from typing import Any, Dict, Union

from nvflare.apis.dxo import DXO, DataKind, from_shareable
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import ReservedKey, ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.abstract.aggregator import Aggregator
from nvflare.app_common.aggregators.dxo_aggregator import DXOAggregator
from nvflare.app_common.app_constant import AppConstants


def _is_nested_aggregation_weights(aggregation_weights):
    pass


def _get_missing_keys(ref_dict: dict, dict_to_check: dict):
    pass


class InTimeAccumulateWeightedAggregator(Aggregator):
    def __init__(
        self,
        exclude_vars: Union[str, Dict[str, str], None] = None,
        aggregation_weights: Union[Dict[str, Any], Dict[str, Dict[str, Any]], None] = None,
        expected_data_kind: Union[DataKind, Dict[str, DataKind]] = DataKind.WEIGHT_DIFF,
        weigh_by_local_iter: bool = True,
    ):
        """Perform accumulated weighted aggregation.

        This is often used as the default aggregation method and can be used for FedAvg. It parses the shareable and
        aggregates the contained DXO(s).

        Args:
            exclude_vars (Union[str, Dict[str, str]], optional):
                Regular expression string to match excluded vars during aggregation. Defaults to None.
                Can be one string or a dict of {dxo_name: regex strings} corresponding to each aggregated DXO
                when processing a DXO of `DataKind.COLLECTION`.
            aggregation_weights (Union[Dict[str, Any], Dict[str, Dict[str, Any]]], optional):
                Aggregation weight for each contributor. Defaults to None.
                Can be one dict of {contrib_name: aggr_weight} or a dict of dicts corresponding to each aggregated DXO
                when processing a DXO of `DataKind.COLLECTION`.
            expected_data_kind (Union[DataKind, Dict[str, DataKind]]):
                DataKind for DXO. Defaults to DataKind.WEIGHT_DIFF
                Can be one DataKind or a dict of {dxo_name: DataKind} corresponding to each aggregated DXO
                when processing a DXO of `DataKind.COLLECTION`. Only the keys in this dict will be processed.
            weigh_by_local_iter (bool, optional): Whether to weight the contributions by the number of iterations
                performed in local training in the current round. Defaults to `True`.
                Setting it to `False` can be useful in applications such as homomorphic encryption to reduce
                the number of computations on encrypted ciphertext.
                The aggregated sum will still be divided by the provided weights and `aggregation_weights` for the
                resulting weighted sum to be valid.
        """
        super().__init__()
        self.logger.debug(f"exclude vars: {exclude_vars}")
        self.logger.debug(f"aggregation weights control: {aggregation_weights}")
        self.logger.debug(f"expected data kind: {expected_data_kind}")

        self._single_dxo_key = ""
        self._weigh_by_local_iter = weigh_by_local_iter

        self.aggregation_weights = aggregation_weights
        self.exclude_vars = exclude_vars
        self.expected_data_kind = expected_data_kind

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        # _initialize() can not be called from the constructor. Because it changes the data, even the data format
        # of the aggregation_weights and exclude_vars parameters. Inspect could not figure out the passed in
        # parameters when re-construct the object creation configuration.
        pass

    def _initialize(self, aggregation_weights, exclude_vars, expected_data_kind):
        # Check expected data kind
        pass

    def accept(self, shareable: Shareable, fl_ctx: FLContext) -> bool:
        """Store shareable and update aggregator's internal state

        Args:
            shareable: information from contributor
            fl_ctx: context provided by workflow

        Returns:
            The first boolean indicates if this shareable is accepted.
            The second boolean indicates if aggregate can be called.
        """
        pass

    def aggregate(self, fl_ctx: FLContext) -> Shareable:
        """Called when workflow determines to generate shareable to send back to contributors

        Args:
            fl_ctx (FLContext): context provided by workflow

        Returns:
            Shareable: the weighted mean of accepted shareables from contributors
        """
        pass
