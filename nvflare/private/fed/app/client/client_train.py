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

"""Federated client launching script."""

import argparse
import os
import sys
import time

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import FLContextKey, JobConstants, SiteType, WorkspaceConstants
from nvflare.apis.workspace import Workspace
from nvflare.fuel.common.excepts import ConfigError
from nvflare.fuel.f3.mpm import MainProcessMonitor as mpm
from nvflare.fuel.utils.argument_utils import parse_vars
from nvflare.fuel.utils.log_utils import configure_logging
from nvflare.private.defs import AppFolderConstants
from nvflare.private.fed.app.fl_conf import FLClientStarterConfiger, create_privacy_manager
from nvflare.private.fed.app.utils import component_security_check, version_check
from nvflare.private.fed.client.admin import FedAdminAgent
from nvflare.private.fed.client.client_engine import ClientEngine
from nvflare.private.fed.client.client_status import ClientStatus
from nvflare.private.fed.client.fed_client import FederatedClient
from nvflare.private.fed.utils.fed_utils import fobs_initialize, security_init
from nvflare.private.privacy_manager import PrivacyService
from nvflare.security.logging import secure_format_exception


def main(args):
    pass


def parse_arguments():
    pass


def create_admin_agent(req_processors, federated_client: FederatedClient, client_engine: ClientEngine):
    """Creates an admin agent.

    Args:
        req_processors: request processors
        federated_client: FL client object
        client_engine: ClientEngine

    Returns:
        A FedAdminAgent.
    """
    pass


if __name__ == "__main__":
    """
    This is the main program when starting the NVIDIA FLARE client process.
    """
    # # For MacOS, it needs to use 'spawn' for creating multi-process.
    # if os.name == 'posix':
    #     import multiprocessing
    #     multiprocessing.set_start_method('spawn')

    # import multiprocessing
    # multiprocessing.set_start_method('spawn')

    # main()
    version_check()
    args = parse_arguments()
    rc = mpm.run(main_func=main, run_dir=args.workspace, args=args)
    sys.exit(rc)
