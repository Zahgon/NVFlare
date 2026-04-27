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
import os
import pathlib
import shutil
import tempfile
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

from nvflare.apis.client_engine_spec import ClientEngineSpec
from nvflare.apis.fl_context import FLContext
from nvflare.apis.job_def import Job, JobDataKey, JobMetaKey, job_from_meta, new_job_id
from nvflare.apis.job_def_manager_spec import JobDefManagerSpec, RunStatus
from nvflare.apis.server_engine_spec import ServerEngineSpec
from nvflare.apis.storage import WORKSPACE, StorageException, StorageSpec
from nvflare.fuel.utils import fobs
from nvflare.fuel.utils.zip_utils import unzip_all_from_bytes, zip_directory_to_bytes

_OBJ_TAG_SCHEDULED = "scheduled"


class JobInfo:
    def __init__(self, meta: dict, job_id: str, uri: str):
        self.meta = meta
        self.job_id = job_id
        self.uri = uri


class _JobFilter(ABC):
    @abstractmethod
    def filter_job(self, info: JobInfo) -> bool:
        pass


class _StatusFilter(_JobFilter):
    def __init__(self, status_to_check):
        self.result = []
        if not isinstance(status_to_check, list):
            # turning to list
            status_to_check = [status_to_check]
        self.status_to_check = status_to_check

    def filter_job(self, info: JobInfo):
        pass


class _AllJobsFilter(_JobFilter):
    def __init__(self):
        self.result = []

    def filter_job(self, info: JobInfo):
        pass


class _ReviewerFilter(_JobFilter):
    def __init__(self, reviewer_name):
        """Not used yet, for use in future implementations."""
        self.result = []
        self.reviewer_name = reviewer_name

    def filter_job(self, info: JobInfo):
        pass


class _ScheduleJobFilter(_JobFilter):
    """
    This filter is optimized for selecting jobs to schedule since it is used so frequently (every 1 sec).
    """

    def __init__(self, store):
        self.store = store
        self.result = []

    def filter_job(self, info: JobInfo):
        pass


class SimpleJobDefManager(JobDefManagerSpec):
    def __init__(self, uri_root: str = "jobs", job_store_id: str = "job_store"):
        super().__init__()
        self.uri_root = uri_root

        # if env var is defined, use it to override uri_root!
        job_store_root = os.environ.get("NVFL_JOB_STORE_ROOT")
        if job_store_root:
            self.uri_root = job_store_root

        os.makedirs(uri_root, exist_ok=True)
        self.job_store_id = job_store_id

    def _get_job_store(self, fl_ctx):
        pass

    def job_uri(self, jid: str):
        pass

    def create(self, meta: dict, uploaded_content: Union[str, bytes], fl_ctx: FLContext) -> Dict[str, Any]:
        # validate meta to make sure it has:
        pass

    def clone(self, from_jid: str, meta: dict, fl_ctx: FLContext) -> Dict[str, Any]:
        pass

    def delete(self, jid: str, fl_ctx: FLContext):
        pass

    def _validate_meta(self, meta):
        """Validate meta

        Args:
            meta: meta to validate

        Returns:

        """
        pass

    def _validate_uploaded_content(self, uploaded_content) -> bool:
        """Validate uploaded content for creating a run config. (THIS NEEDS TO HAPPEN BEFORE CONTENT IS PROVIDED NOW)

        Internally used by create and update.

        1. check all sites in deployment are in resources
        2. each site in deployment need to have resources (each site in resource need to be in deployment ???)
        """
        pass

    def get_job(self, jid: str, fl_ctx: FLContext) -> Optional[Job]:
        pass

    def set_results_uri(self, jid: str, result_uri: str, fl_ctx: FLContext):
        pass

    def get_app(self, job: Job, app_name: str, fl_ctx: FLContext) -> bytes:
        pass

    def _load_job_data_from_store(self, job: Job, temp_dir: str, fl_ctx: FLContext):
        pass

    def get_content(self, meta: dict, fl_ctx: FLContext) -> Optional[bytes]:
        pass

    def set_client_data(self, jid: str, data: Union[bytes, str], client_name: str, data_type: str, fl_ctx: FLContext):
        pass

    def get_client_data(self, jid: str, client_name: str, data_type: str, fl_ctx: FLContext) -> Optional[bytes]:
        pass

    def list_components(self, jid: str, fl_ctx: FLContext) -> List[str]:
        pass

    def set_status(self, jid: str, status: RunStatus, fl_ctx: FLContext):
        pass

    def update_meta(self, jid: str, meta, fl_ctx: FLContext):
        pass

    def refresh_meta(self, job: Job, meta_keys: list, fl_ctx: FLContext):
        """Refresh meta of the job as specified in the meta keys
        Save the values of the specified keys into job store

        Args:
            job: job object
            meta_keys: meta keys need to updated
            fl_ctx: FLContext

        """
        pass

    def get_all_jobs(self, fl_ctx: FLContext) -> List[Job]:
        pass

    def get_jobs_to_schedule(self, fl_ctx: FLContext) -> List[Job]:
        pass

    def _scan(self, job_filter: _JobFilter, fl_ctx: FLContext, skip_tag=None):
        pass

    def get_jobs_by_status(self, status: Union[RunStatus, List[RunStatus]], fl_ctx: FLContext) -> List[Job]:
        """Get jobs that are in the specified status

        Args:
            status: a single status value or a list of status values
            fl_ctx: the FL context

        Returns: list of jobs that are in specified status

        """
        pass

    def get_jobs_waiting_for_review(self, reviewer_name: str, fl_ctx: FLContext) -> List[Job]:
        pass

    def set_approval(
        self, jid: str, reviewer_name: str, approved: bool, note: str, fl_ctx: FLContext
    ) -> Dict[str, Any]:
        pass

    def save_workspace(self, jid: str, data: Union[bytes, str, List[str]], fl_ctx: FLContext):
        pass

    def get_storage_component(self, jid: str, component: str, fl_ctx: FLContext):
        pass

    def get_storage_for_download(
        self, jid: str, download_dir: str, component: str, download_file: str, fl_ctx: FLContext
    ):
        """Prepares the specified component of the job for download at the specified directory

        The component is prepared for download at download_dir/jid/download_file.

        Args:
            jid: job ID
            download_dir: directory to download the component to
            component: component name
            download_file: file name to save the downloaded component
            fl_ctx: FLContext
        """
        pass
