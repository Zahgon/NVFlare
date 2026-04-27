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
import time
from typing import Dict, List, Optional, Union

from nvflare.apis.client import Client
from nvflare.apis.controller_spec import ClientTask, Task
from nvflare.apis.dxo import DXO, from_shareable
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.apis.signal import Signal
from nvflare.app_common.workflows.error_handling_controller import ErrorHandlingController


class BroadcastAndWait(FLComponent):
    def __init__(self, fl_ctx: FLContext, controller: ErrorHandlingController):
        super().__init__()
        self.lock = threading.Lock()
        self.fl_ctx = fl_ctx
        self.controller = controller
        self.task = None

        # [target, DXO]
        self.results: Dict[str, DXO] = {}

    def broadcast_and_wait(
        self,
        task_name: str,
        task_input: Shareable,
        fl_ctx: FLContext,
        targets: Union[List[Client], List[str], None] = None,
        task_props: Optional[Dict] = None,
        min_responses: int = 1,
        abort_signal: Signal = None,
    ) -> Dict[str, DXO]:
        pass

    def multicasts_and_wait(
        self,
        task_name: str,
        task_inputs: Dict[str, Shareable],
        fl_ctx: FLContext,
        abort_signal: Signal = None,
        task_check_period: int = 0.5,
    ) -> Dict[str, DXO]:

        pass

    def get_tasks(self, task_name: str, task_inputs: Dict[str, Shareable]) -> Dict[str, Task]:
        pass

    def update_result(self, client_name: str, dxo: DXO):
        pass

    def results_cb(self, client_task: ClientTask, fl_ctx: FLContext):
        pass
