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
import os.path

import joblib
import tensorboard

from nvflare.apis.dxo import DXO, DataKind, MetaKey, from_shareable
from nvflare.apis.event_type import EventType
from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import FLContextKey, ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.app_common.abstract.learner_spec import Learner
from nvflare.app_common.app_constant import AppConstants
from nvflare.security.logging import secure_format_exception


def _get_global_params(shareable: Shareable, fl_ctx: FLContext):
    # retrieve current global params download from server's shareable
    pass


class SKLearnExecutor(Executor):
    def __init__(self, learner_id: str, train_task=AppConstants.TASK_TRAIN):
        """An Executor interface for scikit-learn Learner.

        Args:
            learner_id (str): id pointing to the learner object
            train_task (str, optional): label to dispatch train task. Defaults to AppConstants.TASK_TRAIN.
        """
        super().__init__()
        self.learner_id = learner_id
        self.learner = None
        self.train_task = train_task
        self.local_model_path = None
        self.global_model_path = None
        self.client_id = None
        self.writer = None
        self.fl_ctx = None

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def initialize(self, fl_ctx: FLContext):
        pass

    def execute(
        self,
        task_name: str,
        shareable: Shareable,
        fl_ctx: FLContext,
        abort_signal: Signal,
    ) -> Shareable:
        pass

    def train(self, current_round, global_param, fl_ctx: FLContext) -> Shareable:
        pass

    def validate(self, current_round, global_param, fl_ctx: FLContext) -> Shareable:
        # retrieve current global center download from server's shareable
        pass

    def finalize(self, fl_ctx: FLContext):
        pass

    def _print_configs(self, fl_ctx: FLContext):
        # get and print the args
        pass

    def load_log_tracker(self):
        pass

    def log_value(self, key, value, step):
        pass

    def save_model_local(self, model: any) -> None:
        pass

    def save_model_global(self, model: any) -> None:
        pass
