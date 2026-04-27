# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
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
from abc import ABC, abstractmethod
from threading import Lock
from typing import Dict, List, Optional

from nvflare.apis.client import Client
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import (
    ConfigVarName,
    ConnPropKey,
    FLContextKey,
    MachineStatus,
    RunProcessKey,
    SecureTrainConst,
    ServerCommandKey,
    ServerCommandNames,
    SiteType,
    SystemComponents,
    SystemConfigs,
)
from nvflare.apis.fl_context import FLContext
from nvflare.apis.fl_exception import NotAuthenticated
from nvflare.apis.job_def import JobMetaKey, RunStatus
from nvflare.apis.shareable import Shareable
from nvflare.apis.workspace import Workspace
from nvflare.fuel.common.exit_codes import ProcessExitCode
from nvflare.fuel.f3.cellnet.cell import Cell
from nvflare.fuel.f3.cellnet.core_cell import Message
from nvflare.fuel.f3.cellnet.core_cell import make_reply as make_cellnet_reply
from nvflare.fuel.f3.cellnet.defs import IdentityChallengeKey, MessageHeaderKey
from nvflare.fuel.f3.cellnet.defs import ReturnCode as F3ReturnCode
from nvflare.fuel.f3.cellnet.fqcn import FQCN
from nvflare.fuel.f3.cellnet.net_agent import NetAgent
from nvflare.fuel.f3.drivers.driver_params import DriverParams
from nvflare.fuel.f3.mpm import MainProcessMonitor as mpm
from nvflare.fuel.sec.authn import add_authentication_headers
from nvflare.fuel.utils.argument_utils import parse_vars
from nvflare.fuel.utils.config_service import ConfigService
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.private.defs import (
    CellChannel,
    CellChannelTopic,
    CellMessageHeaderKeys,
    ClientRegSession,
    ClientType,
    InternalFLContextKey,
    JobFailureMsgKey,
    new_cell_message,
)
from nvflare.private.fed.authenticator import validate_auth_headers
from nvflare.private.fed.server.cred_keeper import CredKeeper
from nvflare.private.fed.server.server_command_agent import ServerCommandAgent
from nvflare.private.fed.server.server_runner import ServerRunner
from nvflare.private.fed.utils.identity_utils import TokenVerifier
from nvflare.security.logging import secure_format_exception
from nvflare.widgets.fed_event import ServerFedEventRunner

from .client_manager import ClientManager
from .run_manager import RunManager
from .server_engine import ServerEngine
from .server_state import (
    ABORT_RUN,
    ACTION,
    MESSAGE,
    NIS,
    Cold2HotState,
    ColdState,
    Hot2ColdState,
    HotState,
    ServerState,
)
from .server_status import ServerStatus


class BaseServer(ABC):
    def __init__(
        self,
        project_name=None,
        min_num_clients=2,
        max_num_clients=10,
        heart_beat_timeout=600,
        handlers: Optional[List[FLComponent]] = None,
        shutdown_period=30.0,
    ):
        """Base server that provides the clients management and server deployment."""
        self.project_name = project_name
        self.min_num_clients = max(min_num_clients, 1)
        self.max_num_clients = max(max_num_clients, 1)

        self.heart_beat_timeout = heart_beat_timeout
        self.handlers = handlers

        self.client_manager = ClientManager(
            project_name=self.project_name, min_num_clients=self.min_num_clients, max_num_clients=self.max_num_clients
        )

        self.cell = None
        self.admin_server = None
        self.lock = Lock()
        self.snapshot_lock = Lock()
        self.fl_ctx = FLContext()
        self.platform = None
        self.shutdown_period = shutdown_period

        self.shutdown = False
        self.status = ServerStatus.NOT_STARTED

        self.abort_signal = None
        self.executor = None

        self.logger = get_obj_logger(self)

    def get_all_clients(self) -> Dict[str, Client]:
        """Get the list of registered clients.

        Returns:
            A dict of {client_token: client}
        """
        pass

    def get_cell(self):
        pass

    @abstractmethod
    def remove_client_data(self, token):
        pass

    def close(self):
        """Shutdown the server."""
        pass

    def deploy(self, args, grpc_args=None, secure_train=False):
        """Start a grpc server and listening the designated port."""
        pass

    def client_cleanup(self):
        pass

    def set_admin_server(self, admin_server):
        pass

    def remove_dead_clients(self):
        # Clean and remove the dead client without heartbeat.
        pass

    def logout_client(self, token):
        pass

    def notify_dead_client(self, client):
        """Called to do further processing of the dead client

        Args:
            client: the dead client

        Returns:

        """
        pass

    def fl_shutdown(self):
        pass


