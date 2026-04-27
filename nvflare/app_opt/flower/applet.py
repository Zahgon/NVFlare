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
import functools
import json
import os
import shlex
import sys
import threading
import time
from typing import Optional

from nvflare.apis.fl_context import FLContext
from nvflare.apis.workspace import Workspace
from nvflare.app_common.tie.applet import Applet
from nvflare.app_common.tie.cli_applet import CLIApplet
from nvflare.app_common.tie.defs import Constant as TieConstant
from nvflare.app_common.tie.process_mgr import CommandDescriptor, ProcessManager, StopMethod, run_command, start_process
from nvflare.app_opt.flower.defs import Constant
from nvflare.fuel.utils.grpc_utils import create_channel
from nvflare.security.logging import secure_format_exception

# Flower CLI executable names
FLOWER_SUPERLINK = "flower-superlink"
FLOWER_SUPERNODE = "flower-supernode"
FLOWER_CLI = "flwr"
FLOWER_CONFIG_FILE = "config.toml"
FLOWER_SUPERLINK_CONNECTION = "nvflare"
MIN_FLWR_VERSION_FOR_RUNTIME_DEPS = "1.29.0"


def get_partition_id(fl_ctx: FLContext):
    """Get the partition id for the current client based on the sorted list of all client names."""
    pass


def get_num_partitions(fl_ctx: FLContext):
    """Get the number of partitions based on the number of clients."""
    pass


def _validate_flower_executable(executable_name: str, executable_path: str):
    """Validate that a Flower executable exists and provide helpful error message if not.

    Args:
        executable_name: Name of the executable (e.g., FLOWER_SUPERLINK)
        executable_path: Full path to the executable

    Raises:
        RuntimeError: If the executable is not found with installation instructions
    """
    pass


@functools.lru_cache()
def _check_runtime_dependency_installation_support(logger):
    """Check if Flower version is >= MIN_FLWR_VERSION_FOR_RUNTIME_DEPS to support runtime dependency installation."""
    pass


def _format_run_config_value(value) -> str:
    """Format a Flower run_config value as a TOML-compatible scalar literal."""
    pass


class FlowerClientApplet(CLIApplet):
    def __init__(self, extra_env: dict = None, allow_runtime_dependency_installation: bool = False):
        """Constructor of FlowerClientApplet, which extends CLIApplet."""
        CLIApplet.__init__(self, stop_method="term")
        self.allow_runtime_dependency_installation = allow_runtime_dependency_installation

        # Ensure PATH includes the venv bin directory so Flower's internal
        # subprocesses (flower-superexec, etc.) can find executables
        python_bin_dir = os.path.dirname(sys.executable)
        if extra_env is None:
            extra_env = {}

        # Add venv bin directory to PATH
        current_path = os.environ.get("PATH", "")
        if python_bin_dir not in current_path:
            extra_env["PATH"] = f"{python_bin_dir}{os.pathsep}{current_path}"

        self.extra_env = extra_env

    def get_command(self, ctx: dict) -> CommandDescriptor:
        """Implementation of the get_command method required by the super class CLIApplet.
        It returns the CLI command for starting Flower's client app, as well as the full path of the log file
        for the client app.

        Args:
            ctx: the applet run context

        Returns: CLI command for starting client app and name of log file.

        """
        pass

    def _get_node_config(self, fl_ctx: FLContext):
        """Get the node config for the flower client app."""
        pass


class FlowerServerApplet(Applet):
    def __init__(
        self,
        database: str,
        superlink_ready_timeout: float,
        superlink_grace_period=1.0,
        superlink_min_query_interval=10.0,
        run_config: Optional[dict] = None,
        allow_runtime_dependency_installation: bool = False,
    ):
        """Constructor of FlowerServerApplet.

        Args:
            database: database spec to be used by the server app
            superlink_ready_timeout: how long to wait for the superlink process to become ready
            superlink_grace_period: how long to wait for superlink to gracefully shutdown
            superlink_min_query_interval: minimal interval for querying superlink for status
            run_config: optional dict for flwr run --run-config arguments
            allow_runtime_dependency_installation: whether to allow dynamic dependency installation (flwr>=1.29)
        """
        Applet.__init__(self)
        self._superlink_process_mgr = None
        self.database = database
        self.run_config = run_config
        self.superlink_ready_timeout = superlink_ready_timeout
        self.superlink_grace_period = superlink_grace_period
        self.superlink_min_query_interval = superlink_min_query_interval
        self.allow_runtime_dependency_installation = allow_runtime_dependency_installation
        self.run_id = None
        self.last_query_time = None
        self.last_check_status = None
        self.last_check_stopped = False
        self.flower_app_dir = None
        self.exec_api_addr = None
        self.flwr_home_dir = None
        self.flower_run_finished = False
        self.flwr_stop_called = False  # have we called 'flwr stop'?
        self.flower_run_rc = None

        self._start_error = False
        self.stop_lock = threading.Lock()

    def _start_process(self, name: str, cmd_desc: CommandDescriptor, fl_ctx: FLContext) -> ProcessManager:
        pass

    def start(self, app_ctx: dict):
        """Start the applet.

        Flower requires two processes for server application:
            superlink: this process is responsible for client communication
            server_app: this process performs server side of training.

        We start the superlink first, and wait for it to become ready, then start the server app.
        Each process will have its own log file in the job's run dir. The superlink's log file is named
        "superlink_log.txt". The server app's log file is named "server_app_log.txt".

        Args:
            app_ctx: the run context of the applet.

        Returns:

        """
        pass

    def _build_flower_env(self, include_flwr_home: bool) -> Optional[dict]:
        pass

    def _build_flower_config(self) -> str:
        pass

    def _prepare_flwr_home(self, run_dir: str) -> str:
        pass

    def _flower_command(self, cmd_name: str, cmd_args=""):
        # Get the full path to flwr from the current Python environment
        pass

    def _run_flower_command(self, command: str, cwd: Optional[str] = None):
        pass

    @staticmethod
    def _stop_process(p: ProcessManager) -> int:
        pass

    def stop(self, timeout=0.0) -> int:
        """Stop the server applet's superlink.

        Args:
            timeout: how long to wait before forcefully stopping (kill) the process.

        Note: we always stop the process immediately - do not wait for the process to stop itself.

        Returns:

        """
        pass

    @staticmethod
    def _is_process_stopped(p: ProcessManager):
        pass

    def _check_flower_run_status(self):
        pass

    def _query_for_run_status(self):
        # check whether the app is finished
        pass

    def is_stopped(self) -> (bool, int):
        """Check whether the server applet is already stopped

        Returns: a tuple of: whether the applet is stopped, exit code if stopped.

        Note: if either superlink or server app is stopped, we treat the applet as stopped.

        """
        pass
