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

import json
import os

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID

from nvflare.lighter.constants import CertFileBasename, CtxKey, ParticipantType, PropKey
from nvflare.lighter.ctx import ProvisionContext
from nvflare.lighter.entity import Participant, Project
from nvflare.lighter.spec import Builder
from nvflare.lighter.utils import Identity, generate_cert, generate_keys, serialize_cert, serialize_pri_key

MAX_CN_LENGTH = 64


class _CertState:

    CERT_STATE_FILE = "cert.json"

    PROP_ROOT_CERT = CtxKey.ROOT_CERT
    PROP_ROOT_PRI_KEY = CtxKey.ROOT_PRI_KEY
    PROP_CERT = "cert"
    PROP_PRI_KEY = "pri_key"

    def __init__(self, state_dir: str):
        self.is_available = False
        self.state_dir = state_dir
        self.content = {}
        cert_file = os.path.join(state_dir, self.CERT_STATE_FILE)
        if os.path.exists(cert_file):
            self.is_available = True
            with open(cert_file, "rt") as f:
                self.content.update(json.load(f))

    def get_root_cert(self):
        pass

    def set_root_cert(self, cert):
        pass

    def get_root_pri_key(self):
        pass

    def set_root_pri_key(self, key):
        pass

    def has_subject(self, subject: str):
        pass

    def _add_subject_prop(self, subject: str, key: str, value):
        pass

    def _get_subject_prop(self, subject: str, key: str):
        pass

    def add_subject_cert(self, subject: str, cert):
        pass

    def get_subject_cert(self, subject: str):
        pass

    def add_subject_pri_key(self, subject: str, pri_key):
        pass

    def get_subject_pri_key(self, subject: str):
        pass

    def persist(self):
        pass


class CertBuilder(Builder):
    def __init__(self):
        """Build certificate chain for every participant.

        Handles building (creating and self-signing) the root CA certificates, creating server, client and
        admin certificates, and having them signed by the root CA for secure communication. If the state folder has
        information about previously generated certs, it loads them back and reuses them.
        """
        self.root_cert = None
        self.persistent_state = None
        self.serialized_cert = None
        self.pri_key = None
        self.pub_key = None
        self.subject = None
        self.issuer = None

    @staticmethod
    def _fix_server_name(server: Participant):
        """Server Name is used as CN of the cert. But the CN cannot exceed 63 chars. So we have to truncate it
        to make the cert.

        Server Name also serves as the identity of the server for all clients to verify, and it must match the
        CN in the server's cert.

        Server Name is also the default host name (unless default host is explicitly specified) for clients to
        connect to. Truncated name won't be a valid host name.

        We have to accommodate all these factors:

        - We truncate the server name and use it for both name and subject of the server. This will satisfy CN
        requirement of the cert, and will satisfy server identity validation by clients.

        - We check whether the DEFAULT_HOST property is explicitly specified in the server. If not, we explicitly
        set it to the original name.

        Args:
            server: the server to be fixed.

        Returns:

        """
        pass

    def initialize(self, project: Project, ctx: ProvisionContext):
        pass

    def _build_root(self, subject, subject_org):
        pass

    def _build_write_cert_pair(self, participant: Participant, base_name, ctx: ProvisionContext):
        pass

    def _build_internal_listener_cert(self, participant: Participant, ctx: ProvisionContext):
        """Build server cert if the participant has internal listeners.
        Note that internal listener used to be only used for connecting SJ to SP, and CJ to SP, but now
        relay hierarchy is connected to internal listeners.

        Just like the FL Server, a relay could offer one or more hosts for other relays and clients to
        connect to. Therefore, the relay's server cert must include all these host names and IP addresses
        for others to make SSL-based connections using any one of these host names/addresses.

        Args:
            participant: the participant being provisioned
            ctx: a ProvisionContext object

        Returns: None

        """
        pass

    def build(self, project: Project, ctx: ProvisionContext):
        pass

    def get_pri_key_cert(self, participant: Participant):
        pass

    @staticmethod
    def _generate_cert(
        subject,
        subject_org,
        issuer,
        signing_pri_key,
        subject_pub_key,
        valid_days=360,
        ca=False,
        role=None,
        server: Participant = None,
    ):
        pass

    def finalize(self, project: Project, ctx: ProvisionContext):
        pass
