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

import gc
import time
from enum import Enum

from nvflare.apis.client import Client
from nvflare.apis.controller_spec import ClientTask, Task
from nvflare.apis.fl_constant import FLContextKey, ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.impl.controller import Controller
from nvflare.apis.shareable import Shareable
from nvflare.apis.signal import Signal
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.app_event_type import AppEventType
from nvflare.edge.assessor import Assessment, Assessor
from nvflare.edge.constants import EdgeTaskHeaderKey
from nvflare.edge.utils import message_topic_for_task_end, message_topic_for_task_update, process_update_from_child
from nvflare.fuel.utils.validation_utils import check_positive_number, check_str
from nvflare.fuel.utils.waiter_utils import WaiterRC, conditional_wait
from nvflare.security.logging import secure_format_exception
from nvflare.widgets.info_collector import GroupInfoCollector, InfoCollector


class TaskDoneReason(Enum):
    ALL_CHILDREN_DONE = "all_children_done"
    ABORTED = "aborted"
    ASSESSED_TASK_DONE = "assessed_task_done"
    ASSESSED_WORKFLOW_DONE = "assessed_workflow_done"


class ScatterAndGatherForEdge(Controller):

    next_task_seq = 0

    def __init__(
        self,
        num_rounds: int = 5,
        assessor_id: str = "assessor",
        task_name=AppConstants.TASK_TRAIN,
        task_check_period: float = 0.5,
        assess_interval: float = 0.5,
        update_interval: float = 1.0,
    ):
        """ScatterAndGatherForEdge Workflow.

        The ScatterAndGatherForEdge workflow is a Fed Average algorithm for hierarchically organized edge devices.

        During the execution of a task, the assessor (specified by assessor_id) is invoked periodically to assess
        the quality of training results to determine whether the task should be continued.

        Args:
            num_rounds (int, optional): The total number of training rounds. Defaults to 5.
            assessor_id (str): ID of the assessor component.
            task_name (str): Name of the train task. Defaults to "train".
            task_check_period (float, optional): interval for checking status of tasks. Defaults to 0.5.
            assess_interval: how often to invoke the assessor during task execution
            update_interval: how often for children to send updates

        Raises:
            TypeError: when any of input arguments does not have correct type
            ValueError: when any of input arguments is out of range
        """
        super().__init__(task_check_period=task_check_period)

        # Check arguments
        check_str("assessor_id", assessor_id)
        check_str("task_name", task_name)
        check_positive_number("task_check_period", task_check_period)
        check_positive_number("assess_interval", assess_interval)
        check_positive_number("update_interval", update_interval)

        self.assessor_id = assessor_id
        self.task_name = task_name
        self.assessor = None

        # config data
        self._num_rounds = num_rounds
        self._assess_interval = assess_interval
        self._update_interval = update_interval

        # workflow phases: init, train, validate
        self._current_round = None
        self._current_task_seq = 0
        self._num_children = 0
        self._children = None
        self._end_task_topic = message_topic_for_task_end(self.task_name)
        self._wf_done = False

    @classmethod
    def get_next_task_seq(cls):
        pass

    def start_controller(self, fl_ctx: FLContext) -> None:
        pass

    def control_flow(self, abort_signal: Signal, fl_ctx: FLContext) -> None:
        pass

    def _monitor_task(self, task: Task, fl_ctx: FLContext, abort_signal: Signal) -> TaskDoneReason:
        pass

    def stop_controller(self, fl_ctx: FLContext):
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def _prepare_train_task_data(self, client_task: ClientTask, fl_ctx: FLContext) -> None:
        pass

    def _process_train_result(self, client_task: ClientTask, fl_ctx: FLContext) -> None:
        pass

    def process_result_of_unknown_task(
        self, client: Client, task_name, client_task_id, result: Shareable, fl_ctx: FLContext
    ) -> None:
        pass

    def _process_update_report(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def _check_abort_signal(self, fl_ctx, abort_signal: Signal):
        pass

    def _accept_update(self, update: Shareable, fl_ctx: FLContext):
        pass
