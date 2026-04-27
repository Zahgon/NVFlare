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

import json

from nvflare.apis.dxo import DXO, DataKind, from_shareable
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.abstract.model import ModelLearnable, ModelLearnableKey, model_learnable_to_dxo
from nvflare.app_common.abstract.shareable_generator import ShareableGenerator
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_opt.xgboost.tree_based.utils import update_model


class XGBModelShareableGenerator(ShareableGenerator):
    def __init__(self):
        super().__init__()
        self.shareable = None

    def learnable_to_shareable(self, model_learnable: ModelLearnable, fl_ctx: FLContext) -> Shareable:
        """Convert ModelLearnable to Shareable.

        Args:
            model_learnable (ModelLearnable): model to be converted
            fl_ctx (FLContext): FL context

        Returns:
            Shareable: a shareable containing a DXO object.
        """
        pass

    def shareable_to_learnable(self, shareable: Shareable, fl_ctx: FLContext) -> ModelLearnable:
        """Convert Shareable to ModelLearnable.

        Supporting TYPE == TYPE_WEIGHTS

        Args:
            shareable (Shareable): Shareable that contains a DXO object
            fl_ctx (FLContext): FL context

        Returns:
            A ModelLearnable object

        Raises:
            TypeError: if shareable is not of type shareable
            ValueError: if data_kind is not `DataKind.WEIGHTS`
        """
        pass