class FederatedServer(BaseServer):
    def __init__(
        self,
        project_name=None,
        min_num_clients=2,
        max_num_clients=10,
        cmd_modules=None,
        heart_beat_timeout=600,
        handlers: Optional[List[FLComponent]] = None,
        args=None,
        secure_train=False,
        snapshot_persistor=None,
        overseer_agent=None,
        shutdown_period=30.0,
        check_engine_frequency=3.0,
    ):
        """Federated server services.

        Args:
            project_name: server project name.
            min_num_clients: minimum number of contributors at each round.
            max_num_clients: maximum number of contributors at each round.
            cmd_modules: command modules.
            heart_beat_timeout: heartbeat timeout
            handlers: A list of handler
            args: arguments
            secure_train: whether to use secure communication
        """
        BaseServer.__init__(
            self,
            project_name=project_name,
            min_num_clients=min_num_clients,
            max_num_clients=max_num_clients,
            heart_beat_timeout=heart_beat_timeout,
            handlers=handlers,
            shutdown_period=shutdown_period,
        )

        self.contributed_clients = {}
        self.tokens = None
        self.round_started = time.time()

        with self.lock:
            self.reset_tokens()

        self.cmd_modules = cmd_modules

        self.builder = None

        self.engine = self._create_server_engine(args, snapshot_persistor)
        self.run_manager = None
        self.server_runner = None
        self.command_agent = None
        self.check_engine_frequency = check_engine_frequency

        self.processors = {}
        self.runner_config = None
        self.secure_train = secure_train

        self.workspace = args.workspace
        self.snapshot_location = None
        self.overseer_agent = overseer_agent
        self.server_state: ServerState = ColdState()
        self.snapshot_persistor = snapshot_persistor
        self.checking_server_state = False
        self.ha_mode = False

        self.reg_lock = threading.Lock()
        self.name_to_reg = {}
        self.cred_keeper = CredKeeper()

        # Tracks per-job which client tokens have been positively observed running the job.
        # Keyed by job_id -> set of client tokens.  Used by _sync_client_jobs() to require
        # a prior positive heartbeat before classifying a client's missing job as "dead".
        # Entries are cleaned up as soon as the job is no longer in run_processes.
        self._job_reported_clients: Dict[str, set] = {}
        self._job_reported_clients_lock = threading.Lock()

        # these are used when the server sends a message to itself.
        self.my_own_auth_client_name = "server"
        self.my_own_token = "server"
        self.my_own_token_signature = None

    def _register_cellnet_cbs(self):
        pass

    def _add_auth_headers(self, message: Message):
        """Add auth headers to the messages sent by the server to itself.
        This is such that no one can fake a message to pretend it's from the server to the server.
        Args:
            message: the message for which to add the headers
        Returns: None
        """
        pass

    def _validate_auth_headers(self, message: Message):
        """Validate auth headers from messages that go through the server.
        Args:
            message: the message to validate
        Returns:
        """
        pass

    def sign_auth_token(self, client_name: str, token: str):
        pass

    def verify_auth_token(self, client_name: str, token: str, signature):
        pass

    def _check_regs(self):
        pass

    def _listen_command(self, request: Message) -> Message:
        pass

    def _set_job_aborted(self, job_id):
        pass

    def _create_server_engine(self, args, snapshot_persistor):
        pass

    def create_job_cell(self, job_id, root_url, parent_url, secure_train, server_config) -> Cell:
        pass

    # @property
    def task_meta_info(self, client_name):
        """Task meta information.

        The model_meta_info uniquely defines the current model,
        it is used to reject outdated client's update.
        """
        pass

    def remove_client_data(self, token):
        pass

    def reset_tokens(self):
        """Reset the token set.

        After resetting, each client can take a token
        and start fetching the current global model.
        This function is not thread-safe.
        """
        pass

    def _before_service(self, fl_ctx: FLContext):
        # before the service processing
        pass

    def _generate_reply(self, headers, payload, fl_ctx: FLContext):
        # process after the service processing
        pass

    def _get_id_asserter(self):
        pass

    def _ready_for_registration(self, fl_ctx: FLContext):
        pass

    def client_challenge(self, request: Message) -> Message:
        pass

    def register_client(self, request: Message) -> Message:
        """Register a new client.
        Each client must be registered before being able to run jobs.
        """
        pass

    def _handle_state_check(self, state_check, fl_ctx: FLContext):
        pass

    def quit_client(self, request: Message) -> Message:
        """Existing client quits the federated training process.

        Server will stop sharing the global model with the client,
        further contribution will be rejected.

        This function does not change min_num_clients and max_num_clients.
        """
        pass

    def process_job_failure(self, request: Message):
        pass

    def client_heartbeat(self, request: Message) -> Message:

        pass

    def _sync_client_jobs(self, request, client_token):
        # jobs that are running on client but not on server need to be aborted!
        pass

    def _notify_dead_job(self, client, job_id: str, reason: str):
        pass

    def notify_dead_client(self, client):
        """Called to do further processing of the dead client

        Args:
            client: the dead client

        Returns:

        """
        pass

    def start_run(self, job_id, run_root, conf, args, snapshot):
        # Create the FL Engine
        pass

    def _send_parent_heartbeat(self, job_id):
        pass

    def create_run_manager(self, workspace, job_id):
        pass

    def authentication_check(self, request: Message, state_check):
        pass

    def abort_run(self):
        pass

    def run_engine(self):
        pass

    def stop_run_engine_cell(self):
        # self.cell.stop()
        # mpm.stop()
        pass

    def deploy(self, args, grpc_args=None, secure_train=False):
        pass

    def _init_agent(self, args=None):
        pass

    def _check_server_state(self, overseer_agent):
        pass

    def _notify_state_change(self, old_state_name):
        pass

    def overseer_callback(self, overseer_agent):
        pass

    def _turn_to_hot(self):
        # Restore Snapshot
        pass

    def _turn_to_cold(self, old_state_name):
        pass

    def stop_training(self):
        pass

    def fl_shutdown(self):
        pass

    def close(self):
        """Shutdown the server."""
        pass
