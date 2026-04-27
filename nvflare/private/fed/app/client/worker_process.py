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

"""Provides a command line interface for a federated client trainer."""

import argparse
import os
import sys
import threading

from nvflare.apis.fl_constant import ConfigVarName, FLContextKey, JobConstants, SiteType, SystemConfigs
from nvflare.apis.overseer_spec import SP
from nvflare.apis.workspace import Workspace
from nvflare.app_opt.job_launcher.workspace_cell_transfer import download_workspace, upload_results_safely
from nvflare.fuel.f3.mpm import MainProcessMonitor as mpm
from nvflare.fuel.utils.argument_utils import parse_vars
from nvflare.fuel.utils.config_service import ConfigService
from nvflare.fuel.utils.log_utils import configure_logging, get_script_logger
from nvflare.private.fed.app.fl_conf import FLClientStarterConfiger
from nvflare.private.fed.app.utils import monitor_parent_process
from nvflare.private.fed.client.client_app_runner import ClientAppRunner
from nvflare.private.fed.client.client_status import ClientStatus
from nvflare.private.fed.utils.fed_utils import (
    create_stats_pool_files_for_job,
    fobs_initialize,
    register_ext_decomposers,
    security_close,
    security_init_for_job,
    set_stats_pool_config_for_job,
)
from nvflare.security.logging import secure_format_exception


def main(args):
    pass


def parse_arguments():
    """Worker process start program."""
    pass


def _create_sp(args):
    pass


def remove_restart_file(workspace: Workspace):
    """To remove the restart.fl file.

    Args:
        workspace: workspace object

    """
    pass


if __name__ == "__main__":
    """
    This is the program when starting the child process for running the NVIDIA FLARE executor.
    """

    # main()
    args = parse_arguments()
    run_dir = os.path.join(args.workspace, args.job_id)
    rc = mpm.run(main_func=main, run_dir=run_dir, args=args)
    sys.exit(rc)
