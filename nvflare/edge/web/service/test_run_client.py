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

from nvflare.edge.web.models.capabilities import Capabilities
from nvflare.edge.web.models.device_info import DeviceInfo
from nvflare.edge.web.models.job_request import JobRequest
from nvflare.edge.web.models.user_info import UserInfo
from nvflare.edge.web.service.client import EdgeApiClient, Reply
from nvflare.edge.web.service.utils import grpc_reply_to_job_response, job_request_to_grpc_request


class ReqInfo:

    def __init__(self, idx):
        self.idx = idx
        self.send_time = None
        self.rcv_time = None


def request_job(req: ReqInfo, client: EdgeApiClient, addr):
    pass


def main():
    pass


if __name__ == "__main__":
    main()
