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

import numpy as np

from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.app_common.abstract.model import ModelLearnable, ModelLearnableKey, make_model_learnable
from nvflare.app_common.abstract.model_persistor import ModelPersistor
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.app_event_type import AppEventType
from nvflare.app_common.model_desc import ModelDescriptor
from nvflare.app_common.np.constants import NPConstants
from nvflare.app_common.np.utils import load_numpy_model
from nvflare.security.logging import secure_format_exception


def _get_run_dir(fl_ctx: FLContext):
    pass


class NPFileModelPersistor(ModelPersistor):
    def __init__(
        self,
        last_global_model_file_name="last_global_model.npy",
        best_global_model_file_name="best_global_model.npy",
        model_dir="models",
        model_file_name="model.npy",
        source_ckpt_file_full_name: str = None,
    ):
        """Persist numpy model to/from file system.

        Args:
            last_global_model_file_name: Filename for last global model.
            best_global_model_file_name: Filename for best global model.
            model_dir: Directory for model files (relative to run dir).
            model_file_name: Filename for model (relative to model_dir).
            source_ckpt_file_full_name: Full absolute path to source checkpoint file.
                This path may not exist locally (server-side path). If provided and
                exists at runtime, it takes priority over model_file_name.
        """
        super().__init__()

        self.model_dir = model_dir
        self.last_global_model_file_name = last_global_model_file_name
        self.best_global_model_file_name = best_global_model_file_name
        self.model_file_name = model_file_name
        self.source_ckpt_file_full_name = source_ckpt_file_full_name
        # Note: We don't validate existence here because the checkpoint path may be
        # a server-side path that doesn't exist on the job submission machine.

        # This is default model that will be used if no model is provided.
        self.default_data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=np.float32)

    def load_model(self, fl_ctx: FLContext) -> ModelLearnable:
        pass

    def save_model(self, model_learnable: ModelLearnable, fl_ctx: FLContext):
        pass

    def _save(self, fl_ctx: FLContext, model_learnable: ModelLearnable, file_name: str):
        pass

    def handle_event(self, event: str, fl_ctx: FLContext):
        pass

    def _model_file_path(self, fl_ctx: FLContext, file_name):
        pass

    def _add_to_inventory(self, inventory: dict, fl_ctx: FLContext, file_name: str):
        pass

    def get_model_inventory(self, fl_ctx: FLContext) -> {str: ModelDescriptor}:
        """Get the model inventory of the ModelPersistor.

        Args:
            fl_ctx: FLContext

        Returns: { model_kind: ModelDescriptor }

        """
        pass

    def get_model(self, model_file: str, fl_ctx: FLContext) -> ModelLearnable:
        pass
