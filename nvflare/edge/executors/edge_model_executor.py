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
import threading
import time
from typing import Optional

from nvflare.apis.dxo import DXO, from_dict
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReservedHeaderKey
from nvflare.edge.constants import CookieKey, EdgeApiStatus, MsgKey, SpecialDeviceId
from nvflare.edge.executors.ete import EdgeTaskExecutor
from nvflare.edge.executors.hug import TaskInfo
from nvflare.edge.mud import BaseState, Device, ModelUpdate, StateUpdateReport
from nvflare.edge.updaters.emd import AggregatorFactory, EdgeModelUpdater
from nvflare.edge.web.models.result_report import ResultReport
from nvflare.edge.web.models.result_response import ResultResponse
from nvflare.edge.web.models.selection_request import SelectionRequest
from nvflare.edge.web.models.selection_response import SelectionResponse
from nvflare.edge.web.models.task_request import TaskRequest
from nvflare.edge.web.models.task_response import TaskResponse
from nvflare.security.logging import secure_format_exception


class EdgeModelExecutor(EdgeTaskExecutor):

    def __init__(
        self,
        aggr_factory_id: str,
        max_model_versions: Optional[int] = None,
        update_timeout=60.0,
    ):
        EdgeTaskExecutor.__init__(self, "", update_timeout)
        self.aggr_factory_id = aggr_factory_id
        self.max_model_versions = max_model_versions

        self.cvt_lock = threading.Lock()

    def get_updater(self, fl_ctx: FLContext):
        pass

    def _convert_task(self, task_state: BaseState, current_task: TaskInfo, fl_ctx: FLContext) -> dict:
        """Convert task_data to a plain dict"""
        pass

    def _convert_device_result_to_model_update(
        self, result_report: ResultReport, current_task: TaskInfo, fl_ctx: FLContext
    ) -> Optional[ModelUpdate]:
        pass

    def accept_alive_device(self, device_id: str, fl_ctx: FLContext):
        pass

    def accept_device_result(self, result_report: ResultReport, current_task: TaskInfo, fl_ctx: FLContext):
        pass

    @staticmethod
    def _make_retry(job_id, msg: str):
        pass

    @staticmethod
    def _make_cookie(model_version, device_selection_id):
        pass

    def process_edge_selection_request(
        self, request: SelectionRequest, current_task: TaskInfo, fl_ctx: FLContext
    ) -> SelectionResponse:
        """Handle selection request from device"""
        pass

    def process_edge_task_request(
        self, request: TaskRequest, current_task: TaskInfo, fl_ctx: FLContext
    ) -> TaskResponse:
        """Handle task request from device"""
        pass

    def process_edge_result_report(
        self, request: ResultReport, current_task: TaskInfo, fl_ctx: FLContext
    ) -> ResultResponse:
        """Handle result report from device
        The report task_id may be different from current task_id. Let HAM deal with it
        """
        pass

    def task_started(self, task: TaskInfo, fl_ctx: FLContext):
        pass

    def task_ended(self, task: TaskInfo, fl_ctx: FLContext):
        pass
