# Copyright (c) 2026, NVIDIA CORPORATION.  All rights reserved.
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

"""nvflare package command handler."""

import datetime
import os
import re
import shutil
import sys
from urllib.parse import urlparse

from nvflare.apis.utils.format_check import name_check
from nvflare.lighter.constants import AdminRole, CtxKey, ParticipantType, PropKey
from nvflare.lighter.entity import Project
from nvflare.lighter.impl.cert import CertBuilder
from nvflare.lighter.impl.static_file import StaticFileBuilder
from nvflare.lighter.impl.workspace import WorkspaceBuilder
from nvflare.lighter.prov_utils import prepare_builders
from nvflare.lighter.provision import prepare_project
from nvflare.lighter.provisioner import Provisioner
from nvflare.lighter.spec import Builder
from nvflare.lighter.utils import load_crt, load_yaml, verify_cert
from nvflare.tool.cert.cert_constants import ADMIN_CERT_TYPES, KIT_TYPE_TO_ROLE, VALID_CERT_TYPES
from nvflare.tool.cli_output import is_json_mode, output_error, output_error_message, output_ok, output_usage_error
from nvflare.tool.cli_schema import handle_schema_flag

_VALID_SCHEMES = {"grpc", "tcp", "http"}
_ADMIN_ROLES = set(ADMIN_CERT_TYPES)
_VALID_CERT_TYPES = set(VALID_CERT_TYPES)
_KIT_TYPE_TO_ROLE = KIT_TYPE_TO_ROLE
_DUMMY_SERVER_NAME = "__nvflare_dummy_server__"
_DUMMY_ORG = "myorg"


def _read_cert_type_from_cert(cert) -> str:
    """Return the kit type embedded in cert's UNSTRUCTURED_NAME, or '' if absent."""
    pass


class PrebuiltCertBuilder(Builder):
    """Builder that installs pre-made cert/key/rootCA into each participant's kit directory.

    Replaces CertBuilder for the ``nvflare package`` workflow where certs are already signed
    externally.  The caller supplies the cert/key/rootCA paths; this builder simply copies them
    into the correct locations that StaticFileBuilder and the runtime expect.

    Two modes:
    - Single-participant: pass cert_path/key_path/rootca_path + optional target_name.
    - Multi-participant: pass cert_map={name: (cert_path, key_path)} + rootca_path.
      Only participants present in cert_map receive certs; others (e.g. dummy server) are skipped.
    """

    def __init__(
        self,
        cert_path: str = None,
        key_path: str = None,
        rootca_path: str = None,
        target_name: str = None,
        cert_map: dict = None,
    ):
        self.cert_path = cert_path
        self.key_path = key_path
        self.rootca_path = rootca_path
        self.target_name = target_name
        self.cert_map = cert_map  # {participant_name: (cert_path, key_path)}

    def build(self, project: Project, ctx):
        pass


def _parse_endpoint(endpoint: str) -> tuple:
    """Return (scheme, host, port: int). Raises ValueError on invalid format."""
    pass


def _discover_name_from_dir(work_dir: str) -> str:
    """Find the single *.key file in work_dir and return its stem as the participant name."""
    pass


def _latest_prod_dir(workspace: str, project_name: str):
    """Return the path to the highest-numbered existing prod_NN under workspace/project_name/.

    Returns None if no prod_NN directories exist.
    """
    pass


def _load_project_from_file(path: str) -> tuple:
    """Load and validate a project yaml or single-site yaml. Returns (project, custom_builders).

    Accepts:
    - Full project YAML (api_version 3/4) with participants
    - Single-site YAML with name/org/type (converted to a minimal project)
    """
    pass


def _handle_package_yaml_mode(args, scheme, host, port):
    """Build kits for all participants defined in a project yaml file.

    Called by handle_package when --project-file is given.  The cert/key for each participant
    is resolved from --dir/<name>.crt and --dir/<name>.key; rootCA is --dir/rootCA.pem.
    """
    pass


def handle_package(args):
    """Assemble a startup kit from locally generated key + Project Admin cert + rootCA.pem."""
    pass
