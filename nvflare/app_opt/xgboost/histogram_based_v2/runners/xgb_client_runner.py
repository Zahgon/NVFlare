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
from typing import Tuple

import xgboost as xgb
from xgboost import callback

from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import FLContextKey, SystemConfigs
from nvflare.apis.fl_context import FLContext
from nvflare.app_common.tracking.log_writer import LogWriter
from nvflare.app_opt.xgboost.data_loader import XGBDataLoader
from nvflare.app_opt.xgboost.histogram_based_v2.defs import Constant
from nvflare.app_opt.xgboost.histogram_based_v2.runners.xgb_runner import AppRunner
from nvflare.app_opt.xgboost.metrics_cb import MetricsCallback
from nvflare.fuel.utils.config_service import ConfigService
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.utils.cli_utils import get_package_root

PLUGIN_PARAM_KEY = "federated_plugin"
PLUGIN_KEY_NAME = "name"
PLUGIN_KEY_PATH = "path"
MODEL_FILE_NAME = "model.json"


def _check_ctx(ctx: dict):
    pass


class XGBClientRunner(AppRunner, FLComponent):
    def __init__(
        self,
        data_loader_id: str,
        model_file_name: str,
        metrics_writer_id: str = None,
    ):
        FLComponent.__init__(self)
        self.model_file_name = model_file_name
        self.data_loader_id = data_loader_id
        self.logger = get_obj_logger(self)
        self.fl_ctx = None

        self._client_name = None
        self._rank = None
        self._world_size = None
        self._num_rounds = None
        self._data_split_mode = None
        self._secure_training = None
        self._xgb_params = None
        self._xgb_options = None
        self._server_addr = None
        self._data_loader = None
        self._model_dir = None
        self._stopped = False
        self._metrics_writer_id = metrics_writer_id
        self._metrics_writer = None

    def initialize(self, fl_ctx: FLContext):
        pass

    def _xgb_train(self, num_rounds, xgb_params: dict, xgb_options: dict, train_data, val_data) -> xgb.core.Booster:
        """XGBoost training logic.

        Args:
            num_rounds: Number of rounds
            xgb_params: The Boost parameters for XGBoost train method
            xgb_options: Other arguments needed by XGBoost
            train_data: Training data
            val_data: Validation data

        Returns:
            A xgboost booster.
        """
        pass

    def run(self, ctx: dict):
        pass

    def stop(self):
        # currently no way to stop the runner
        pass

    def is_stopped(self) -> Tuple[bool, int]:
        pass
