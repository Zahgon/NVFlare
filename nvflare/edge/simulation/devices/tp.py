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
import copy

from nvflare.edge.constants import EdgeApiStatus
from nvflare.edge.simulation.config import ConfigParser
from nvflare.edge.simulation.device_task_processor import DeviceTaskProcessor
from nvflare.edge.simulation.simulated_device import DeviceFactory, SimulatedDevice
from nvflare.edge.web.models.device_info import DeviceInfo
from nvflare.edge.web.models.job_response import JobResponse
from nvflare.edge.web.models.task_response import TaskResponse
from nvflare.edge.web.models.user_info import UserInfo
from nvflare.fuel.utils.log_utils import get_obj_logger


class TaskProcessingDevice(SimulatedDevice):

    def __init__(
        self,
        device_id: str,
        endpoint_url: str,
        device_info: DeviceInfo,
        user_info: UserInfo,
        processor: DeviceTaskProcessor,
    ):
        SimulatedDevice.__init__(self, device_id)
        self.endpoint_url = endpoint_url
        self.device_info = device_info
        self.user_info = user_info
        self.processor = processor
        processor.device = self

    def get_device_info(self):
        pass

    def get_user_info(self):
        pass

    def set_job(
        self,
        job_id: str,
        job_name: str,
        method: str,
        job_data: dict,
    ):
        pass

    def shutdown(self):
        pass

    def do_task(self, task: TaskResponse) -> dict:
        pass


class TPDeviceFactory(DeviceFactory):

    def __init__(self, parser: ConfigParser):
        self.logger = get_obj_logger(self)
        self.parser = parser
        self.endpoint_url = parser.get_endpoint()

    def make_device(self, device_id: str) -> SimulatedDevice:
        pass


class TPODeviceFactory(DeviceFactory):

    def __init__(self, tpo: DeviceTaskProcessor):
        self.logger = get_obj_logger(self)
        self.tpo = tpo

    def make_device(self, device_id: str) -> SimulatedDevice:
        pass
