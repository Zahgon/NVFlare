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

from typing import Optional

from nvflare.apis.client import Client
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.apis.signal import Signal
from nvflare.app_common.app_constant import PSIConst
from nvflare.app_common.psi.psi_workflow_spec import PSIWorkflow
from nvflare.app_common.utils.component_utils import check_component_type
from nvflare.app_common.workflows.error_handling_controller import ErrorHandlingController


class PSIController(ErrorHandlingController):
    def __init__(self, psi_workflow_id: str):
        super().__init__()
        self.psi_workflow_id = psi_workflow_id
        self.psi_workflow: Optional[PSIWorkflow] = None
        self.fl_ctx = None
        self.task_name = PSIConst.TASK

    def control_flow(self, abort_signal: Signal, fl_ctx: FLContext):
        pass

    def start_controller(self, fl_ctx: FLContext):
        pass

    def stop_controller(self, fl_ctx: FLContext):
        pass

    def process_result_of_unknown_task(
        self, client: Client, task_name: str, client_task_id: str, result: Shareable, fl_ctx: FLContext
    ):
        pass

    def load_psi_workflow(self, fl_ctx: FLContext) -> PSIWorkflow:
        pass
