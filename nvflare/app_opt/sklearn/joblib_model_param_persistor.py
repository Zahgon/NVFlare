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

import os
from typing import Any, Dict, Optional

from joblib import dump, load

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.app_common.abstract.model import ModelLearnable, ModelLearnableKey, make_model_learnable
from nvflare.app_common.abstract.model_persistor import ModelPersistor
from nvflare.app_common.app_constant import AppConstants

# Key in initial_params that means "load model from this path"
MODEL_PATH_KEY = "model_path"


def validate_model_path(path: Optional[str]) -> None:
    """Require model_path to be absolute if provided.

    All sklearn recipes use this so construction fails fast instead of at runtime
    when the persistor's load_model() runs. Call from recipe __init__ or validators.
    """
    pass


class JoblibModelParamPersistor(ModelPersistor):
    def __init__(
        self,
        initial_params: Optional[Dict[str, Any]] = None,
        save_name: str = "model_param.joblib",
        model_path: Optional[str] = None,
    ):
        """Persist global model parameters from a dict to a joblib file.

        Note that this contains the necessary information to build
        a certain model but may not be directly loadable.

        Unlike PTFileModelPersistor, this persistor does NOT instantiate model classes.
        It only stores and transmits parameter values (e.g., hyperparameters, weights).
        The sklearn model class is instantiated on the client side using these params.

        Args:
            initial_params: Initial parameters dict (e.g., {"n_clusters": 3, "kernel": "rbf"}).
                Hyperparameters/config only; do not put model_path here—use the model_path
                argument instead. Used as fallback when model_path is None and no saved
                model exists in save_path.
            save_name: Filename for saving model params. Defaults to "model_param.joblib".
            model_path: Optional absolute path to a saved model file (.joblib, .pkl).
                If provided, the model is loaded from this path at runtime (file must exist).
                Defaults to None. For backward compatibility, initial_params may still
                contain key "model_path" and will be used if model_path is None.
        """
        super().__init__()
        self.initial_params = initial_params or {}
        self.save_name = save_name
        self.model_path = model_path

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
