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
import threading

from nvflare.apis.dxo import MetaKey
from nvflare.apis.event_type import EventType
from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import FLContextKey, ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.app_common.abstract.fl_model import FLModel
from nvflare.app_common.abstract.model_learner import ModelLearner
from nvflare.app_common.app_constant import AppConstants, ValidateType
from nvflare.app_common.utils.fl_model_utils import FLModelUtils
from nvflare.fuel.utils.validation_utils import check_object_type
from nvflare.security.logging import secure_format_exception


class ModelLearnerExecutor(Executor):
    def __init__(
        self,
        learner_id,
        train_task=AppConstants.TASK_TRAIN,
        submit_model_task=AppConstants.TASK_SUBMIT_MODEL,
        validate_task=AppConstants.TASK_VALIDATION,
        configure_task=AppConstants.TASK_CONFIGURE,
    ):
        """Key component to run learner on clients.

        Args:
            learner_id (str): id of the learner object
            train_task (str, optional): task name for train. Defaults to AppConstants.TASK_TRAIN.
            submit_model_task (str, optional): task name for submit model. Defaults to AppConstants.TASK_SUBMIT_MODEL.
            validate_task (str, optional): task name for validation. Defaults to AppConstants.TASK_VALIDATION.
            configure_task (str, optional): task name for configure. Defaults to AppConstants.TASK_CONFIGURE.
        """
        super().__init__()
        self.learner_id = learner_id
        self.learner = None
        self.learner_name = ""
        self.is_initialized = False
        self.learner_exe_lock = threading.Lock()  # used ensure only one execution at a time

        self.task_funcs = {
            train_task: self.train,
            submit_model_task: self.submit_model,
            validate_task: self.validate,
            configure_task: self.configure,
        }

    def _abort(self, fl_ctx: FLContext):
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def _create_learner(self, fl_ctx: FLContext):
        pass

    def initialize(self, fl_ctx: FLContext):
        pass

    def execute(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        # Do one task at a time since the shareable and fl_ctx are kept in "self".
        pass

    def _do_execute(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    @staticmethod
    def _setup_learner(learner: ModelLearner, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal):
        pass

    def train(self, shareable: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def submit_model(self, shareable: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def validate(self, shareable: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def configure(self, shareable: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def finalize(self, fl_ctx: FLContext):
        pass
