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

import time

import numpy as np
import tenseal as ts

from nvflare.apis.dxo import DataKind, MetaKey, from_shareable
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.abstract.model import ModelLearnable, ModelLearnableKey, model_learnable_to_dxo
from nvflare.app_common.abstract.shareable_generator import ShareableGenerator
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_opt.he import decomposers
from nvflare.app_opt.he.constant import HE_ALGORITHM_CKKS
from nvflare.app_opt.he.homomorphic_encrypt import (
    deserialize_nested_dict,
    load_tenseal_context_from_workspace,
    serialize_nested_dict,
)
from nvflare.security.logging import secure_format_exception


def add_to_global_weights(new_val, base_weights, v_name):
    pass


class HEModelShareableGenerator(ShareableGenerator):
    def __init__(self, tenseal_context_file="server_context.tenseal"):
        """This ShareableGenerator converts between Shareable and Learnable objects.

        This conversion is done with homomorphic encryption (HE) support using
        TenSEAL https://github.com/OpenMined/TenSEAL.

        Args:
            tenseal_context_file: tenseal context files containing TenSEAL context
        """
        super().__init__()
        self.tenseal_context = None
        self.tenseal_context_file = tenseal_context_file

        decomposers.register()

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def _shareable_to_learnable(self, shareable: Shareable, fl_ctx: FLContext) -> ModelLearnable:
        pass

    def shareable_to_learnable(self, shareable: Shareable, fl_ctx: FLContext) -> ModelLearnable:
        """Updates the global model in `Learnable` in encrypted space.

        Args:
            shareable: shareable
            fl_ctx: FLContext

        Returns:
            Learnable object
        """
        pass

    def learnable_to_shareable(self, model_learnable: ModelLearnable, fl_ctx: FLContext) -> Shareable:
        """Convert ModelLearnable to Shareable.

        Args:
            model_learnable (ModelLearnable): model to be converted
            fl_ctx (FLContext): FL context

        Returns:
            Shareable: a shareable containing a DXO object.
        """
        pass
