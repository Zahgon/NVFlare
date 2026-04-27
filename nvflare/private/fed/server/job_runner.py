# Copyright (c) 2022-2026, NVIDIA CORPORATION.  All rights reserved.
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
from typing import Dict, List, Tuple

from nvflare.apis.client import Client
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import (
    AdminCommandNames,
    ConfigVarName,
    FLContextKey,
    RunProcessKey,
    SiteType,
    SystemComponents,
    SystemConfigs,
)
from nvflare.apis.fl_context import FLContext
from nvflare.apis.job_def import ALL_SITES, Job, JobMetaKey, RunStatus
from nvflare.apis.job_scheduler_spec import DispatchInfo
from nvflare.apis.workspace import Workspace
from nvflare.fuel.utils.config_service import ConfigService
from nvflare.lighter.tool_consts import NVFLARE_SIG_FILE
from nvflare.lighter.utils import verify_folder_signature
from nvflare.private.admin_defs import Message, MsgHeader, ReturnCode
from nvflare.private.defs import RequestHeader, TrainingTopic
from nvflare.private.fed.server.admin import check_client_replies
from nvflare.private.fed.server.server_state import HotState
from nvflare.private.fed.utils.app_deployer import AppDeployer
from nvflare.private.fed.utils.fed_utils import extract_participants, require_signed_jobs, set_message_security_data
from nvflare.security.logging import secure_format_exception


def _send_to_clients(admin_server, client_sites: List[str], engine, message, timeout=None, optional=False):
    pass


def _get_active_job_participants(connected_clients: Dict[str, Client], participants: Dict[str, Client]) -> List[str]:
    """Gets active job participants.

        Some clients might be dropped/dead during job execution.
        No need to abort those clients.

    Args:
        connected_clients: Clients that are currently connected.
        participants: Clients that were participating when the job started.

    Returns:
        A list of active job participants name.
    """
    pass


class JobRunner(FLComponent):
    def __init__(self, workspace_root: str) -> None:
        super().__init__()
        self.workspace_root = workspace_root
        self.ask_to_stop = False
        self.scheduler = None
        self.running_jobs = {}
        self.lock = threading.Lock()

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    @staticmethod
    def _make_deploy_message(job: Job, app_data, app_name, fl_ctx):
        pass

    def _deploy_job(self, job: Job, sites: dict, fl_ctx: FLContext) -> Tuple[str, list]:
        """Deploy the application to the list of participants

        Args:
            job: job to be deployed
            sites: participating sites
            fl_ctx: FLContext

        Returns:  job id, failed_clients

        """
        pass

    def _start_run(self, job_id: str, job: Job, client_sites: Dict[str, DispatchInfo], fl_ctx: FLContext):
        """Start the application

        Args:
            job_id: job_id
            client_sites: participating sites
            fl_ctx: FLContext
        """
        pass

    def _stop_run(self, job_id, fl_ctx: FLContext):
        """Stop the application

        Args:
            job_id: job_id to be stopped
            fl_ctx: FLContext
        """
        pass

    def abort_client_run(self, job_id, client_sites: List[str], fl_ctx):
        """Send the abort run command to the clients

        Args:
            job_id: job_id
            client_sites: Clients to be aborted
            fl_ctx: FLContext
        """
        pass

    def _delete_run(self, job_id, client_sites: List[str], fl_ctx: FLContext):
        """Deletes the run workspace

        Args:
            job_id: job_id
            client_sites: participating sites
            fl_ctx: FLContext
        """
        pass

    def _job_complete_process(self, engine):
        pass

    def _update_job_status(self, engine, job, job_manager, fl_ctx):
        pass

    def _save_workspace(self, fl_ctx: FLContext):
        pass

    def run(self, fl_ctx: FLContext):
        """Starts job runner."""
        pass

    @staticmethod
    def _check_job_status(job_manager, job_id, job_run_status, fl_ctx: FLContext):
        pass

    def stop(self):
        pass

    def restore_running_job(self, job_id: str, job_clients, snapshot, fl_ctx: FLContext):
        pass

    def update_abnormal_finished_jobs(self, running_job_ids, fl_ctx: FLContext):
        pass

    def update_unfinished_jobs(self, fl_ctx: FLContext):
        pass

    @staticmethod
    def _get_all_running_jobs(job_manager, fl_ctx):
        pass

    def stop_run(self, job_id: str, fl_ctx: FLContext):
        pass

    def stop_all_runs(self, fl_ctx: FLContext):
        pass

    def remove_running_job(self, job_id: str):
        pass
