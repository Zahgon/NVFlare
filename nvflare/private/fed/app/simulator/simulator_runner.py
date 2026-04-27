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
import copy
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from argparse import Namespace
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Manager, Process
from multiprocessing.connection import Client
from urllib.parse import urlparse

from nvflare.apis.client import Client as FLClient
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import (
    ConfigVarName,
    FLMetaKey,
    JobConstants,
    MachineStatus,
    RunnerTask,
    RunProcessKey,
    SiteType,
    SystemConfigs,
    SystemVarName,
    WorkspaceConstants,
)
from nvflare.apis.job_def import ALL_SITES, JobMetaKey
from nvflare.apis.utils.job_utils import convert_legacy_zipped_app_to_job
from nvflare.apis.workspace import Workspace
from nvflare.fuel.common.exit_codes import ProcessExitCode
from nvflare.fuel.common.multi_process_executor_constants import CommunicationMetaData
from nvflare.fuel.f3.mpm import MainProcessMonitor as mpm
from nvflare.fuel.f3.stats_pool import StatsPoolManager
from nvflare.fuel.hci.server.authz import AuthorizationService
from nvflare.fuel.sec.audit import AuditService
from nvflare.fuel.utils import log_utils
from nvflare.fuel.utils.argument_utils import parse_vars
from nvflare.fuel.utils.config_service import ConfigService
from nvflare.fuel.utils.gpu_utils import get_host_gpu_ids
from nvflare.fuel.utils.log_utils import FL_LOG_LEVEL, dynamic_log_config
from nvflare.fuel.utils.network_utils import get_open_ports
from nvflare.fuel.utils.zip_utils import split_path, unzip_all_from_bytes, zip_directory_to_bytes
from nvflare.private.defs import AppFolderConstants
from nvflare.private.fed.app.deployer.simulator_deployer import SimulatorDeployer
from nvflare.private.fed.app.utils import init_security_content_service, kill_child_processes
from nvflare.private.fed.client.client_status import ClientStatus
from nvflare.private.fed.server.job_meta_validator import JobMetaValidator
from nvflare.private.fed.simulator.simulator_app_runner import SimulatorServerAppRunner
from nvflare.private.fed.simulator.simulator_audit import SimulatorAuditor
from nvflare.private.fed.simulator.simulator_const import SimulatorConstants
from nvflare.private.fed.utils.fed_utils import (
    custom_fobs_initialize,
    get_simulator_app_root,
    nvflare_fobs_initialize,
    register_ext_decomposers,
    split_gpus,
)
from nvflare.security.logging import secure_format_exception, secure_log_traceback
from nvflare.security.security import EmptyAuthorizer
from nvflare.utils.job_launcher_utils import add_custom_dir_to_path

CLIENT_CREATE_POOL_SIZE = 200
POOL_STATS_DIR = "pool_stats"
SIMULATOR_POOL_STATS = "simulator_cell_stats.json"


class SimulatorRunner(FLComponent):
    def __init__(
        self,
        job_folder: str,
        workspace: str,
        clients=None,
        n_clients=None,
        threads=None,
        gpu=None,
        log_config=None,
        max_clients=100,
        end_run_for_all=False,
    ):
        super().__init__()

        self.job_folder = job_folder
        self.workspace = workspace
        self.clients = clients
        self.n_clients = n_clients
        self.threads = threads
        self.gpu = gpu
        self.log_config = None
        self.max_clients = max_clients
        self.end_run_for_all = end_run_for_all

        self.ask_to_stop = False

        self.simulator_root = None
        self.server = None
        self.deployer = SimulatorDeployer()
        self.client_names = []
        self.federated_clients = []
        self.client_config = None
        self.deploy_args = None
        self.build_ctx = None
        self.server_custom_folder = None

        self.clients_created = 0

        running_dir = os.getcwd()
        if self.workspace is None:
            self.workspace = "simulator_workspace"
            self.logger.warning(
                f"Simulator workspace is not provided. Set it to the default location:"
                f" {os.path.join(running_dir, self.workspace)}"
            )
        self.workspace = os.path.join(running_dir, self.workspace)

        if log_config is None:
            log_config = os.environ.get(FL_LOG_LEVEL)
        if log_config:
            log_config_path = os.path.join(running_dir, log_config)
            self.log_config = log_config_path if os.path.isfile(log_config_path) else log_config

    def _generate_args(
        self,
        job_folder: str,
        workspace: str,
        clients=None,
        n_clients=None,
        threads=None,
        gpu=None,
        log_config=None,
        max_clients=100,
    ):
        pass

    def setup(self):
        pass

    def _cleanup_workspace(self):
        pass

    def _setup_local_startup(self, log_config_file_path, workspace):
        pass

    def validate_job_data(self):
        # Validate the simulate job
        pass

    def _extract_client_names_from_meta(self, meta):
        pass

    def _validate_client_names(self, meta, client_names):
        pass

    def _deploy_apps(self, job_name, data_bytes, meta, log_config_file_path):
        pass

    def split_clients(self, clients: [], gpus: []):
        pass

    def create_clients(self):
        # Deploy the FL clients
        pass

    def create_client(self, client_name):
        pass

    def _set_client_status(self):
        pass

    def run(self):
        pass

    def _get_return_code(self, return_dict, process, workspace):
        pass

    def run_process(self, return_dict):
        # run_status = self.simulator_run_main()
        pass

    def simulator_run_main(self):
        pass

    def client_run(self, server_custom_folder, clients, gpu):
        pass

    def start_server_app(self, args):
        pass

    def dump_stats(self, workspace: Workspace):
        pass


class SimulatorClientRunner(FLComponent):
    def __init__(self, server_custom_folder, args, clients: [], client_config, deploy_args, build_ctx):
        super().__init__()
        self.server_custom_folder = server_custom_folder
        self.args = args
        self.federated_clients = clients
        self.run_client_index = -1

        self.simulator_root = self.args.workspace
        self.client_config = client_config
        self.deploy_args = deploy_args
        self.build_ctx = build_ctx
        self.kv_list = parse_vars(args.set)
        self.logging_config = os.path.join(self.args.workspace, "local", WorkspaceConstants.LOGGING_CONFIG)

        self.clients_finished_end_run = []

    def run(self, gpu):
        pass

    def _shutdown_client(self, client):
        pass

    def run_client_thread(self, num_of_threads, gpu, lock, end_run_for_all, timeout=60):
        pass

    def _end_run_clients(self, gpu, lock, num_of_threads, timeout):
        """After the WF reaches the END_RUN, each running thread will try to pick up one of the remaining client
        which has not run the END_RUN yet, then execute the END_RUN handler, until all the clients have done so.
        These client END_RUN event handler only execute when "end_run_for_all" has been set.

        Multiple client running threads will try to pick up the client from the same clients pool.

        """
        pass

    def _pick_next_client(self):
        pass

    def do_one_task(self, client, num_of_threads, gpu, lock, timeout=60.0, task_name=RunnerTask.TASK_EXEC):
        pass

    def _cleanup_process(self, process, timeout=5.0):
        """Clean process shutdown - no exceptions escape"""
        pass

    def _get_new_sys_path(self):
        pass

    def _create_connection(self, open_port, timeout=60.0):
        pass

    def get_next_run_client(self, gpu):
        # Find the next client which is not currently running
        pass
