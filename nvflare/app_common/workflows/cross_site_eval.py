# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
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
import shutil
import time

from nvflare.app_common.abstract.fl_model import FLModel
from nvflare.app_common.abstract.model_persistor import ModelPersistor
from nvflare.app_common.app_constant import AppConstants, DefaultCheckpointFileName, ModelName
from nvflare.app_common.utils.fl_model_utils import FLModelUtils
from nvflare.fuel.utils import fobs

from .model_controller import ModelController


class CrossSiteEval(ModelController):
    def __init__(
        self,
        *args,
        cross_val_dir=AppConstants.CROSS_VAL_DIR,
        submit_model_timeout=600,
        validation_timeout: int = 6000,
        server_models=[DefaultCheckpointFileName.GLOBAL_MODEL],
        participating_clients=None,
        **kwargs,
    ):
        """Cross Site Evaluation Workflow.

        # TODO: change validation to evaluation to reflect the real meaning

        Args:
            cross_val_dir (str, optional): Path to cross site validation directory relative to run directory.
                Defaults to "cross_site_val".
            submit_model_timeout (int, optional): Timeout of submit_model_task. Defaults to 600 secs.
            validation_timeout (int, optional): Timeout for validate_model task. Defaults to 6000 secs.
            participating_clients (list, optional): List of participating client names. If not provided, defaults
                to all clients connected at start of controller.

        """
        super().__init__(*args, **kwargs)
        self._cross_val_dir = cross_val_dir
        self._submit_model_timeout = submit_model_timeout
        self._validation_timeout = validation_timeout
        self._server_models = server_models
        self._participating_clients = participating_clients

        self._val_results = {}
        self._client_models = {}

        self._cross_val_models_dir = None
        self._cross_val_results_dir = None

        self._results_dir = AppConstants.CROSS_VAL_DIR
        self._json_val_results = {}
        self._json_file_name = "cross_val_results.json"

    def initialize(self, fl_ctx):
        pass

    def run(self) -> None:
        pass

    def _receive_local_model_cb(self, model: FLModel):
        pass

    def _send_validation_task(self, model_name: str, model: FLModel):
        pass

    def _receive_val_result_cb(self, model: FLModel):
        pass

    def track_results(self, model_owner, data_client, val_results: FLModel):
        pass

    def save_results(self):
        pass
