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

from abc import ABC, abstractmethod
from typing import Optional

from nvflare.apis.dxo import DXO
from nvflare.apis.event_type import EventType
from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.app_common.abstract.task_handler import TaskHandler


class ErrorHandlingExecutor(Executor, ABC):
    """This class adds error handling mechanisms to Executor spec.

    It also makes sharable convertible to DXO.
    It delegates the task execution to TaskHandler.
    """

    def __init__(self):
        super().__init__()
        self.init_status_ok = True
        self.init_failure = {"abort_job": None, "fail_client": None}
        self.client_name = None
        self.task_handler: Optional[TaskHandler] = None

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def initialize(self, fl_ctx: FLContext):
        pass

    @abstractmethod
    def get_task_handler(self, fl_ctx: FLContext) -> TaskHandler:
        pass

    @abstractmethod
    def get_data_kind(self) -> str:
        pass

    def execute(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def _check_init_status(self, fl_ctx: FLContext):

        pass

    def finalize(self, fl_ctx: FLContext):
        pass
