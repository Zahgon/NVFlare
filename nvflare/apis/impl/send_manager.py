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

from nvflare.apis.controller_spec import ClientTask, SendOrder, Task, TaskCompletionStatus
from nvflare.apis.fl_context import FLContext

from .task_manager import TaskCheckStatus, TaskManager

_KEY_ORDER = "__order"
_KEY_TASK_ASSIGN_TIMEOUT = "__task_assignment_timeout"


class SendTaskManager(TaskManager):
    def __init__(self, task: Task, send_order: SendOrder, task_assignment_timeout):
        """Task manager for send controller.

        Args:
            task (Task): an instance of Task
            send_order (SendOrder): the order of clients to receive task
            task_assignment_timeout (int): timeout value on a client requesting its task
        """
        TaskManager.__init__(self)
        if task_assignment_timeout is None or task_assignment_timeout <= 0:
            task_assignment_timeout = 0
        task.props[_KEY_ORDER] = send_order
        task.props[_KEY_TASK_ASSIGN_TIMEOUT] = task_assignment_timeout

    def check_task_send(self, client_task: ClientTask, fl_ctx: FLContext) -> TaskCheckStatus:
        """Determine whether the task should be sent to the client.

        Args:
            client_task (ClientTask): the task processing state of the client
            fl_ctx (FLContext): fl context that comes with the task request

        Returns:
            TaskCheckStatus: NO_BLOCK for not sending the task, BLOCK for waiting, SEND for OK to send
        """
        pass

    def check_task_exit(self, task: Task) -> Tuple[bool, TaskCompletionStatus]:
        """Determine whether the task should exit.

        Args:
            task (Task): an instance of Task

        Tuple[bool, TaskCompletionStatus]:
            first entry in the tuple means whether to exit the task or not.  If it's True, the task should exit.
            second entry in the tuple indicates the TaskCompletionStatus.
        """
        pass
