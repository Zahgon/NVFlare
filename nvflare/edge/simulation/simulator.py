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
import uuid
from concurrent.futures import ThreadPoolExecutor

from nvflare.edge.constants import CookieKey, EdgeApiStatus, SpecialDeviceId
from nvflare.edge.simulation.simulated_device import DeviceFactory, DeviceState, SimulatedDevice
from nvflare.edge.web.models.job_request import JobRequest
from nvflare.edge.web.models.job_response import JobResponse
from nvflare.edge.web.models.result_report import ResultReport
from nvflare.edge.web.models.result_response import ResultResponse
from nvflare.edge.web.models.selection_request import SelectionRequest
from nvflare.edge.web.models.selection_response import SelectionResponse
from nvflare.edge.web.models.task_request import TaskRequest
from nvflare.edge.web.models.task_response import TaskResponse
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.security.logging import secure_format_exception


class Simulator:

    def __init__(
        self,
        job_name: str,
        device_factory: DeviceFactory,
        num_devices: int = 10000,
        num_workers: int = 10,
        get_job_timeout: float = 60.0,
    ):
        """Constructor of Simulator.

        Args:
            device_factory: object for creating new devices
            num_devices: max number of devices to be created
            num_workers: number of threads for doing tasks
        """
        self.job_name = job_name
        self.device_factory = device_factory
        self.num_devices = num_devices
        self.num_workers = num_workers
        self.get_job_timeout = get_job_timeout
        self.send_f = None
        self.send_kwargs = None

        self.done = False

        # devices that are currently busy doing task
        self.busy_devices = {}  # device_id => selection id

        # devices that have finished tasks
        self.used_devices = {}  # device_id => selection id

        # all created devices
        self.all_devices = {}  # device_id => SimulatedDevice

        # thread pool for doing tasks
        self.worker_pool = ThreadPoolExecutor(num_workers)

        self.logger = get_obj_logger(self)
        self.update_lock = threading.Lock()
        self.device_id_prefix = str(uuid.uuid4())

    def set_send_func(self, send_f, **kwargs):
        """Set the function for sending request to Flare

        Args:
            send_f: the function to be set
            **kwargs: args to be passed to the function when invoked

        Returns: None

        """
        pass

    def _determine_my_devices(self, selected_devices: dict):
        """Determines active devices for the next cycle.

        Args:
            selected_devices: the devices that have been selected for task

        Returns: a dict of devices for next query cycle

        """
        pass

    def _control_flow(self):
        pass

    def start(self):
        pass

    def stop(self):
        """Stop the simulator.

        Returns: None

        """
        pass

    def _send_request(self, req, device, default_resp, **kwargs):
        pass

    def _ask_for_task(self, device: SimulatedDevice) -> TaskResponse:
        """Send a request to Flare to ask for a task for a device

        Args:
            device: the device that the request is for

        Returns: TaskResponse

        """
        pass

    def _ask_for_selection(self, job_id: str, device_id) -> SelectionResponse:
        """Send a request to Flare for ask for the current device selection.
        Note: this is used for simulation purpose. Real devices don't make this request.

        Returns: SelectionResponse

        """
        pass

    def _ask_for_job(self, device: SimulatedDevice) -> JobResponse:
        """Send a request to Flare to ask for a Job for the specified device

        Args:
            device: the device that the request is for.

        Returns:

        """
        pass

    def _make_new_device(self, device_id: str):
        """Create a new device for inclusion to active device list.

        Returns: a device

        """
        pass

    def _do_learn(self, task_data: TaskResponse, device: SimulatedDevice, selection_id):
        """Do the task.

        Args:
            task_data: task data
            device: device to do the task
            selection_id: selection id of the device

        Returns:

        """
        pass
