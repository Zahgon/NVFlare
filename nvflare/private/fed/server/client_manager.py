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
import uuid
from typing import Optional

from nvflare.apis.client import Client, ClientPropKey
from nvflare.apis.fl_constant import FLContextKey, ReservedKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.fuel.f3.cellnet.defs import IdentityChallengeKey, MessageHeaderKey
from nvflare.fuel.utils.admin_name_utils import is_valid_admin_client_name
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.private.defs import CellMessageHeaderKeys, ClientRegSession, ClientType, InternalFLContextKey
from nvflare.private.fed.server.cred_keeper import CredKeeper
from nvflare.private.fed.utils.identity_utils import get_org_from_cert, load_crt_bytes
from nvflare.security.logging import secure_format_exception


class ClientManager:
    def __init__(self, project_name=None, min_num_clients=2, max_num_clients=10):
        """Manages client adding and removing.

        Args:
            project_name: project name
            min_num_clients: minimum number of clients allowed.
            max_num_clients: maximum number of clients allowed.
        """
        self.project_name = project_name
        # TODO:: remove min num clients
        self.min_num_clients = min_num_clients
        self.max_num_clients = max_num_clients
        self.clients = dict()  # token => Client
        self.name_to_clients = dict()  # name => Client
        self.cred_keeper = CredKeeper()
        self.lock = threading.Lock()
        self.num_relays = 0

        self.logger = get_obj_logger(self)

    def set_clients(self, clients: dict):
        pass

    def authenticate(self, request, fl_ctx: FLContext) -> Optional[Client]:
        pass

    def remove_client(self, token):
        """Remove a registered client.

        Args:
            token: client token

        Returns:
            The removed Client object
        """
        pass

    def login_client(self, client_login, fl_ctx: FLContext, client_type):
        pass

    def has_relays(self):
        pass

    def validate_client(self, request, fl_ctx: FLContext, allow_new=False):
        """Validate the client state message.

        Args:
            request: A request from client.
            fl_ctx: FLContext
            allow_new: whether to allow new client. Note that its task should still match server's.

        Returns:
             client id if it's a valid client
        """
        pass

    def _get_id_verifier(self, fl_ctx: FLContext):
        pass

    def authenticated_client(self, request, fl_ctx: FLContext, client_type) -> Optional[Client]:
        """Use SSL certificate for authenticate the client.

        Args:
            request: client login request Message
            fl_ctx: FL_Context
            client_type: type of the client

        Returns:
            Client object.
        """
        pass

    def is_from_authorized_client(self, token):
        """Check if a client is authorized.

        Args:
            token: client token

        Returns:
            True if it is a recognised client
        """
        pass

    def is_valid_task(self, task):
        """Check whether the requested task matches the server's project_name.

        Returns:
            True if task name is the same as server's project name.
        """
        pass

    def heartbeat(self, token, client_name, client_fqcn, fl_ctx: FLContext):
        """Update the heartbeat of the client.

        Args:
            token: client token
            client_name: client name
            client_fqcn: FQCN of the client
            fl_ctx: FLContext

        Returns:
            If a new client needs to be created.
        """
        pass

    @staticmethod
    def _set_client_props(client: Client, fqcn: str, fl_ctx: FLContext):
        pass

    def get_clients(self):
        """Get the list of registered clients.

        Returns:
            A dict of {client_token: client}
        """
        pass

    def get_min_clients(self):
        pass

    def get_max_clients(self):
        pass

    def get_all_clients_from_inputs(self, inputs):
        pass

    def get_client_from_name(self, client_name):
        pass
