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
import random
import threading
import time
from typing import Optional

from nvflare.apis.event_type import EventType
from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import FLContextKey, ReservedKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReturnCode, Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.app_common.app_constant import AppConstants
from nvflare.edge.constants import EdgeTaskHeaderKey
from nvflare.edge.updater import Updater
from nvflare.edge.utils import message_topic_for_task_end, message_topic_for_task_update, process_update_from_child
from nvflare.fuel.utils.tree_utils import Forest, Node
from nvflare.fuel.utils.validation_utils import check_positive_number, check_str
from nvflare.fuel.utils.waiter_utils import WaiterRC, conditional_wait
from nvflare.security.logging import secure_format_exception


class TaskInfo:
    def __init__(self, task: Shareable):
        self.task = task
        self.cookie_jar = task.get_cookie_jar()
        self.round = task.get_header(AppConstants.CURRENT_ROUND)
        self.id = task.get_header(ReservedKey.TASK_ID)
        self.name = task.get_header(ReservedKey.TASK_NAME)
        self.seq = task.get_header(EdgeTaskHeaderKey.TASK_SEQ)
        self.update_interval = task.get_header(EdgeTaskHeaderKey.UPDATE_INTERVAL, 1.0)


class HierarchicalUpdateGatherer(Executor):
    def __init__(
        self,
        learner_id: str,
        updater_id: str,
        update_timeout,
    ):
        Executor.__init__(self)

        check_str("learner_id", learner_id)
        check_str("updater_id", updater_id)
        check_positive_number("update_timeout", update_timeout)
        self.learner_id = learner_id
        self.updater_id = updater_id
        self.update_timeout = update_timeout

        self._pending_task = None
        self._pending_clients = {}
        self._updater = None
        self._learner = None
        self._status_lock = threading.Lock()
        self._update_lock = threading.Lock()
        self._process_error = None
        self._task_start_time = None
        self._children = None
        self._num_children = 0
        self._num_children_done = 0
        self._parent_name = None
        self._task_done = False

        self._msg_handler_registered = {}  # topic => bool
        self.register_event_handler(EventType.START_RUN, self._hug_handle_start_run)
        self.register_event_handler(EventType.POST_TASK_ASSIGNMENT_SENT, self._handle_task_sent)
        self.register_event_handler(EventType.POST_TASK_RESULT_RECEIVED, self._handle_result_received)

    def get_updater(self, fl_ctx: FLContext) -> Optional[Updater]:
        pass

    def _hug_handle_start_run(self, event_type: str, fl_ctx: FLContext):
        pass

    def _handle_task_sent(self, event_type: str, fl_ctx: FLContext):
        # the task was sent to a child client
        pass

    def _handle_result_received(self, event_type: str, fl_ctx: FLContext):
        # received results from a child client
        pass

    def _pending_clients_status(self):
        pass

    def _update_client_status(self, client_name, status):
        pass

    def execute(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        """Execute the assigned task.
        If we are a leaf node in client hierarchy, we'll execute the task by using the configured executor for the
        task name "exec_<task_name>". This way different tasks can be handled by different executors.

        If we are not leaf node, we'll wait for results from child clients and then aggregate their results using
        the configured aggregator.

        Args:
            task_name: name of the assigned task
            shareable: task data
            fl_ctx: FLContext object
            abort_signal: signal to notify abort

        Returns: task result

        """
        pass

    def _do_task(self, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def _check_task_done(self):
        pass

    def _make_update_report(self, task_info: TaskInfo, fl_ctx: FLContext):
        pass

    def _prepare_update(self, fl_ctx: FLContext):
        pass

    def _process_task_end(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        # process notification from parent that task is ended
        pass

    def _process_child_update(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        """Process update received from a child.
        Every time an update is received from a child, we call the "updater" to accept the update and return the
        reply from the updater back to the child.

        Args:
            topic: topic of the update message
            update: the update data from child
            fl_ctx: FLContext object

        Returns: reply from the updater

        """
        pass

    def _accept_child_update(self, update: Shareable, fl_ctx: FLContext, current_round) -> (bool, Shareable):
        pass

    def accept_update(self, task_id: str, update: Shareable, fl_ctx: FLContext) -> bool:
        """This is to be called by subclass to accept a specified update

        Args:
            task_id: ID of the task
            update: the update to be accepted.
            fl_ctx: FLContext object

        Returns: whether the update is accepted

        """
        pass

    def set_task_done(self, task_id: str, fl_ctx: FLContext) -> bool:
        """This method is to be called by subclass to forcefully end the specified task

        Args:
            task_id: ID of the task to be ended
            fl_ctx: FLContext object

        Returns: whether this request is accepted

        """
        pass

    def get_current_task(self, fl_ctx: FLContext) -> Optional[TaskInfo]:
        """Get the info of current task

        Returns: TaskInfo of current task or None if no current task

        Note: During the life of the task processing, the "task" data of the TaskInfo could be updated many times.

        """
        pass

    def task_started(self, task: TaskInfo, fl_ctx: FLContext):
        """This method is called when a task assignment is received from the controller.
        Subclass can implement this method to prepare for task processing.

        Args:
            task: info of the received task
            fl_ctx: FLContext object

        Returns: None

        """
        pass

    def task_ended(self, task: TaskInfo, fl_ctx: FLContext):
        """This method is called when the current task is ended.
        Subclass can implement this method to finish task processing.

        Args:
            task: info of the task that is ended
            fl_ctx: FLContext object

        Returns: None

        """
        pass
