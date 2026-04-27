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
from typing import Union

from flask import Blueprint, request

from nvflare.edge.constants import EdgeApiStatus, HttpHeaderKey
from nvflare.edge.web.models.api_error import ApiError
from nvflare.edge.web.models.base_model import EdgeProtoKey
from nvflare.edge.web.models.device_info import DeviceInfo
from nvflare.edge.web.models.job_request import JobRequest
from nvflare.edge.web.models.result_report import ResultReport
from nvflare.edge.web.models.selection_request import SelectionRequest
from nvflare.edge.web.models.task_request import TaskRequest
from nvflare.edge.web.models.user_info import UserInfo
from nvflare.edge.web.service.query import Query


class APIQuery:

    def __init__(self):
        self.lcp_mapping_file = None
        self.ca_cert_file = None
        self.query = None

    def set_lcp_mapping(self, file_name: str):
        pass

    def set_ca_cert(self, file_name: str):
        pass

    def start(self):
        pass

    def __call__(self, req: Union[TaskRequest, JobRequest, SelectionRequest, ResultReport]):
        return self.query(req)


feg_bp = Blueprint("feg", __name__)
api_query = APIQuery()


def _process_headers() -> dict:
    pass


def _update_body(d: dict):
    pass


def _update_args(d: dict, keys: dict):
    pass


def _do_query(req):
    pass


@feg_bp.route("/job", methods=["POST"])
def job_view():
    pass


@feg_bp.route("/task", methods=["POST"])
def task_view():
    pass


@feg_bp.route("/result", methods=["POST"])
def result_view():
    pass


@feg_bp.route("/selection", methods=["POST"])
def selection_view():
    pass
