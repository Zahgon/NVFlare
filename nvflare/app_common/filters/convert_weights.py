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

from typing import Union

from nvflare.apis.dxo import DXO, DataKind, MetaKey, from_shareable
from nvflare.apis.dxo_filter import DXOFilter
from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable


class ConvertWeights(DXOFilter):

    WEIGHTS_TO_DIFF = "weights_to_diff"
    DIFF_TO_WEIGHTS = "diff_to_weights"

    def __init__(self, direction: str):
        """Convert WEIGHTS to WEIGHT_DIFF or vice versa.

        Args:
            direction (str): control conversion direction.  Either weights_to_diff or diff_to_weights.

        Raises:
            ValueError: when the direction string is neither weights_to_diff nor diff_to_weights
        """
        DXOFilter.__init__(
            self, supported_data_kinds=[DataKind.WEIGHT_DIFF, DataKind.WEIGHTS], data_kinds_to_filter=None
        )
        if direction not in (self.WEIGHTS_TO_DIFF, self.DIFF_TO_WEIGHTS):
            raise ValueError(
                f"invalid convert direction {direction}: must be in {(self.WEIGHTS_TO_DIFF, self.DIFF_TO_WEIGHTS)}"
            )

        self.direction = direction

    def _get_base_weights(self, fl_ctx: FLContext):
        pass

    def process_dxo(self, dxo: DXO, shareable: Shareable, fl_ctx: FLContext) -> Union[None, DXO]:
        """Called by runners to perform weight conversion.

        Args:
            dxo (DXO): dxo to be processed.
            shareable: the shareable that the dxo belongs to
            fl_ctx (FLContext): this context must include TASK_DATA, which is another shareable containing base weights.
              If not, the input shareable will be returned.

        Returns: filtered result
        """
        pass
