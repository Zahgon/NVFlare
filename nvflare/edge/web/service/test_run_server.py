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
import logging
import threading
import time
import uuid

from nvflare.edge.constants import CookieKey, EdgeApiStatus
from nvflare.edge.web.models.job_request import JobRequest
from nvflare.edge.web.models.job_response import JobResponse
from nvflare.edge.web.models.result_report import ResultReport
from nvflare.edge.web.models.result_response import ResultResponse
from nvflare.edge.web.models.selection_request import SelectionRequest
from nvflare.edge.web.models.selection_response import SelectionResponse
from nvflare.edge.web.models.task_request import TaskRequest
from nvflare.edge.web.models.task_response import TaskResponse
from nvflare.edge.web.service.query_handler import QueryHandler
from nvflare.edge.web.service.server import EdgeApiServer
from nvflare.fuel.utils.log_utils import get_obj_logger


class TestQueryHandler(QueryHandler):

    def __init__(self):
        QueryHandler.__init__(self)
        self.logger = get_obj_logger(self)

    def handle_job_request(self, request: JobRequest) -> JobResponse:
        pass

    def handle_task_request(self, request: TaskRequest) -> TaskResponse:
        pass

    def handle_result_report(self, request: ResultReport) -> ResultResponse:
        pass

    def handle_selection_request(self, request: SelectionRequest) -> SelectionResponse:
        pass


def shutdown_server(server):
    pass


def main():
    pass


if __name__ == "__main__":
    main()
