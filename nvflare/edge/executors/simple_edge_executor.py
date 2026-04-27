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
from typing import Optional

from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReservedHeaderKey, Shareable
from nvflare.edge.constants import EdgeApiStatus, MsgKey
from nvflare.edge.executors.ete import EdgeTaskExecutor
from nvflare.edge.executors.hug import TaskInfo
from nvflare.edge.web.models.result_report import ResultReport
from nvflare.edge.web.models.result_response import ResultResponse
from nvflare.edge.web.models.selection_request import SelectionRequest
from nvflare.edge.web.models.selection_response import SelectionResponse
from nvflare.edge.web.models.task_request import TaskRequest
from nvflare.edge.web.models.task_response import TaskResponse
from nvflare.security.logging import secure_format_exception


class SimpleEdgeExecutor(EdgeTaskExecutor):
    """A very simple edge executor that only does aggregation"""

    def __init__(self, updater_id, update_timeout=60):
        EdgeTaskExecutor.__init__(self, updater_id, update_timeout)
        self.devices = None

    def convert_task(self, task_data: Shareable, current_task: TaskInfo, fl_ctx: FLContext) -> dict:
        """Convert task_data to a plain dict"""
        pass

    def convert_result(self, result: dict, current_task: TaskInfo, fl_ctx: FLContext) -> Shareable:
        """Convert result from device to shareable"""
        pass

    def process_edge_task_request(
        self, request: TaskRequest, current_task: TaskInfo, fl_ctx: FLContext
    ) -> TaskResponse:
        """Handle task request from device"""
        pass

    def process_edge_result_report(
        self, report: ResultReport, current_task: TaskInfo, fl_ctx: FLContext
    ) -> ResultResponse:
        """Handle result report from device
        The report task_id may be different from current task_id. Let HAM deal with it
        """
        pass

    def task_started(self, task: TaskInfo, fl_ctx: FLContext):
        pass

    def task_ended(self, task: TaskInfo, fl_ctx: FLContext):
        pass

    def process_edge_selection_request(
        self, request: SelectionRequest, current_task: TaskInfo, fl_ctx: FLContext
    ) -> Optional[SelectionResponse]:
        pass
