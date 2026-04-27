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

from nvflare.apis.event_type import EventType
from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.app_common.abstract.learner_spec import Learner
from nvflare.app_common.workflows.splitnn_workflow import SplitNNConstants
from nvflare.security.logging import secure_format_exception


class SplitNNLearnerExecutor(Executor):
    def __init__(
        self,
        learner_id,
        init_model_task_name=SplitNNConstants.TASK_INIT_MODEL,
        train_task_name=SplitNNConstants.TASK_TRAIN,
    ):
        """Key component to run learner on clients.

        Args:
            learner_id (str): id pointing to the learner object
            train_task_name (str, optional): label to dispatch train task. Defaults to AppConstants.TASK_TRAIN.
            submit_model_task_name (str, optional): label to dispatch submit model task. Defaults to AppConstants.TASK_SUBMIT_MODEL.
            validate_task_name (str, optional): label to dispatch validation task. Defaults to AppConstants.TASK_VALIDATION.
        """
        super().__init__()
        self.learner_id = learner_id
        self.learner = None
        self.init_model_task_name = init_model_task_name
        self.train_task_name = train_task_name

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def initialize(self, fl_ctx: FLContext):
        pass

    def execute(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def finalize(self, fl_ctx: FLContext):
        pass
