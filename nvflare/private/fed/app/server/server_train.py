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

"""Federated server launching script."""

import argparse
import logging
import os
import sys
import time

from nvflare.apis.fl_constant import FLContextKey, JobConstants, SiteType, WorkspaceConstants
from nvflare.apis.workspace import Workspace
from nvflare.fuel.common.excepts import ConfigError
from nvflare.fuel.f3.mpm import MainProcessMonitor as mpm
from nvflare.fuel.utils.argument_utils import parse_vars
from nvflare.fuel.utils.log_utils import configure_logging
from nvflare.private.defs import AppFolderConstants
from nvflare.private.fed.app.fl_conf import FLServerStarterConfiger, create_privacy_manager
from nvflare.private.fed.app.utils import create_admin_server, version_check
from nvflare.private.fed.server.server_status import ServerStatus
from nvflare.private.fed.utils.fed_utils import fobs_initialize, security_init
from nvflare.private.privacy_manager import PrivacyService
from nvflare.security.logging import secure_format_exception


def main(args):
    pass


def parse_arguments():
    pass


if __name__ == "__main__":
    """
    This is the main program when starting the NVIDIA FLARE server process.
    """

    version_check()
    args = parse_arguments()
    rc = mpm.run(main_func=main, run_dir=args.workspace, args=args)
    sys.exit(rc)
