# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
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

from nvflare.apis.dxo import MetaKey, from_shareable
from nvflare.apis.event_type import EventType
from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.app_common.abstract.learner_spec import Learner
from nvflare.app_common.app_constant import AppConstants, ValidateType
from nvflare.security.logging import secure_format_exception


class LearnerExecutor(Executor):
    def __init__(
        self,
        learner_id,
        train_task=AppConstants.TASK_TRAIN,
        submit_model_task=AppConstants.TASK_SUBMIT_MODEL,
        validate_task=AppConstants.TASK_VALIDATION,
    ):
        """Key component to run learner on clients.

        Args:
            learner_id (str): id of the learner object
            train_task (str, optional): task name for train. Defaults to AppConstants.TASK_TRAIN.
            submit_model_task (str, optional): task name for submit model. Defaults to AppConstants.TASK_SUBMIT_MODEL.
            validate_task (str, optional): task name for validation. Defaults to AppConstants.TASK_VALIDATION.
        """
        super().__init__()
        self.learner_id = learner_id
        self.learner = None
        self.train_task = train_task
        self.submit_model_task = submit_model_task
        self.validate_task = validate_task
        self.is_initialized = False

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def initialize(self, fl_ctx: FLContext):
        pass

    def execute(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def train(self, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def submit_model(self, shareable: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def validate(self, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def finalize(self, fl_ctx: FLContext):
        pass
