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


from typing import Any, Optional

from nvflare.apis.dxo import DXO, DataKind, from_shareable
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.abstract.fl_model import FLModel, FLModelConst, MetaKey, ParamsType
from nvflare.app_common.abstract.model import ModelLearnable, ModelLearnableKey, make_model_learnable
from nvflare.app_common.app_constant import AppConstants
from nvflare.fuel.utils.validation_utils import check_object_type

MODEL_ATTRS = [
    FLModelConst.PARAMS_TYPE,
    FLModelConst.PARAMS,
    FLModelConst.METRICS,
    FLModelConst.OPTIMIZER_PARAMS,
    FLModelConst.CURRENT_ROUND,
    FLModelConst.TOTAL_ROUNDS,
    FLModelConst.META,
]


params_type_to_data_kind = {
    ParamsType.FULL.value: DataKind.WEIGHTS,
    ParamsType.DIFF.value: DataKind.WEIGHT_DIFF,
}
data_kind_to_params_type = {v: k for k, v in params_type_to_data_kind.items()}


class FLModelUtils:
    @staticmethod
    def to_shareable(fl_model: FLModel) -> Shareable:
        """From FLModel to NVFlare side shareable.

        This is a temporary solution to converts FLModel to the shareable of existing style,
        so that we can reuse the existing components we have.

        In the future, we should be using the to_dxo, from_dxo directly.
        And all the components should be changed to accept the standard DXO.
        """
        pass

    @staticmethod
    def from_shareable(shareable: Shareable, fl_ctx: Optional[FLContext] = None) -> FLModel:
        """From NVFlare side shareable to FLModel.

        This is a temporary solution to converts the shareable of existing style to FLModel,
        so that we can reuse the existing components we have.

        In the future, we should be using the to_dxo, from_dxo directly.
        And all the components should be changed to accept the standard DXO.
        """
        pass

    @staticmethod
    def to_dxo(fl_model: FLModel) -> DXO:
        """Converts FLModel to a DXO."""
        pass

    @staticmethod
    def from_dxo(dxo: DXO) -> FLModel:
        """Converts DXO to FLModel."""
        pass

    @staticmethod
    def to_model_learnable(fl_model: FLModel) -> ModelLearnable:
        pass

    @staticmethod
    def from_model_learnable(model_learnable: ModelLearnable) -> FLModel:
        pass

    @staticmethod
    def get_meta_prop(model: FLModel, key: str, default=None):
        pass

    @staticmethod
    def set_meta_prop(model: FLModel, key: str, value: Any):
        pass

    @staticmethod
    def get_configs(model: FLModel) -> Optional[dict]:
        pass

    @staticmethod
    def update_model(model: FLModel, model_update: FLModel, replace_meta: bool = True) -> FLModel:
        pass
