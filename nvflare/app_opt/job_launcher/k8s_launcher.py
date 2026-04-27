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
from __future__ import annotations

import base64
import copy
import hashlib
import logging
import os
import re
import time
from abc import abstractmethod
from enum import Enum

import yaml

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import FLContextKey, JobConstants
from nvflare.apis.fl_context import FLContext
from nvflare.apis.job_def import JobMetaKey
from nvflare.apis.job_launcher_spec import JobHandleSpec, JobLauncherSpec, JobProcessArgs, JobReturnCode, add_launcher
from nvflare.app_opt.job_launcher.workspace_cell_transfer import (
    ENV_WORKSPACE_OWNER_FQCN,
    ENV_WORKSPACE_TRANSFER_TOKEN,
    WorkspaceTransferManager,
)
from nvflare.utils.job_launcher_utils import (
    get_client_job_args,
    get_job_launcher_spec,
    get_launcher_resource_spec,
    get_server_job_args,
)


class JobState(Enum):
    STARTING = "starting"
    RUNNING = "running"
    TERMINATED = "terminated"
    SUCCEEDED = "succeeded"
    UNKNOWN = "unknown"


class PodPhase(Enum):
    PENDING = "Pending"
    RUNNING = "Running"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    UNKNOWN = "Unknown"


POD_STATE_MAPPING = {
    PodPhase.PENDING.value: JobState.STARTING,
    PodPhase.RUNNING.value: JobState.RUNNING,
    PodPhase.SUCCEEDED.value: JobState.SUCCEEDED,
    PodPhase.FAILED.value: JobState.TERMINATED,
    PodPhase.UNKNOWN.value: JobState.UNKNOWN,
}

JOB_RETURN_CODE_MAPPING = {
    JobState.SUCCEEDED: JobReturnCode.SUCCESS,
    JobState.STARTING: JobReturnCode.UNKNOWN,
    JobState.RUNNING: JobReturnCode.UNKNOWN,
    JobState.TERMINATED: JobReturnCode.ABORTED,
    JobState.UNKNOWN: JobReturnCode.UNKNOWN,
}

DEFAULT_CONTAINER_ARGS_MODULE_ARGS_DICT = {
    "-m": None,
    "-w": None,
    "-t": None,
    "-d": None,
    "-n": None,
    "-c": None,
    "-p": None,
    "-g": None,
    "-scheme": None,
    "-s": None,
}

DEFAULT_NAMESPACE = "default"
DEFAULT_PENDING_TIMEOUT = 120
DEFAULT_PYTHON_PATH = "/usr/local/bin/python"


DATA_PVC_VOLUME_NAME = "nvfldata"
WORKSPACE_MOUNT_PATH = "/var/tmp/nvflare/workspace"
DEFAULT_EPHEMERAL_STORAGE = "1Gi"

# Files actually read from startup/ by the job pod at runtime. Others in
# startup/ are dropped to shrink the Secret. local/ is bundled whole with each
# job workspace so job resource files and local custom code keep working.
_STARTUP_KEEP_SUFFIXES = (".crt", ".key", ".pem", ".json")


def _keep_startup_file(fname: str) -> bool:
    pass


def uuid4_to_rfc1123(uuid_str: str) -> str:
    pass


def site_name_to_rfc1123(site_name: str, max_length: int = 47) -> str:
    """Convert a site name into a stable RFC1123-safe label with a hash suffix."""
    pass


class K8sJobHandle(JobHandleSpec):
    def __init__(
        self,
        job_id: str,
        api_instance,
        job_config: dict,
        namespace=DEFAULT_NAMESPACE,
        timeout=None,
        pending_timeout=DEFAULT_PENDING_TIMEOUT,
        python_path=DEFAULT_PYTHON_PATH,
        workspace_transfer: WorkspaceTransferManager = None,
        workspace_job_id: str = "",
    ):
        super().__init__()
        self.job_id = job_id
        self.timeout = timeout
        self.terminal_state = None
        self.workspace_transfer = workspace_transfer
        self.workspace_job_id = workspace_job_id
        self.api_instance = api_instance
        self.namespace = namespace
        self.pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {"name": None},  # set by job_config['name']
            "spec": {
                "containers": None,  # link to container_list
                "volumes": None,  # link to volume_list
                "restartPolicy": "Never",
            },
        }
        self.volume_list = []

        self.container_list = [
            {
                "image": None,
                "name": None,
                "command": [python_path],
                "args": None,  # args_list + args_dict + args_sets
                "volumeMounts": None,  # volume_mount_list
                "imagePullPolicy": "Always",
            }
        ]
        command = job_config.get("command")
        if not command:
            raise ValueError("job_config must contain a non-empty 'command' key")
        self.container_args_python_args_list = ["-u", "-m", command]
        self.container_volume_mount_list = []
        self._make_manifest(job_config)
        self._stuck_count = 0
        self._max_stuck_count = self.timeout if self.timeout is not None else pending_timeout
        self.logger = logging.getLogger(self.__class__.__name__)

    def _make_manifest(self, job_config):
        pass

    def get_manifest(self):
        pass

    def enter_states(self, job_states_to_enter: list):
        pass

    def _remove_workspace_job(self) -> None:
        pass

    def terminate(self):
        pass

    def poll(self):
        pass

    def _query_phase(self):
        pass

    def _query_state(self):
        pass

    def _stuck_in_pending(self, current_phase):
        pass

    def wait(self):
        pass


class K8sJobLauncher(JobLauncherSpec):
    def __init__(
        self,
        config_file_path: str,
        study_data_pvc_file_path: str,
        timeout=None,
        namespace=DEFAULT_NAMESPACE,
        pending_timeout=DEFAULT_PENDING_TIMEOUT,
        python_path=DEFAULT_PYTHON_PATH,
        security_context: dict = None,
        ephemeral_storage: str = DEFAULT_EPHEMERAL_STORAGE,
    ):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config_file_path = config_file_path
        self.study_data_pvc_file_path = study_data_pvc_file_path
        self.timeout = timeout
        self.namespace = namespace
        self.pending_timeout = pending_timeout
        self.python_path = python_path
        self.security_context = security_context
        self.ephemeral_storage = ephemeral_storage
        self.study_data_pvc_dict = None
        self.default_data_pvc = None
        self.core_v1 = None

    def _ensure_startup_secret(self, site_name: str, startup_dir: str) -> str:
        """Create or update a k8s Secret containing the site startup kit.

        Returns the Secret name.
        """
        pass

    def launch_job(self, job_meta: dict, fl_ctx: FLContext) -> JobHandleSpec:
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    @abstractmethod
    def get_module_args(self, job_id, fl_ctx: FLContext):
        """To get the args to run the launcher

        Args:
            job_id: run job_id
            fl_ctx: FLContext

        Returns:

        """
        pass


def _job_args_dict(job_args: dict, arg_names: list) -> dict:
    pass


class ClientK8sJobLauncher(K8sJobLauncher):
    def get_module_args(self, _job_id, fl_ctx: FLContext):
        pass


class ServerK8sJobLauncher(K8sJobLauncher):
    def get_module_args(self, _job_id, fl_ctx: FLContext):
        pass
