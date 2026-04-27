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
import os

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.app_common.abstract.model import ModelLearnable, ModelLearnableKey, make_model_learnable
from nvflare.app_common.abstract.model_persistor import ModelPersistor
from nvflare.app_common.app_constant import AppConstants


class XGBModelPersistor(ModelPersistor):
    def __init__(self, save_name="xgboost_model.json", load_as_dict=True):
        super().__init__()
        self.save_name = save_name
        self.load_as_dict = load_as_dict

    def _initialize(self, fl_ctx: FLContext):
        # get save path from FLContext
        pass

    def load_model(self, fl_ctx: FLContext) -> ModelLearnable:
        """Initialize and load the Model.

        Args:
            fl_ctx: FLContext

        Returns:
            ModelLearnable object
        """
        pass

    def handle_event(self, event: str, fl_ctx: FLContext):
        pass

    def save_model(self, model_learnable: ModelLearnable, fl_ctx: FLContext):
        """Persists the Model object.

        Args:
            model_learnable: ModelLearnable object
            fl_ctx: FLContext
        """
        pass
