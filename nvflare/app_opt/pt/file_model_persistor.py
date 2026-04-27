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

import json
import os
import re
from collections import OrderedDict
from typing import Any, Dict, Optional, Union

import torch

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import FLContextKey, WorkspaceConstants
from nvflare.apis.fl_context import FLContext
from nvflare.app_common.abstract.model import ModelLearnable
from nvflare.app_common.abstract.model_persistor import ModelPersistor
from nvflare.app_common.app_constant import AppConstants, DefaultCheckpointFileName, EnvironmentKey
from nvflare.app_common.app_event_type import AppEventType
from nvflare.app_common.model_desc import ModelDescriptor
from nvflare.app_opt.pt.decomposers import TensorDecomposer
from nvflare.app_opt.pt.model_persistence_format_manager import PTModelPersistenceFormatManager
from nvflare.fuel.utils import fobs


class PTFileModelPersistor(ModelPersistor):
    def __init__(
        self,
        exclude_vars: Optional[str] = None,
        model: Optional[Union[torch.nn.Module, str, Dict[str, Any]]] = None,
        global_model_file_name: str = DefaultCheckpointFileName.GLOBAL_MODEL,
        best_global_model_file_name: str = DefaultCheckpointFileName.BEST_GLOBAL_MODEL,
        source_ckpt_file_full_name: Optional[str] = None,
        filter_id: Optional[str] = None,
        load_weights_only: bool = True,
        allow_numpy_conversion: bool = True,
    ):
        """Persist pytorch-based model to/from file system.

        This Model Persistor tries to load PT model data in the following three ways:

            1. Load from a specified source checkpoint file
            2. Load from a location from the app folder
            3. Load from a torch model object

        The Persistor tries method 1 first if the source_ckpt_file_full_name is specified;
        If source_ckpt_file_full_name is not specified, it tries method 2;
        If no checkpoint location is specified in the app folder, it tries method 3.

        Method 2 - Load from a location from the app folder

        It is assumed that the app folder must contain the environments.json file. Among other things, this
        JSON file must specify where to find the checkpoint file. It does so with two JSON elements:

            - APP_CKPT_DIR: specifies the folder (within the app) where the checkpoint file resides.
            - APP_CKPT: specifies the base file name of the checkpoint

        Here is an example of the environments.json content::

            {
                "APP_CKPT_DIR": "model",
                "APP_CKPT": "pretrained_model.pt"
            }

        In this example, the checkpoint file is located in the "model" folder within the app and is named
        pretrained_model.pt.

        Method 3 - Load from a torch model object. In this case, the 'model' arg must be a valid torch
        model, or the component ID of a valid torch model included in the "components" section of
        your config_fed_server.json.

        If all 3 methods fail, system_panic() is called.

        If checkpoint folder name is specified, then global model and best global model will be saved to it;
        Otherwise they will be saved directly in the app folder.

        The model is saved in a dict depending on the persistor you used. You might need to access it with
        ``model.load_state_dict(torch.load(path_to_model)["model"])`` as there is additional meta information together with the model weights.

        Args:
            exclude_vars (str, optional): regex expression specifying weight vars to be excluded from training. Defaults to None.
            model: Model input. Can be one of:
                - torch.nn.Module: Direct model instance
                - str: Component ID of a model registered in config
                - dict: {"path": "fully.qualified.Class", "args": {...}} for dynamic instantiation
                Defaults to None.
            global_model_file_name (str, optional): file name for saving global model. Defaults to DefaultCheckpointFileName.GLOBAL_MODEL.
            best_global_model_file_name (str, optional): file name for saving best global model. Defaults to DefaultCheckpointFileName.BEST_GLOBAL_MODEL.
            source_ckpt_file_full_name (str, optional): full file name for source model checkpoint file. Defaults to None.
            filter_id: Optional string that defines a filter component that is applied to prepare the model to be saved,
                e.g. for serialization of custom Python objects.
            load_weights_only: Indicates whether torch's unpickler should be restricted to loading only tensors, primitive types, dictionaries
                and any types added via :func:`torch.serialization.add_safe_globals`. Defaults to True (safe mode). Set to False
                for legacy checkpoints that require full unpickling (pre-PyTorch 2.6 behavior).
            allow_numpy_conversion (bool): If set to True, enables conversion between PyTorch tensors and NumPy arrays.
                PyTorch tensors will be converted to NumPy arrays during 'load_model',
                and NumPy arrays will be converted to PyTorch tensors during 'save_model'. Defaults to True.
        Raises:
            ValueError: when source_ckpt_file_full_name does not exist
        """
        super().__init__(
            filter_id=filter_id,
        )
        self.exclude_vars = re.compile(exclude_vars) if exclude_vars else None
        self.model = model
        self.log_dir = None
        self.ckpt_preload_path = None
        self.persistence_manager = None
        self.ckpt_dir_env_key = EnvironmentKey.CHECKPOINT_DIR
        self.ckpt_file_name_env_key = EnvironmentKey.CHECKPOINT_FILE_NAME
        self.global_model_file_name = global_model_file_name
        self.best_global_model_file_name = best_global_model_file_name
        self.source_ckpt_file_full_name = source_ckpt_file_full_name
        self.load_weights_only = load_weights_only
        self._allow_numpy_conversion = allow_numpy_conversion

        self.default_train_conf = None

        # Note: We don't validate existence here because the checkpoint path may be
        # a server-side path that doesn't exist on the job submission machine.
        # Existence is validated at runtime in load_model() when the job executes.

    def _initialize(self, fl_ctx: FLContext):
        pass

    def load_model(self, fl_ctx: FLContext) -> ModelLearnable:
        """Convert initialised model into Learnable/Model format.

        Args:
            fl_ctx (FLContext): FL Context delivered by workflow

        Returns:
            Model: a Learnable/Model object
        """
        pass

    def _get_persistence_manager(self, fl_ctx: FLContext):
        pass

    def handle_event(self, event: str, fl_ctx: FLContext):
        pass

    def save_model_file(self, save_path: str):
        pass

    def save_model(self, ml: ModelLearnable, fl_ctx: FLContext):
        pass

    def get_model(self, model_file: str, fl_ctx: FLContext) -> ModelLearnable:
        pass

    def _get_model_from_location(self, location, fl_ctx):
        pass

    def get_model_inventory(self, fl_ctx: FLContext) -> Dict[str, ModelDescriptor]:
        pass
