# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
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

import json
import os
import shutil
import tempfile

from nvflare.fuel.f3.cellnet.cell import Cell
from nvflare.fuel.f3.mpm import MainProcessMonitor as mpm
from nvflare.fuel.utils.dict_utils import augment
from nvflare.fuel.utils.network_utils import get_open_ports
from nvflare.private.fed.app.utils import create_admin_server
from nvflare.private.fed.simulator.simulator_client_engine import SimulatorParentClientEngine
from nvflare.private.fed.simulator.simulator_server import SimulatorServer
from nvflare.security.logging import secure_format_exception

from .base_client_deployer import BaseClientDeployer
from .server_deployer import ServerDeployer


class SimulatorDeployer(ServerDeployer):
    def __init__(self):
        super().__init__()
        self.open_ports = get_open_ports(2)
        self.admin_storage = tempfile.mkdtemp()

    def create_fl_server(self, args, secure_train=False):
        pass

    def create_fl_client(self, client_name, args):
        pass

    def _create_client_cell(self, client_config, client_name, federated_client):
        pass

    def _create_simulator_server_config(self, admin_storage, max_clients):
        pass

    def _create_simulator_client_config(self, client_name, args):
        pass

    def close(self):
        pass
