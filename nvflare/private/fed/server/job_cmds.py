# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
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

import datetime
import json
import os
import shutil
import uuid
from collections import deque
from typing import Dict, List

import nvflare.fuel.hci.file_transfer_defs as ftd
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import AdminCommandNames, FLContextKey, ReturnCode, ServerCommandKey, WorkspaceConstants
from nvflare.apis.job_def import (
    ALL_SITES,
    DEFAULT_STUDY,
    SERVER_SITE_NAME,
    Job,
    JobMetaKey,
    get_job_meta_study,
    is_valid_job_id,
)
from nvflare.apis.job_def_manager_spec import JobDefManagerSpec, RunStatus
from nvflare.apis.shareable import Shareable
from nvflare.apis.storage import DATA, JOB_ZIP, META, META_JSON, WORKSPACE, WORKSPACE_ZIP, StorageSpec
from nvflare.fuel.hci.conn import Connection
from nvflare.fuel.hci.proto import ConfirmMethod, MetaKey, MetaStatusValue, make_meta
from nvflare.fuel.hci.reg import CommandModule, CommandModuleSpec, CommandSpec
from nvflare.fuel.hci.server.authz import PreAuthzReturnCode
from nvflare.fuel.hci.server.binary_transfer import BinaryTransfer
from nvflare.fuel.hci.server.constants import ConnProps
from nvflare.fuel.utils.argument_utils import SafeArgumentParser
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.private.defs import RequestHeader, TrainingTopic
from nvflare.private.fed.server.admin import new_message
from nvflare.private.fed.server.job_meta_validator import JobMetaValidator
from nvflare.private.fed.server.server_engine import ServerEngine
from nvflare.private.fed.server.server_engine_internal_spec import ServerEngineInternalSpec
from nvflare.private.fed.utils.fed_utils import extract_participants
from nvflare.security.logging import secure_format_exception, secure_log_traceback
from nvflare.security.study_registry import StudyRegistryService

from .cmd_utils import CommandUtil

CLONED_META_KEYS = {
    JobMetaKey.JOB_NAME.value,
    JobMetaKey.JOB_FOLDER_NAME.value,
    JobMetaKey.DEPLOY_MAP.value,
    JobMetaKey.RESOURCE_SPEC.value,
    JobMetaKey.CONTENT_LOCATION.value,
    JobMetaKey.RESULT_LOCATION.value,
    JobMetaKey.APPROVALS.value,
    JobMetaKey.MIN_CLIENTS.value,
    JobMetaKey.MANDATORY_CLIENTS.value,
    JobMetaKey.DATA_STORAGE_FORMAT.value,
    JobMetaKey.STUDY.value,
}


def _create_list_job_cmd_parser():
    pass


def _create_get_job_log_cmd_parser():
    pass


class JobCommandModule(CommandModule, CommandUtil, BinaryTransfer):
    """Command module with commands for job management."""

    MAX_RETURNED_JOB_LOG_BYTES = 5 * 1024 * 1024
    MAX_RETURNED_JOB_LOG_LINES = 10000

    def __init__(self):
        super().__init__()
        self.logger = get_obj_logger(self)

    def get_spec(self):
        pass

    def authorize_job_file(self, conn: Connection, args: List[str]):
        """
        Args: cmd_name tx_id job_id file_name [end]
        """
        pass

    def authorize_job_id(self, conn: Connection, args: List[str]):
        pass

    def authorize_job(self, conn: Connection, args: List[str]):
        pass

    def authorize_configure_job_log(self, conn: Connection, args: List[str]):
        pass

    def delete_job_id(self, conn: Connection, args: List[str]):
        pass

    def configure_job_log(self, conn: Connection, args: List[str]):
        pass

    def list_jobs(self, conn: Connection, args: List[str]):
        pass

    def delete_job(self, conn: Connection, args: List[str]):
        pass

    def get_job_meta(self, conn: Connection, args: List[str]):
        pass

    def get_job_log(self, conn: Connection, args: List[str]):
        pass

    def _collect_job_log_lines(self, log_file: str, tail_lines=None, grep_pattern=None):
        pass

    def list_job_components(self, conn: Connection, args: List[str]):
        pass

    def abort_job(self, conn: Connection, args: List[str]):
        pass

    def clone_job(self, conn: Connection, args: List[str]):
        pass

    @staticmethod
    def _job_match(job_meta: Dict, id_prefix: str, name_prefix: str, user_name: str, requested_study: str) -> bool:
        pass

    @staticmethod
    def _send_detail_list(conn: Connection, jobs: List[Job]):
        pass

    @staticmethod
    def _send_summary_list(conn: Connection, jobs: List[Job]):
        pass

    @staticmethod
    def _set_duration(job):
        pass

    def submit_job(self, conn: Connection, args: List[str]):
        pass

    def _clean_up_download(self, conn: Connection, tx_id: str):
        """
        Remove the job download folder
        """
        pass

    def _download_job_comps(self, conn: Connection, args: List[str], get_comps_f):
        """
        Job download uses binary protocol for more efficient download.
        - Retrieve job data from job store. This puts job files (meta, data, and workspace) in a transfer folder
        - Returns job file names, a TX ID, and a command name for downloading files to the admin client
        - Admin client downloads received file names one by one. It signals the end of download in the last command.
        """
        pass

    def _get_default_job_components(self, job_def_manager, job_id, fl_ctx):
        pass

    def download_job(self, conn: Connection, args: List[str]):
        """
        Job download uses binary protocol for more efficient download.
        - Retrieve job data from job store. This puts job files (meta, data, and workspace) in a transfer folder
        - Returns job file names, a TX ID, and a command name for downloading files to the admin client
        - Admin client downloads received file names one by one. It signals the end of download in the last command.
        """
        pass

    def download_job_components(self, conn: Connection, args: List[str]):
        """Download additional job components (e.g., ERRORLOG_site-1) for a specified job.

        Based on job download but downloads the additional components for a job that job download does
        not download.
        """
        pass

    def _get_extra_job_components(self, job_def_manager, job_id, fl_ctx):
        pass

    def do_app_command(self, conn: Connection, args: List[str]):
        # cmd job_id topic
        pass
