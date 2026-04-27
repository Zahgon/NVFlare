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
from nvflare.apis.dxo import DXO, from_shareable
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.abstract.aggregator import Aggregator


class NumDXOAggregator(Aggregator):

    def __init__(self):
        Aggregator.__init__(self)
        self.value = 0
        self.count = 0

    def accept(self, shareable: Shareable, fl_ctx: FLContext) -> bool:
        pass

    def aggregate(self, fl_ctx: FLContext) -> Shareable:
        pass
