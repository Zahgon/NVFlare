# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
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
import uuid
from typing import List, Optional, Union

from nvflare.apis.client import Client
from nvflare.apis.controller_spec import ClientTask, SendOrder, Task, TaskCompletionStatus
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import FilterKey, FLContextKey, ReservedKey, ReservedTopic, ReturnCode, SiteType
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReservedHeaderKey, Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.apis.utils.task_utils import apply_filters
from nvflare.apis.wf_comm_spec import WFCommSpec
from nvflare.app_common.ccwf.common import Constant
from nvflare.fuel.utils.msg_root_utils import delete_msg_root
from nvflare.private.fed.utils.fed_utils import get_target_names
from nvflare.private.privacy_manager import Scope
from nvflare.security.logging import secure_format_exception


class WFCommClient(FLComponent, WFCommSpec):
    def __init__(
        self,
        max_task_timeout: int = Constant.MAX_TASK_TIMEOUT,
    ) -> None:
        """Communicator using aux channel communication.

        Args:
            max_task_timeout (int, optional): Maximum task timeout when `task.timeout` is set to 0. Defaults to 3600.
        """
        super().__init__()
        self.task_data_filters = {}
        self.task_result_filters = {}
        self.max_task_timeout = max_task_timeout

    def broadcast(
        self,
        task: Task,
        fl_ctx: FLContext,
        targets: Union[List[Client], List[str], None] = None,
        min_responses: int = 0,
        wait_time_after_min_received: int = 0,
    ):
        pass

    def broadcast_and_wait(
        self,
        task: Task,
        fl_ctx: FLContext,
        targets: Union[List[Client], List[str], None] = None,
        min_responses: int = 0,
        wait_time_after_min_received: int = 0,
        abort_signal: Signal = None,
    ):
        pass

    def _make_error_reply(self, error_type, targets):
        pass

    def _get_client(self, client, engine) -> Client:
        pass

    def _call_task_cb(self, task_cb, client, task, fl_ctx):
        pass

    def _get_client_task(self, client, task):
        pass

    def send(
        self,
        task: Task,
        fl_ctx: FLContext,
        targets: Union[List[Client], List[str], None] = None,
        send_order: SendOrder = SendOrder.SEQUENTIAL,
        task_assignment_timeout: int = 0,
    ):
        pass

    def send_and_wait(
        self,
        task: Task,
        fl_ctx: FLContext,
        targets: Union[List[Client], List[str], None] = None,
        send_order: SendOrder = SendOrder.SEQUENTIAL,
        task_assignment_timeout: int = 0,
        abort_signal: Signal = None,
    ):
        pass

    def relay(
        self,
        task: Task,
        fl_ctx: FLContext,
        targets: Union[List[Client], List[str], None] = None,
        send_order: SendOrder = SendOrder.SEQUENTIAL,
        task_assignment_timeout: int = 0,
        task_result_timeout: int = 0,
        dynamic_targets: bool = True,
    ):
        pass

    def relay_and_wait(
        self,
        task: Task,
        fl_ctx: FLContext,
        targets: Union[List[Client], List[str], None] = None,
        send_order=SendOrder.SEQUENTIAL,
        task_assignment_timeout: int = 0,
        task_result_timeout: int = 0,
        dynamic_targets: bool = True,
        abort_signal: Optional[Signal] = None,
    ):
        pass

    def _validate_target(self, engine, targets):
        pass
