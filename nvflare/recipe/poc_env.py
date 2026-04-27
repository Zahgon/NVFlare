# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
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

import os
import shutil
import threading
import time
from typing import Optional

from pydantic import BaseModel, conint, model_validator

from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.job_config.api import FedJob
from nvflare.recipe.spec import ExecEnv
from nvflare.recipe.utils import collect_non_local_scripts
from nvflare.tool.poc.poc_commands import (
    _clean_poc,
    _start_poc,
    _stop_poc,
    get_poc_workspace,
    get_prod_dir,
    is_poc_running,
    prepare_poc_provision,
    setup_service_config,
)
from nvflare.tool.poc.service_constants import FlareServiceConstants as SC

from .session_mgr import SessionManager

STOP_POC_TIMEOUT = 10
SERVICE_START_TIMEOUT = 3
DEFAULT_ADMIN_USER = "admin@nvidia.com"


# Internal — not part of the public API
class _PocEnvValidator(BaseModel):
    num_clients: Optional[conint(gt=0)] = None
    clients: Optional[list[str]] = None
    gpu_ids: Optional[list[int]] = None
    use_he: bool = False
    docker_image: Optional[str] = None
    project_conf_path: str = ""
    username: str = DEFAULT_ADMIN_USER

    @model_validator(mode="after")
    def check_client_configuration(self):
        # Check if clients list is empty
        pass


class PocEnv(ExecEnv):
    """Proof of Concept execution environment for local testing and development.

    This environment sets up a POC deployment on a single machine with multiple
    processes representing the server, clients, and admin console.
    """

    def __init__(
        self,
        *,
        num_clients: Optional[int] = 2,
        clients: Optional[list[str]] = None,
        gpu_ids: Optional[list[int]] = None,
        use_he: bool = False,
        docker_image: Optional[str] = None,
        project_conf_path: str = "",
        username: str = DEFAULT_ADMIN_USER,
        extra: Optional[dict] = None,
    ):
        """Initialize POC execution environment.

        Args:
            num_clients (int, optional): Number of clients to use in POC mode. Defaults to 2.
            clients (list[str], optional): List of client names. If None, will generate site-1, site-2, etc. Defaults to None.
                If specified, number_of_clients argument will be ignored.
            gpu_ids (list[int], optional): List of GPU IDs to assign to clients. If None, uses CPU only. Defaults to None.
            use_he (bool, optional): Whether to use HE. Defaults to False.
            docker_image (str, optional): Docker image to use for POC. Defaults to None.
            project_conf_path (str, optional): Path to the project configuration file. Defaults to "".
                If specified, 'number_of_clients','clients' and 'docker' specific options will be ignored.
            username (str, optional): Admin user. Defaults to "admin@nvidia.com".
            extra: extra env info.
        """
        super().__init__(extra)
        self.logger = get_obj_logger(self)

        v = _PocEnvValidator(
            num_clients=num_clients,
            clients=clients,
            gpu_ids=gpu_ids,
            use_he=use_he,
            docker_image=docker_image,
            project_conf_path=project_conf_path,
            username=username,
        )

        self.clients = v.clients
        self.num_clients = len(v.clients) if v.clients is not None else v.num_clients
        self.poc_workspace = get_poc_workspace()
        self.gpu_ids = v.gpu_ids or []
        self.use_he = v.use_he
        self.project_conf_path = v.project_conf_path
        self.docker_image = v.docker_image
        self.username = v.username
        self._session_manager = None  # Lazy initialization
        self._session_manager_lock = threading.Lock()

    def deploy(self, job: FedJob) -> str:
        """Deploy a FedJob to the POC environment.

        Args:
            job (FedJob): The FedJob to deploy.

        Returns:
            str: Job ID.

        Raises:
            ValueError: If scripts do not exist locally.
        """
        pass

    def _check_poc_running(self) -> bool:
        """Check if POC services are currently running.

        Returns:
            bool: True if POC is running, False otherwise.
        """
        pass

    def stop(self, clean_up: bool = False) -> None:
        """Try to stop and clean existing POC.

        This method is idempotent - safe to call multiple times.

        Args:
            clean_up (bool, optional): Whether to clean the POC workspace. Defaults to False.
        """
        pass

    def get_job_status(self, job_id: str) -> Optional[str]:
        """Get the status of a job.

        Args:
            job_id: The job ID to check status for.

        Returns:
            Optional[str]: The status of the job, or None if not available.
        """
        pass

    def abort_job(self, job_id: str) -> None:
        """Abort a running job.

        Args:
            job_id: The job ID to abort.
        """
        pass

    def get_job_result(self, job_id: str, timeout: float = 0.0) -> Optional[str]:
        """Get the result workspace of a job.

        Args:
            job_id: The job ID to get results for.
            timeout: The timeout for the job to complete. Defaults to 0.0 (no timeout).

        Returns:
            Optional[str]: The result workspace path if job completed, None otherwise.
        """
        pass

    def _get_admin_startup_kit_path(self) -> str:
        """Get the path to the admin startup kit for POC.

        Returns:
            str: Path to admin startup kit directory.
        """
        pass

    def _get_session_manager(self) -> SessionManager:
        """Get or create SessionManager with lazy initialization (thread-safe)."""
        pass
