# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
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
import json
import logging
import os
import sys
import threading

from nvflare.apis.fl_constant import ConnectionSecurity, ConnPropKey, ReservedKey, WorkspaceConstants
from nvflare.apis.fl_context import FLContext
from nvflare.apis.signal import Signal
from nvflare.apis.utils.decomposers import flare_decomposers
from nvflare.apis.workspace import Workspace
from nvflare.fuel.f3.cellnet.cell import Cell
from nvflare.fuel.f3.cellnet.fqcn import FQCN
from nvflare.fuel.f3.cellnet.net_agent import NetAgent
from nvflare.fuel.f3.drivers.driver_params import DriverParams
from nvflare.fuel.f3.drivers.net_utils import SSL_ROOT_CERT, enhance_credential_info
from nvflare.fuel.f3.message import Message as CellMessage
from nvflare.fuel.f3.mpm import MainProcessMonitor as mpm
from nvflare.fuel.sec.authn import set_add_auth_headers_filters
from nvflare.fuel.utils.argument_utils import parse_vars
from nvflare.fuel.utils.config_service import ConfigService, search_file
from nvflare.fuel.utils.log_utils import configure_logging
from nvflare.fuel.utils.url_utils import make_url
from nvflare.private.defs import ClientType
from nvflare.private.fed.authenticator import Authenticator, validate_auth_headers
from nvflare.private.fed.utils.identity_utils import TokenVerifier


class CellnetMonitor:
    def __init__(self, stop_event: threading.Event, workspace: str):
        self.stop_event = stop_event
        self.workspace = workspace

    def cellnet_stopped(self):
        pass


class _ConfigKey:
    PROJECT_NAME = "project_name"
    SERVER_IDENTITY = "server_identity"
    IDENTITY = "identity"
    CONNECT_TO = "connect_to"


def parse_arguments():
    pass


def main(args):
    pass


def _validate_auth_headers(message: CellMessage, token_verifier: TokenVerifier, logger):
    """Validate auth headers from messages that go through the server.
    Args:
        message: the message to validate
    Returns:
    """
    pass


if __name__ == "__main__":
    args = parse_arguments()
    rc = mpm.run(main_func=main, run_dir=args.workspace, args=args)
    sys.exit(rc)
