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
import logging
import os
import re
import time
from abc import abstractmethod

try:
    import docker.errors

    import docker

    _DOCKER_AVAILABLE = True
except ImportError:
    _DOCKER_AVAILABLE = False

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import FLContextKey, JobConstants
from nvflare.apis.fl_context import FLContext
from nvflare.apis.job_def import JobMetaKey, get_job_meta_study
from nvflare.apis.job_launcher_spec import JobHandleSpec, JobLauncherSpec, JobProcessArgs, JobReturnCode, add_launcher
from nvflare.apis.workspace import Workspace
from nvflare.utils.job_launcher_utils import get_client_job_args, get_job_launcher_spec, get_server_job_args


# Docker container status strings
class DockerStatus:
    CREATED = "created"
    RESTARTING = "restarting"
    RUNNING = "running"
    PAUSED = "paused"
    EXITED = "exited"
    DEAD = "dead"


TERMINAL_STATUSES = {DockerStatus.EXITED, DockerStatus.DEAD}


def _sanitize_container_name(name: str) -> str:
    """Sanitize a string to a valid Docker container name.

    Docker container names allow alphanumeric, hyphens, underscores, and dots.
    """
    pass


def _exit_code_to_return_code(exit_code: int) -> JobReturnCode:
    pass


class DockerJobHandle(JobHandleSpec):
    """Handle for a running Docker container job.

    Modeled on K8sJobHandle: once the container reaches a terminal state,
    terminal_state is set and all subsequent poll()/wait() calls return
    immediately without querying Docker.
    """

    def __init__(
        self,
        container_id: str,
        container_name: str,
        docker_client,
        timeout: int = 30,
    ):
        super().__init__()
        self.container_id = container_id
        self.container_name = container_name
        self.docker_client = docker_client
        self.timeout = timeout
        self.terminal_state: JobReturnCode = None  # set once, never cleared
        self.logger = logging.getLogger(self.__class__.__name__)

    def _get_container(self):
        """Query Docker for the current container object.

        Returns None if not found (sets terminal_state) or on API error.
        """
        pass

    def _resolve_terminal_return_code(self, container) -> JobReturnCode:
        """Get the final JobReturnCode from a terminal container using exit code."""
        pass

    def _remove_container(self):
        """Remove the container after it has reached a terminal state."""
        pass

    def poll(self) -> JobReturnCode:
        """Non-blocking status check. Returns UNKNOWN while still running."""
        pass

    def wait(self):
        """Block until the container reaches a terminal state."""
        pass

    def terminate(self):
        """Stop and remove the container. Always sets terminal_state."""
        pass

    def enter_states(self, states_to_enter: list) -> bool:
        """Poll until the container enters one of the target states.

        Returns True if the target state was reached, False otherwise
        (timeout, stuck, or terminal state reached before target).
        """
        pass


def _job_args_dict(job_args: dict, arg_names: list) -> dict:
    """Extract a {flag: value} dict from JOB_PROCESS_ARGS for the given arg names."""
    pass


class DockerJobLauncher(JobLauncherSpec):
    """Launches NVFlare job processes as Docker containers.

    SP/CP runs as a container started by start_docker.sh (site admin).
    SJ/CJ containers are started dynamically per job by this launcher.

    Assumptions:
    - Docker network already exists (created by start_docker.sh or site admin).
    - Workspace is a host directory bind-mounted into all containers at /var/tmp/nvflare/workspace.
    - SP/CP container name is known and reachable via Docker DNS on the network.
    - parent_url is derived at runtime from the site name and the port in JOB_PROCESS_ARGS.
    """

    WORKSPACE_MOUNT = "/var/tmp/nvflare/workspace"
    DATA_MOUNT = "/var/tmp/nvflare/data"
    STUDY_DATA_PATH_FILE = "local/study_data.json"

    def __init__(
        self,
        workspace: str = None,
        network: str = "nvflare-network",
        python_path: str = "/usr/local/bin/python",
        timeout: int = 30,
        default_job_container_kwargs: dict = None,
        default_job_env: dict = None,
    ):
        """
        Args:
            workspace: host path to the NVFlare workspace directory (bind-mounted into job containers
                       at /var/tmp/nvflare/workspace). If not provided, reads from NVFL_DOCKER_WORKSPACE
                       environment variable. Must be the HOST path because it is passed directly to the
                       Docker daemon as a volume bind source.
            network: Docker network name. Must already exist.
            python_path: Python executable path inside the job container.
            timeout: max seconds to wait for container to reach RUNNING state (default 30).
            default_job_container_kwargs: site-level default docker run kwargs applied to every job
                                          container launched by this site. Job-level resource_spec[site][docker]
                                          takes precedence on conflict. Keys use Docker SDK naming
                                          (underscores, not hyphens).
                                          Example: {"shm_size": "8g", "ipc_mode": "host"}
                                          Note: "volumes", "network", "environment", "command", "name",
                                          "detach", "user", "working_dir" are controlled by the launcher
                                          and cannot be overridden here.
            default_job_env: site-level default environment variables injected into every job
                             container launched by this site. Useful for site/runtime-specific
                             settings such as NCCL workarounds. Launcher-controlled variables
                             like USER, HOME, and PYTHONPATH still take precedence.
        """
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)

        if not workspace:
            workspace = os.environ.get("NVFL_DOCKER_WORKSPACE")

        self.workspace = workspace
        self.network = network
        self.python_path = python_path
        self.timeout = timeout
        default_job_container_kwargs = default_job_container_kwargs or {}
        _RESERVED_KWARGS = {"volumes", "network", "environment", "command", "name", "detach", "user", "working_dir"}
        reserved_used = _RESERVED_KWARGS & set(default_job_container_kwargs.keys())
        if reserved_used:
            raise ValueError(
                f"default_job_container_kwargs must not contain reserved keys: {sorted(reserved_used)}. "
                f"These are controlled by the launcher."
            )
        self.default_job_container_kwargs = default_job_container_kwargs
        self.default_job_env = default_job_env or {}

        self._docker_client = None

    def _get_docker_client(self):
        pass

    def launch_job(self, job_meta: dict, fl_ctx: FLContext) -> JobHandleSpec:
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    @abstractmethod
    def get_module_args(self, job_args: dict) -> dict:
        """Return a {flag: value} dict of args to pass to the job module.

        Args:
            job_args: JOB_PROCESS_ARGS dict from FLContext (with PARENT_URL already overridden).

        Returns:
            dict of {flag: value} pairs to append after '-u -m <module>' in the container command.
        """
        pass


class ClientDockerJobLauncher(DockerJobLauncher):
    def get_module_args(self, job_args: dict) -> dict:
        pass


class ServerDockerJobLauncher(DockerJobLauncher):
    def get_module_args(self, job_args: dict) -> dict:
        pass
