# Copyright (c) 2026, NVIDIA CORPORATION.  All rights reserved.
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

import logging
from typing import Dict, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import mutual_info_classif
from sklearn.linear_model import ElasticNet, Lasso, LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.preprocessing import StandardScaler

from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.apis.signal import Signal

try:
    from PyImpetus import PPIMBC

    PYIMPETUS_AVAILABLE = True
except ImportError:
    PYIMPETUS_AVAILABLE = False

logger = logging.getLogger(__name__)

LASSO_ELASTIC_NET_ZERO_THRESHOLD: float = 1e-6


class FeatureElectionExecutor(Executor):
    """
    Client-side executor for the Feature Election federated workflow.

    Handles four request types dispatched by ``FeatureElectionController``:

    * ``feature_selection`` — runs the configured FS method on local data and returns
      a boolean feature mask and per-feature scores.
    * ``tuning_eval`` — evaluates a candidate mask proposed by the controller during
      the hill-climbing phase and returns the local score.
    * ``apply_mask`` — permanently slices ``X_train`` / ``X_val`` to the selected
      features.  **Idempotent**: if the same mask is received a second time (e.g. due
      to task retransmission) the call returns ``OK`` immediately without modifying data.
    * ``train`` — performs one FedAvg round on the masked feature set and returns the
      updated model weights.

    Args:
        fs_method: Feature selection algorithm.  One of ``'lasso'``, ``'elastic_net'``,
            ``'mutual_info'``, ``'random_forest'``, ``'pyimpetus'``.
        fs_params: Extra keyword arguments forwarded to the FS algorithm.
        eval_metric: ``'f1'`` (weighted) or ``'accuracy'``, used for tuning eval and
            local scoring.
        task_name: Must match the ``task_name`` on ``FeatureElectionController``.

    Note:
        Call :meth:`set_data` before the executor is registered with the FL runtime.
        ``FeatureElectionExecutor`` has no ``client_id`` attribute; use
        ``fl_ctx.get_identity_name()`` inside ``_load_data_if_needed`` to retrieve the
        site name assigned by the FL platform.
    """

    def __init__(
        self,
        fs_method: str = "lasso",
        fs_params: Optional[Dict] = None,
        eval_metric: str = "f1",
        task_name: str = "feature_election",
    ):
        super().__init__()
        self.fs_method = fs_method.lower()
        self.fs_params = fs_params or {}
        self.eval_metric = eval_metric
        self.task_name = task_name

        # Data
        self.X_train = None
        self.y_train = None
        self.X_val = None
        self.y_val = None

        # Scaler fitted on X_train; stored so _handle_train and _handle_tuning_eval
        # use the same parameters rather than each reconstructing an identical instance.
        # Reset to None whenever X_train changes (set_data, apply_mask).
        self.scaler = None

        # Use LogisticRegression with LBFGS solver - much faster convergence than SGDClassifier
        # for small-to-medium datasets. warm_start=True allows incremental training across rounds.
        self.global_feature_mask = None
        self.model = LogisticRegression(max_iter=1000, solver="lbfgs", warm_start=True, random_state=42)
        self._model_initialized = False  # Track if model has been fit

        self._set_default_params()

    def _set_default_params(self):
        pass

    def set_data(self, X_train, y_train, X_val=None, y_val=None, feature_names=None):
        """
        Set data for the executor.
        X_val and y_val are optional; if not provided, training data is used for evaluation.
        """
        pass

    def execute(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def evaluate_model(self, X_train, y_train, X_val, y_val, scaler=None) -> float:
        """
        Helper method to train and evaluate a model locally.
        Required for the 'simulate_election' functionality and tests.

        Args:
            scaler: Optional pre-fitted ``StandardScaler``.  When provided the data
                is transformed (not fit-transformed), ensuring the same normalisation
                parameters are used as those established on the same feature set by the
                caller.  When ``None`` a fresh scaler is fitted on ``X_train``.
        """
        pass

    def _handle_feature_selection(self) -> Shareable:
        pass

    def _handle_tuning_eval(self, shareable: Shareable) -> Shareable:
        pass

    def _handle_apply_mask(self, shareable: Shareable) -> Shareable:
        pass

    def _handle_train(self, shareable: Shareable) -> Shareable:
        pass

    def perform_feature_selection(self) -> Tuple[np.ndarray, np.ndarray]:
        pass
