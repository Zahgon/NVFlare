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

"""Decomposers for types from app_common and Machine Learning libraries."""
import os
from typing import Any

from nvflare.app_common.abstract.fl_model import FLModel
from nvflare.app_common.abstract.learnable import Learnable
from nvflare.app_common.abstract.model import ModelLearnable
from nvflare.app_common.widgets.event_recorder import _CtxPropReq, _EventReq, _EventStats
from nvflare.fuel.utils import fobs
from nvflare.fuel.utils.fobs.datum import DatumManager
from nvflare.fuel.utils.fobs.decomposer import DictDecomposer, Externalizer, Internalizer


class FLModelDecomposer(fobs.Decomposer):
    def supported_type(self):
        pass

    def decompose(self, b: FLModel, manager: DatumManager = None) -> Any:
        pass

    def recompose(self, data: tuple, manager: DatumManager = None) -> FLModel:
        pass


def register():
    pass


register.registered = False
