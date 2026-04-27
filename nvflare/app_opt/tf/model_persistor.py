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
from typing import Any, Dict, Optional, Union

import tensorflow as tf

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_context import FLContext
from nvflare.app_common.abstract.model import ModelLearnable, ModelLearnableKey, make_model_learnable
from nvflare.app_common.abstract.model_persistor import ModelPersistor
from nvflare.app_common.model_desc import ModelDescriptor
from nvflare.app_opt.tf.utils import flat_layer_weights_dict, unflat_layer_weights_dict


class TFModelPersistor(ModelPersistor):
    def __init__(
        self,
        model: Optional[Union[tf.keras.Model, Dict[str, Any]]] = None,
        save_name: str = "tf_model.weights.h5",
        filter_id: Optional[str] = None,
        source_ckpt_file_full_name: Optional[str] = None,
    ):
        """Persist TensorFlow/Keras model to/from file system.

        This persistor supports loading from a source checkpoint file, which is useful
        for pre-trained models. The checkpoint path may be a server-side path that
        doesn't exist on the job submission machine.

        Args:
            model: Model input. Can be one of:
                - tf.keras.Model: Direct model instance
                - dict: {"path": "fully.qualified.Class", "args": {...}} for dynamic instantiation
                - None: If source_ckpt_file_full_name points to a full model file
            save_name: Filename for saving model weights. Defaults to "tf_model.weights.h5".
            filter_id: Optional filter component ID for model serialization.
            source_ckpt_file_full_name: Full path to source checkpoint file.
                This path may not exist locally (server-side path).
        """
        super().__init__(
            filter_id=filter_id,
        )
        self.save_name = save_name
        self.model = model
        self.source_ckpt_file_full_name = source_ckpt_file_full_name
        # Note: We don't validate existence here because the checkpoint path may be
        # a server-side path that doesn't exist on the job submission machine.

    def _initialize(self, fl_ctx: FLContext):
        pass

    def load_model(self, fl_ctx: FLContext) -> ModelLearnable:
        """Initializes and loads the Model.

        Args:
            fl_ctx: FLContext

        Returns:
            ModelLearnable object
        """
        pass

    def handle_event(self, event: str, fl_ctx: FLContext):
        pass

    def save_model(self, model_learnable: ModelLearnable, fl_ctx: FLContext):
        """Saves model.

        Args:
            model_learnable: ModelLearnable object
            fl_ctx: FLContext
        """
        pass

    def get_model(self, model_file: str, fl_ctx: FLContext) -> ModelLearnable:
        """Get a specific model by file name for cross-site evaluation.

        Args:
            model_file: Name/path of the model file to load
            fl_ctx: FLContext

        Returns:
            ModelLearnable object or None if model not found
        """
        pass

    def _get_model_from_location(self, location: str, fl_ctx: FLContext) -> ModelLearnable:
        """Load model from a specific file location.

        Args:
            location: Full path to model file
            fl_ctx: FLContext

        Returns:
            ModelLearnable object or None if loading fails
        """
        pass

    def get_model_inventory(self, fl_ctx: FLContext) -> Dict[str, ModelDescriptor]:
        """Get inventory of available models for cross-site evaluation.

        Args:
            fl_ctx: FLContext

        Returns:
            Dictionary mapping model names to ModelDescriptor objects
        """
        pass
