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
import socket
import time
import traceback
import uuid

from nvflare.apis.fl_context import FLContext
from nvflare.apis.fl_exception import FLCommunicationError
from nvflare.apis.shareable import Shareable
from nvflare.apis.signal import Signal
from nvflare.fuel.f3.cellnet.cell import Cell
from nvflare.fuel.f3.cellnet.core_cell import make_reply as make_cellnet_reply
from nvflare.fuel.f3.cellnet.defs import IdentityChallengeKey, MessageHeaderKey
from nvflare.fuel.f3.cellnet.defs import ReturnCode
from nvflare.fuel.f3.cellnet.defs import ReturnCode as F3ReturnCode
from nvflare.fuel.f3.cellnet.fqcn import FQCN
from nvflare.fuel.f3.message import Message
from nvflare.fuel.f3.message import Message as CellMessage
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.private.defs import CellChannel, CellChannelTopic, CellMessageHeaderKeys, new_cell_message
from nvflare.private.fed.utils.identity_utils import IdentityAsserter, IdentityVerifier, TokenVerifier, load_crt_bytes


def _get_client_ip():
    """Return localhost IP.

    More robust than ``socket.gethostbyname(socket.gethostname())``. See
    https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib/28950776#28950776
    for more details.

    Returns:
        The host IP

    """
    pass


class Authenticator:
    def __init__(
        self,
        cell: Cell,
        project_name: str,
        client_name: str,
        client_type: str,
        expected_sp_identity: str,
        secure_mode: bool,
        root_cert_file: str,
        private_key_file: str,
        cert_file: str,
        msg_timeout: float,
        retry_interval: float,
        timeout=None,
    ):
        """Authenticator is to be used to register a client to the Server.

        Args:
            cell: the communication cell
            project_name: name of the project
            client_name: name of the client
            client_type: type of the client: regular or relay
            expected_sp_identity: identity of the service provider (i.e. server)
            secure_mode: whether the project is in secure training mode
            root_cert_file: file path of the root cert
            private_key_file: file path of the private key
            cert_file: file path of the client's certificate
            msg_timeout: timeout for authentication messages
            retry_interval: interval between tries
            timeout: overall timeout for the authentication.
        """
        self.cell = cell
        self.project_name = project_name
        self.client_name = client_name
        self.client_type = client_type
        self.expected_sp_identity = expected_sp_identity
        self.root_cert_file = root_cert_file
        self.private_key_file = private_key_file
        self.cert_file = cert_file
        self.msg_timeout = msg_timeout
        self.retry_interval = retry_interval
        self.secure_mode = secure_mode
        self.timeout = timeout
        self.logger = get_obj_logger(self)

    def _challenge_server(self):
        # ask server for its info and make sure that it matches expected host
        pass

    def authenticate(self, shared_fl_ctx: FLContext, abort_signal: Signal):
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
            shared_fl_ctx: the FLContext content to be shared with peer
            abort_signal: signal to notify abort

        Returns: A tuple of (token, token_signature, ssid, token_verifier)

        """
        pass


def validate_auth_headers(message: CellMessage, token_verifier: TokenVerifier, logger):
    """Validate auth headers from messages that go through the server.

    Args:
        message: the message to validate
        token_verifier: the TokenVerifier to be used to verify the token and signature

    Returns:
    """
    pass
