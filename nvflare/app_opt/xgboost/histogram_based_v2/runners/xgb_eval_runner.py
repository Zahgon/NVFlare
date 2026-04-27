# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
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
from sklearn.metrics import roc_auc_score

from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_context import FLContext
from nvflare.app_opt.xgboost.data_loader import XGBDataLoader
from nvflare.app_opt.xgboost.histogram_based_v2.defs import Constant
from nvflare.app_opt.xgboost.histogram_based_v2.runners.xgb_runner import AppRunner
from nvflare.fuel.utils.log_utils import get_obj_logger


def _check_ctx(ctx: dict):
    pass


class XGBEvalRunner(AppRunner, FLComponent):
    def __init__(
        self,
        data_loader_id: str,
        train_workspace_path: str,
    ):
        FLComponent.__init__(self)
        self.data_loader_id = data_loader_id
        self.train_workspace_path = train_workspace_path
        self.logger = get_obj_logger(self)
        self.fl_ctx = None

        self._client_name = None
        self._rank = None
        self._world_size = None
        self._data_split_mode = None
        self._server_addr = None
        self._data_loader = None
        self._stopped = False

    def initialize(self, fl_ctx: FLContext):
        pass

    def _load_trained_model(self) -> xgb.core.Booster:
        """Load the trained model from the training workspace.

        Returns:
            A xgboost booster loaded from the trained model.
        """
        pass

    def _evaluate_model(self, bst: xgb.core.Booster, val_data) -> float:
        """Evaluate the model and return metrics.

        Args:
            bst: The trained XGBoost model
            val_data: Validation data

        Returns:
            AUC score for the evaluation
        """
        pass

    def run(self, ctx: dict):
        pass

    def stop(self):
        # currently no way to stop the runner
        pass

    def is_stopped(self) -> Tuple[bool, int]:
        pass
