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

from typing import Optional

from nvflare.apis.dxo import DXO, from_shareable
from nvflare.apis.fl_constant import ReservedKey, ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.abstract.aggregator import Aggregator
from nvflare.app_common.aggregators.assembler import Assembler
from nvflare.app_common.app_constant import AppConstants


class CollectAndAssembleAggregator(Aggregator):
    """Perform collection and flexible assemble aggregation

    This is used for methods needing a special assemble mechanism on the client submissions.
    It first collects all submissions from clients, then delegates the assembling functionality to assembler,
    which is specific to a particular algorithm.
    Note that the aggregation in this case is not in-time, since the assembling function may not be arithmetic mean.
    """

    def __init__(self, assembler_id: str):
        super().__init__()
        self.assembler_id = assembler_id
        self.assembler: Optional[Assembler] = None

    def accept(self, shareable: Shareable, fl_ctx: FLContext) -> bool:
        pass

    def _accept_contribution(self, contributor: str, current_round: int, dxo: DXO, fl_ctx: FLContext) -> bool:
        pass

    def _get_contribution(self, shareable: Shareable, fl_ctx: FLContext) -> Optional[DXO]:
        pass

    def aggregate(self, fl_ctx: FLContext) -> Shareable:
        pass
