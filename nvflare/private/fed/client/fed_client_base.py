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
from typing import List, Optional

from nvflare.apis.filter import Filter
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import ConnPropKey, FLContextKey, SecureTrainConst, ServerCommandKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.fl_exception import FLCommunicationError
from nvflare.apis.overseer_spec import SP
from nvflare.apis.shareable import ReservedHeaderKey, Shareable
from nvflare.apis.signal import Signal
from nvflare.fuel.data_event.utils import get_scope_property, set_scope_property
from nvflare.fuel.f3.cellnet.cell import Cell
from nvflare.fuel.f3.cellnet.fqcn import FQCN
from nvflare.fuel.f3.cellnet.net_agent import NetAgent
from nvflare.fuel.f3.drivers.driver_params import DriverParams
from nvflare.fuel.f3.mpm import MainProcessMonitor as mpm
from nvflare.fuel.utils.argument_utils import parse_vars
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.security.logging import secure_format_exception

from .client_status import ClientStatus
from .communicator import Communicator


class FederatedClientBase:
    """The client-side base implementation of federated learning.

    This class provide the tools function which will be used in both FedClient and FedClientLite.
    """

    def __init__(
        self,
        client_name,
        client_args,
        secure_train,
        server_args=None,
        retry_timeout=30,
        client_state_processors: Optional[List[Filter]] = None,
        handlers: Optional[List[FLComponent]] = None,
        compression=None,
        overseer_agent=None,
        args=None,
        components=None,
        cell: Cell = None,
    ):
        """To init FederatedClientBase.

        Args:
            client_name: client name
            client_args: client config args
            secure_train: True/False to indicate secure train
            server_args: server config args
            retry_timeout: retry timeout
            client_state_processors: client state processor filters
            handlers: handlers
            compression: communication compression algorithm
            cell: CellNet communicator
        """
        self.logger = get_obj_logger(self)

        self.client_name = client_name
        self.token = None
        self.token_signature = None
        self.ssid = None
        self.client_args = client_args
        self.servers = server_args
        self.cell = cell
        self.net_agent = None
        self.args = args
        self.engine_create_timeout = client_args.get("engine_create_timeout", 30.0)
        self.cell_check_frequency = client_args.get("cell_check_frequency", 0.005)
        client_args["client_name"] = client_name

        self.communicator = Communicator(
            client_config=client_args,
            secure_train=secure_train,
            client_state_processors=client_state_processors,
            compression=compression,
            cell=cell,
            client_register_interval=client_args.get("client_register_interval", 2.0),
            timeout=client_args.get("communication_timeout", 300.0),
            maint_msg_timeout=client_args.get("maint_msg_timeout", 30.0),
        )

        self.secure_train = secure_train
        self.handlers = handlers
        self.components = components

        self.heartbeat_done = False
        self.fl_ctx = FLContext()
        self.platform = None
        self.abort_signal = Signal()
        self.engine = None
        self.client_runner = None

        self.status = ClientStatus.NOT_STARTED
        self.remote_tasks = None

        self.sp_established = False
        self.overseer_agent = overseer_agent

        self.overseer_agent = self._init_agent(args)

        if secure_train:
            if self.overseer_agent:
                self.overseer_agent.set_secure_context(
                    ca_path=client_args["ssl_root_cert"],
                    cert_path=client_args["ssl_cert"],
                    prv_key_path=client_args["ssl_private_key"],
                )

    def start_overseer_agent(self):
        pass

    def _init_agent(self, args=None):
        pass

    def overseer_callback(self, overseer_agent):
        pass

    def set_sp(self, project_name, sp: SP):
        pass

    def _create_cell(self, location, scheme):
        """Create my cell.

        Args:
            location: the location of the Server
            scheme: communication protocol (grpc, http, tcp, etc).

        Returns: None

        Note that the client can be connected to the server either directly or via bridge nodes.
        The client's FQCN is different, depending on how the connection is made.

        """
        pass

    def _switch_ssid(self):
        pass

    def client_register(self, project_name, fl_ctx: FLContext):
        """Register the client to the FL server.

        Args:
            project_name: FL study project name.
            fl_ctx: FLContext

        """
        pass

    def fetch_execute_task(self, project_name, fl_ctx: FLContext, timeout=None):
        """Fetch a task from the server.

        Args:
            project_name: FL study project name
            fl_ctx: FLContext
            timeout: timeout for the getTask message sent tp server

        Returns:
            A CurrentTask message from server
        """
        pass

    def push_execute_result(self, project_name, shareable: Shareable, fl_ctx: FLContext, timeout=None):
        """Submit execution results of a task to server.

        Args:
            project_name: FL study project name
            shareable: Shareable object
            fl_ctx: FLContext
            timeout: how long to wait for reply from server

        Returns:
            A FederatedSummary message from the server.
        """
        pass

    def send_heartbeat(self, project_name, interval):
        pass

    def quit_remote(self, project_name, fl_ctx: FLContext):
        """Sending the last message to the server before leaving.

        Args:
            fl_ctx: FLContext

        Returns: N/A

        """
        pass

    def _get_project_name(self):
        """Get name of the project that the site is part of.

        Returns:

        """
        pass

    def heartbeat(self, interval):
        """Sends a heartbeat from the client to the server."""
        pass

    def pull_task(self, fl_ctx: FLContext, timeout=None):
        """Fetch remote models and update the local client's session."""
        pass

    def push_results(self, shareable: Shareable, fl_ctx: FLContext, timeout=None):
        """Push the local model to multiple servers."""
        pass

    def register(self, fl_ctx: FLContext):
        """Register the client with the server."""
        pass

    def set_primary_sp(self, sp):
        pass

    def run_heartbeat(self, interval):
        """Periodically runs the heartbeat."""
        pass

    def start_heartbeat(self, interval=30):
        pass

    def logout_client(self, fl_ctx: FLContext):
        """Logout the client from the server.

        Args:
            fl_ctx: FLContext

        Returns: N/A

        """
        pass

    def set_client_engine(self, engine):
        pass

    def set_client_runner(self, client_runner):
        pass

    def stop_cell(self):
        """Stop the cell communication"""
        pass

    def close(self):
        """Quit the remote federated server, close the local session."""
        pass

    def terminate(self):
        """Terminating the local client session."""
        pass
