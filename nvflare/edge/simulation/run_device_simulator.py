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
import argparse
import logging

from nvflare.edge.simulation.config import ConfigParser
from nvflare.edge.simulation.devices.tp import TPDeviceFactory
from nvflare.edge.simulation.feg_api import FegApi
from nvflare.edge.simulation.simulated_device import SimulatedDevice
from nvflare.edge.simulation.simulator import Simulator
from nvflare.edge.web.models.job_request import JobRequest
from nvflare.edge.web.models.result_report import ResultReport
from nvflare.edge.web.models.selection_request import SelectionRequest
from nvflare.edge.web.models.task_request import TaskRequest
from nvflare.edge.web.service.query import Query

log = logging.getLogger(__name__)


def run_simulator(config_file: str, lcp_mapping_file: str = None, ca_cert_file: str = None):
    pass


def _send_request_to_lcp(request, device: SimulatedDevice, query: Query):
    pass


def _send_request_to_proxy(request, device: SimulatedDevice, parser: ConfigParser):
    pass


def main():
    # Set up logging
    pass


if __name__ == "__main__":
    main()
