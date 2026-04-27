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

import xgboost as xgb

from nvflare.apis.dxo import DXO, DataKind, from_shareable
from nvflare.apis.event_type import EventType
from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import FLContextKey, ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_opt.xgboost.data_loader import XGBDataLoader
from nvflare.app_opt.xgboost.tree_based.utils import update_model
from nvflare.fuel.utils.import_utils import optional_import
from nvflare.security.logging import secure_format_exception


def mask_sum_hessian(model: dict) -> int:
    """Mask sum_hessian values in model trees for privacy protection.

    Args:
        model: XGBoost model dictionary containing learner and gradient_booster

    Returns:
        Number of trees that were masked
    """
    pass


class FedXGBTreeExecutor(Executor):
    def __init__(
        self,
        training_mode,
        lr_scale,
        data_loader_id: str,
        num_client_bagging: int = 1,
        lr_mode: str = "uniform",
        local_model_path: str = "model.json",
        global_model_path: str = "model_global.json",
        learning_rate: float = 0.1,
        objective: str = "binary:logistic",
        num_local_parallel_tree: int = 1,
        local_subsample: float = 1,
        max_depth: int = 8,
        eval_metric: str = "auc",
        nthread: int = 16,
        tree_method: str = "hist",
        train_task_name: str = AppConstants.TASK_TRAIN,
        use_gpus=False,
    ):
        super().__init__()
        self.client_id = None
        self.writer = None

        self.training_mode = training_mode
        self.num_client_bagging = num_client_bagging
        self.lr = None
        self.lr_scale = lr_scale
        self.base_lr = learning_rate
        self.lr_mode = lr_mode
        self.num_local_parallel_tree = num_local_parallel_tree
        self.local_subsample = local_subsample
        self.local_model_path = local_model_path
        self.global_model_path = global_model_path
        self.objective = objective
        self.max_depth = max_depth
        self.eval_metric = eval_metric
        self.nthread = nthread
        self.tree_method = tree_method
        self.train_task_name = train_task_name
        self.use_gpus = use_gpus
        self.num_local_round = 1

        self.bst = None
        self.global_model_as_dict = None
        self.config = None
        self.local_model = None

        self.data_loader_id = data_loader_id
        self.train_data = None
        self.val_data = None

        # use dynamic shrinkage - adjusted by personalized scaling factor
        if lr_mode not in ["uniform", "scaled"]:
            raise ValueError(f"Only support [uniform] or [scaled] mode, but got {lr_mode}")

    def initialize(self, fl_ctx: FLContext):
        # set the paths according to fl_ctx
        pass

    def _get_effective_learning_rate(self):
        pass

    def _get_xgb_train_params(self):
        pass

    def _local_boost_bagging(self, fl_ctx: FLContext):
        pass

    def _local_boost_cyclic(self, fl_ctx: FLContext):
        # Cyclic mode
        # starting from global model
        # return the whole boosting tree series
        pass

    def train(
        self,
        shareable: Shareable,
        fl_ctx: FLContext,
        abort_signal: Signal,
    ) -> Shareable:
        pass

    def finalize(self, fl_ctx: FLContext):
        # freeing resources in finalize avoids seg fault during shutdown of gpu mode
        pass

    def execute(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass
