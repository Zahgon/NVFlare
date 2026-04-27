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


import os

import xgboost as xgb
from xgboost import callback

from nvflare.apis.event_type import EventType
from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import FLContextKey, ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.apis.workspace import Workspace
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.tracking.log_writer import LogWriter
from nvflare.app_opt.xgboost.data_loader import XGBDataLoader
from nvflare.app_opt.xgboost.histogram_based.constants import XGB_TRAIN_TASK, XGBShareableHeader
from nvflare.app_opt.xgboost.metrics_cb import MetricsCallback
from nvflare.security.logging import secure_format_exception, secure_log_traceback


class XGBoostParams:
    def __init__(
        self, xgb_params: dict, num_rounds: int = 10, early_stopping_rounds: int = 2, verbose_eval: bool = False
    ):
        """Container for all XGBoost parameters.

        Args:
            xgb_params: The Booster parameters. This dict is passed to `xgboost.train()`
                as the argument `params`. It contains all the Booster parameters.
                Please refer to XGBoost documentation for details:
                https://xgboost.readthedocs.io/en/stable/parameter.html
        """
        self.num_rounds = num_rounds
        self.early_stopping_rounds = early_stopping_rounds
        self.verbose_eval = verbose_eval
        self.xgb_params: dict = xgb_params if xgb_params else {}


class FedXGBHistogramExecutor(Executor):
    """Federated XGBoost Executor Spec for histogram-base collaboration.

    This class implements a basic xgb_train logic, feel free to overwrite the function for custom behavior.
    """

    def __init__(
        self,
        num_rounds,
        early_stopping_rounds,
        xgb_params: dict,
        data_loader_id: str,
        verbose_eval=False,
        use_gpus=False,
        metrics_writer_id: str = None,
        model_file_name="test.model.json",
    ):
        """Federated XGBoost Executor for histogram-base collaboration.

        This class sets up the training environment for Federated XGBoost.
        This is the executor running on each NVFlare client, which starts XGBoost training.

        Args:
            num_rounds: number of boosting rounds
            early_stopping_rounds: early stopping rounds
            xgb_params: This dict is passed to `xgboost.train()` as the first argument `params`.
                It contains all the Booster parameters.
                Please refer to XGBoost documentation for details:
                https://xgboost.readthedocs.io/en/stable/python/python_api.html#module-xgboost.training
            data_loader_id: the ID points to XGBDataLoader.
            verbose_eval: verbose_eval in xgboost.train
            use_gpus: flag to enable gpu training
            metrics_writer_id: the ID points to a LogWriter, if provided, a MetricsCallback will be added.
                Users can then use the receivers from nvflare.app_opt.tracking.
            model_file_name (str): where to save the model.
        """
        super().__init__()

        self.num_rounds = num_rounds
        self.early_stopping_rounds = early_stopping_rounds
        self.xgb_params = xgb_params
        self.data_loader_id = data_loader_id
        self.data_loader = None
        self.verbose_eval = verbose_eval
        self.use_gpus = use_gpus

        self.rank = None
        self.world_size = None
        self.client_id = None
        self._ca_cert_path = None
        self._client_key_path = None
        self._client_cert_path = None
        self._server_address = "localhost"
        self.train_data = None
        self.val_data = None
        self.model_file_name = model_file_name

        self._metrics_writer_id = metrics_writer_id
        self._metrics_writer = None

    def initialize(self, fl_ctx):
        pass

    def xgb_train(self, params: XGBoostParams) -> xgb.core.Booster:
        """XGBoost training logic.

        Args:
            params (XGBoostParams): xgboost parameters.

        Returns:
            A xgboost booster.
        """
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def _get_server_address(self, fl_ctx: FLContext):
        pass

    def _get_certificates(self, fl_ctx: FLContext):
        pass

    def execute(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def train(self, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        """XGBoost training task pipeline which handles NVFlare specific tasks"""
        pass
