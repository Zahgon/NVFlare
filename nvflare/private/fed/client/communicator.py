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

from nvflare.apis.event_type import EventType
from nvflare.apis.filter import Filter
from nvflare.apis.fl_constant import FLContextKey, FLMetaKey, ReservedKey
from nvflare.apis.fl_constant import ReturnCode as ShareableRC
from nvflare.apis.fl_constant import SecureTrainConst, ServerCommandKey, ServerCommandNames
from nvflare.apis.fl_context import FLContext
from nvflare.apis.fl_exception import FLCommunicationError
from nvflare.apis.shareable import ReservedHeaderKey, Shareable, make_copy
from nvflare.apis.signal import Signal
from nvflare.apis.utils.fl_context_utils import gen_new_peer_ctx
from nvflare.fuel.data_event.utils import get_scope_property, set_scope_property
from nvflare.fuel.f3.cellnet.cell import Cell
from nvflare.fuel.f3.cellnet.defs import MessageHeaderKey, ReturnCode
from nvflare.fuel.f3.cellnet.fqcn import FQCN
from nvflare.fuel.f3.cellnet.utils import format_size
from nvflare.fuel.f3.message import Message as CellMessage
from nvflare.fuel.sec.authn import set_add_auth_headers_filters
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.private.defs import (
    CellChannel,
    CellChannelTopic,
    CellMessageHeaderKeys,
    ClientType,
    SpecialTaskName,
    new_cell_message,
)
from nvflare.private.fed.authenticator import Authenticator
from nvflare.private.fed.client.client_engine_internal_spec import ClientEngineInternalSpec
from nvflare.security.logging import secure_format_exception

from .utils import determine_parent_fqcn


class Communicator:
    def __init__(
        self,
        client_config=None,
        secure_train=False,
        client_state_processors: Optional[List[Filter]] = None,
        compression=None,
        cell: Cell = None,
        client_register_interval=2,
        timeout=5.0,
        maint_msg_timeout=5.0,
    ):
        """To init the Communicator.

        Args:
            client_config: client configuration data
            secure_train: True/False to indicate if secure train
            client_state_processors: Client state processor filters
            compression: communicate compression algorithm
        """
        self.cell = cell
        self.client_config = client_config
        self.secure_train = secure_train

        self.verbose = False
        self.heartbeat_done = False
        self.client_state_processors = client_state_processors
        self.compression = compression
        self.client_register_interval = client_register_interval
        self.timeout = timeout
        self.maint_msg_timeout = maint_msg_timeout

        # token and token_signature are issued by the Server after the client is authenticated
        # they are added to every message going to the server as proof of authentication
        self.token = None
        self.token_signature = None
        self.ssid = None
        self.client_name = None
        self.token_verifier = None
        self.abort_signal = Signal()
        self.engine = None
        self.last_task_id = None  # ID of the last task received
        self.pending_task = None  # the task currently being processed
        self.logger = get_obj_logger(self)
        self._state_lock = threading.Lock()
        tmp_ctx = FLContext()
        tmp_ctx.set_prop(
            key=ReservedKey.IDENTITY_NAME,
            value=client_config["client_name"],
            private=False,
            sticky=True,
        )
        self._peer_ctx = tmp_ctx

    """
    To call set_add_auth_headers_filters, both cell and token must be available.
    The set_cell is called when cell becomes available, set_auth is called when token becomes available.
    In CP, set_cell happens before set_auth, hence we call set_add_auth_headers_filters in set_auth for CP.
    In CJ, set_auth happens before set_cell, hence we call set_add_auth_headers_filters in set_cell for CJ.
    """

    def set_auth(self, client_name, token, token_signature, ssid):
        pass

    def set_cell(self, cell):
        pass

    @staticmethod
    def _make_try_again():
        pass

    def _process_get_task(self, request: CellMessage):
        pass

    def _process_submit_result(self, request: CellMessage):
        pass

    def client_registration(self, client_name, project_name, fl_ctx: FLContext):
        """Register the client with the FLARE Server.

        Note that the client no longer needs to be directly connected with the Server!

        Since the client may be connected with the Server indirectly (e.g. via bridge nodes or proxy), in the secure
        mode, the client authentication cannot be based on the connection's TLS cert. Instead, the server and the
        client will explicitly authenticate each other using their provisioned PKI credentials, as follows:

        1. Make sure that the Server is authentic. The client sends a Challenge request with a random nonce.
        The server is expected to return the following in its reply:
            - its cert and common name (Server_CN)
            - signature on the received client nonce + Server_CN
            - a random Server Nonce. This will be used for the server to validate the client's identity in the
            Registration request.

        The client then validates to make sure:
            - the Server_CN is the same as presented in the server cert
            - the Server_CN is the same as configured in the client's config (fed_client.json)
            - the signature is valid

        2. Client sends Registration request that contains:
            - client cert and common name (Client_CN)
            - signature on the received Server Nonce + Client_CN

        The Server then validates to make sure:
            - the Client_CN is the same as presented in the client cert
            - the signature is valid

        NOTE: we do not explicitly validate certs' expiration time. This is because currently the same certs are
        also used for SSL connections, which already validate expiration.

        Args:
            client_name: client name
            project_name: FL study project name
            fl_ctx: FLContext

        Returns:
            The client's token

        """
        pass

    def pull_task(self, project_name, token, ssid, fl_ctx: FLContext, timeout=None):
        """Get a task from server.

        Args:
            project_name: FL study project name
            token: client token
            ssid: service session ID
            fl_ctx: FLContext
            timeout: how long to wait for response from server

        Returns:
            A CurrentTask message from server

        """
        pass

    def submit_update(
        self, project_name, token, ssid, fl_ctx: FLContext, client_name, shareable, execute_task_name, timeout=None
    ):
        """Submit the task execution result back to the server.

        Args:
            project_name: server project name
            token: client token
            ssid: service session ID
            fl_ctx: fl_ctx
            client_name: client name
            shareable: execution task result shareable
            execute_task_name: execution task name
            timeout: how long to wait for response from server

        Returns:
            ReturnCode
        """
        pass

    def quit_remote(self, servers, task_name, token, ssid, fl_ctx: FLContext):
        """Sending the last message to the server before leaving.

        Args:
            servers: FL servers
            task_name: project name
            token: FL client token
            fl_ctx: FLContext

        Returns:
            server's reply to the last message

        """
        pass

    def send_heartbeat(self, servers, task_name, token, ssid, client_name, engine: ClientEngineInternalSpec, interval):
        pass

    def _clean_up_runs(self, engine, abort_runs):
        # abort_runs = list(set(response.abort_jobs))
        pass
