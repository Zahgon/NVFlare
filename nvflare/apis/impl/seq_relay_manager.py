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

import time
from typing import Tuple

from nvflare.apis.controller_spec import ClientTask, Task, TaskCompletionStatus
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReservedHeaderKey, Shareable

from .task_manager import TaskCheckStatus, TaskManager

_KEY_DYNAMIC_TARGETS = "__dynamic_targets"
_KEY_TASK_ASSIGN_TIMEOUT = "__task_assignment_timeout"
_KEY_TASK_RESULT_TIMEOUT = "__task_result_timeout"
_KEY_LAST_SEND_IDX = "__last_send_idx"
_PENDING_CLIENT_TASK = "__pending_client_task"


class SequentialRelayTaskManager(TaskManager):
    def __init__(self, task: Task, task_assignment_timeout, task_result_timeout, dynamic_targets: bool):
        """Task manager for relay controller on SendOrder.SEQUENTIAL.

        Args:
            task (Task): an instance of Task
            task_assignment_timeout (int): timeout value on a client requesting its task
            task_result_timeout (int): timeout value on reply of one client
            dynamic_targets (bool): allow clients to join after this task starts
        """
        TaskManager.__init__(self)
        if task_assignment_timeout is None:
            task_assignment_timeout = 0

        if task_result_timeout is None:
            task_result_timeout = 0

        task.props[_KEY_DYNAMIC_TARGETS] = dynamic_targets
        task.props[_KEY_TASK_ASSIGN_TIMEOUT] = task_assignment_timeout
        task.props[_KEY_TASK_RESULT_TIMEOUT] = task_result_timeout
        task.props[_KEY_LAST_SEND_IDX] = -1  # client index of last send
        task.props[_PENDING_CLIENT_TASK] = None

    def check_task_send(self, client_task: ClientTask, fl_ctx: FLContext) -> TaskCheckStatus:
        """Determine whether the task should be sent to the client.

        Args:
            client_task (ClientTask): the task processing state of the client
            fl_ctx (FLContext): fl context that comes with the task request

        Returns:
            TaskCheckStatus: NO_BLOCK for not sending the task, BLOCK for waiting, SEND for OK to send
        """
        pass

    def _determine_window(self, task: Task) -> Tuple[int, int]:
        """Returns two indexes (starting/ending) of a window of client candidates.

        When starting is negative and ending is 0, the window is closed and the task should exit
        When both starting and ending are negative, there is no client candidate as current client task has not returned

        Args:
            task (Task): an instance of Task

        Returns:
            Tuple[int, int]: starting and ending indices of a window of client candidates.

        """
        pass

    def check_task_exit(self, task: Task) -> Tuple[bool, TaskCompletionStatus]:
        """Determine whether the task should exit.

        Args:
            task (Task): an instance of Task

        Returns:
            Tuple[bool, TaskCompletionStatus]:
                first entry in the tuple means whether to exit the task or not.  If it's True, the task should exit.
                second entry in the tuple indicates the TaskCompletionStatus.
        """
        pass

    def check_task_result(self, result: Shareable, client_task: ClientTask, fl_ctx: FLContext):
        """Check the result received from the client.

        See whether the client_task is the last one in the task's list
        If not, then it is a late response and ReservedHeaderKey.REPLY_IS_LATE is
        set to True in result's header.

        Args:
            result (Shareable): an instance of Shareable
            client_task (ClientTask): the task processing state of the client
            fl_ctx (FLContext): fl context that comes with the task request
        """
        pass
