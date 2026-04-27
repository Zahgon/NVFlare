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

import argparse
import os
import sys
import threading
import time
from multiprocessing.connection import Listener

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import FLContextKey, RunnerTask, WorkspaceConstants
from nvflare.apis.workspace import Workspace
from nvflare.fuel.common.multi_process_executor_constants import CommunicationMetaData
from nvflare.fuel.f3.cellnet.cell import Cell
from nvflare.fuel.f3.cellnet.fqcn import FQCN
from nvflare.fuel.f3.mpm import MainProcessMonitor as mpm
from nvflare.fuel.hci.server.authz import AuthorizationService
from nvflare.fuel.sec.audit import AuditService
from nvflare.fuel.utils.log_utils import dynamic_log_config
from nvflare.private.fed.app.deployer.base_client_deployer import BaseClientDeployer
from nvflare.private.fed.app.utils import check_parent_alive, init_security_content_service
from nvflare.private.fed.client.client_engine import ClientEngine
from nvflare.private.fed.client.client_status import ClientStatus
from nvflare.private.fed.client.fed_client import FederatedClient
from nvflare.private.fed.simulator.simulator_app_runner import SimulatorClientAppRunner
from nvflare.private.fed.simulator.simulator_audit import SimulatorAuditor
from nvflare.private.fed.simulator.simulator_const import SimulatorConstants
from nvflare.private.fed.utils.fed_utils import fobs_initialize, get_simulator_app_root, register_ext_decomposers
from nvflare.security.logging import secure_format_exception, secure_log_traceback
from nvflare.security.security import EmptyAuthorizer

CELL_CONNECT_CHECK_TIMEOUT = 10.0
FETCH_TASK_RUN_RETRY = 3


class ClientTaskWorker(FLComponent):
    def create_client_engine(self, federated_client: FederatedClient, args, rank=0):
        pass

    def create_client_runner(self, client):
        """Create the ClientRunner for the client to run the ClientApp.

        Args:
            client: the client to run

        """
        pass

    def do_one_task(self, client, args):
        pass

    def release_resources(self, client):
        pass

    def run(self, args, conn):
        pass

    def _create_client(self, args, build_ctx, deploy_args):
        pass

    def _set_client_status(self, client, deploy_args, simulator_root):
        pass

    def _create_client_cell(self, federated_client, root_url, parent_url):
        pass


def _create_connection(listen_port):
    pass


def main(args):

    # start parent process checking thread
    pass


def parse_arguments():
    pass


if __name__ == "__main__":
    """
    This is the main program of simulator worker process when running the NVFlare Simulator..
    """

    # main()
    args = parse_arguments()
    mpm.run(main_func=main, run_dir=args.workspace, args=args)
    time.sleep(2)
    # os._exit(0)
