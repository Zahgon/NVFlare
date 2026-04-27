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

"""FL Server deployer."""
import threading

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import FLContextKey, ReservedKey, SiteType, SystemComponents
from nvflare.apis.signal import Signal
from nvflare.apis.workspace import Workspace
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.private.fed.app.utils import component_security_check
from nvflare.private.fed.server.fed_server import FederatedServer
from nvflare.private.fed.server.job_runner import JobRunner
from nvflare.private.fed.server.run_manager import RunManager
from nvflare.private.fed.server.server_cmd_modules import ServerCommandModules
from nvflare.private.fed.server.server_status import ServerStatus
from nvflare.widgets.fed_event import ServerFedEventRunner


class ServerDeployer:
    """FL Server deployer."""

    def __init__(self):
        """Init the ServerDeployer."""
        self.cmd_modules = ServerCommandModules.cmd_modules
        self.logger = get_obj_logger(self)
        self.server_config = None
        self.secure_train = None
        self.app_validator = None
        self.host = None
        self.snapshot_persistor = None
        self.overseer_agent = None
        self.components = None
        self.handlers = None

    def build(self, build_ctx):
        """To build the ServerDeployer.

        Args:
            build_ctx: build context

        """
        pass

    def create_fl_server(self, args, secure_train=False):
        """To create the FL Server.

        Args:
            args: command args
            secure_train: True/False

        Returns: FL Server

        """
        pass

    def deploy(self, args):
        """To deploy the FL server services.

        Args:
            args: command args.

        Returns: FL Server

        """
        pass

    def _start_job_runner(self, job_runner, fl_ctx):
        pass

    def close(self):
        """To close the services."""
        pass
