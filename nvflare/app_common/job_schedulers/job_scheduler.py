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
import threading
import time
from typing import Dict, List, Optional, Tuple

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.job_def import ALL_SITES, SERVER_SITE_NAME, Job, JobMetaKey, RunStatus, get_job_meta_study
from nvflare.apis.job_def_manager_spec import JobDefManagerSpec
from nvflare.apis.job_scheduler_spec import DispatchInfo, JobSchedulerSpec
from nvflare.apis.server_engine_spec import ServerEngineSpec
from nvflare.private.fed.utils.fed_utils import extract_participants
from nvflare.security.study_registry import StudyRegistryService
from nvflare.utils.job_launcher_utils import get_site_launcher_spec

SCHEDULE_RESULT_OK = 0  # the job is scheduled
SCHEDULE_RESULT_NO_RESOURCE = 1  # job is not scheduled due to lack of resources
SCHEDULE_RESULT_BLOCK = 2  # job is to be blocked from scheduled again due to fatal error


class DefaultJobScheduler(JobSchedulerSpec, FLComponent):
    def __init__(
        self,
        max_jobs: int = 1,
        max_schedule_count: int = 10,
        min_schedule_interval: float = 10.0,
        max_schedule_interval: float = 600.0,
    ):
        """
        Create a DefaultJobScheduler
        Args:
            max_jobs: max number of concurrent jobs allowed
            max_schedule_count: max number of times to try to schedule a job
            min_schedule_interval: min interval between two schedules
            max_schedule_interval: max interval between two schedules
        """
        super().__init__()
        self.max_jobs = max_jobs
        self.max_schedule_count = max_schedule_count
        self.min_schedule_interval = min_schedule_interval
        self.max_schedule_interval = max_schedule_interval
        self.scheduled_jobs = []
        self.lock = threading.Lock()

    def _check_client_resources(
        self, job: Job, resource_reqs: Dict[str, dict], fl_ctx: FLContext
    ) -> Dict[str, Tuple[bool, str]]:
        """Checks resources on each site.

        Args:
            resource_reqs (dict): {client_name: resource_requirements}

        Returns:
            A dict of {client_name: client_check_result}.
                client_check_result is a tuple of (is_resource_enough, token);
                is_resource_enough is a bool indicates whether there is enough resources;
                token is for resource reservation / cancellation for this check request.
        """
        pass

    def _cancel_resources(
        self, resource_reqs: Dict[str, dict], resource_check_results: Dict[str, Tuple[bool, str]], fl_ctx: FLContext
    ):
        """Cancels any reserved resources based on resource check results.

        Args:
            resource_reqs (dict): {client_name: resource_requirements}
            resource_check_results: A dict of {client_name: client_check_result}
                where client_check_result is a tuple of {is_resource_enough, resource reserve token if any}
            fl_ctx: FL context
        """
        pass

    def _try_job(self, job: Job, fl_ctx: FLContext) -> (int, Optional[Dict[str, DispatchInfo]], str):
        pass

    def _exceed_max_jobs(self, fl_ctx: FLContext) -> bool:
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def schedule_job(
        self, job_manager: JobDefManagerSpec, job_candidates: List[Job], fl_ctx: FLContext
    ) -> (Optional[Job], Optional[Dict[str, DispatchInfo]]):
        pass

    def _get_update_meta_keys(self):
        pass

    def _update_schedule_history(self, job: Job, result: str, fl_ctx: FLContext):
        pass

    def _do_schedule_job(
        self, job_candidates: List[Job], fl_ctx: FLContext, failed_jobs: list, blocked_jobs: list
    ) -> (Optional[Job], Optional[Dict[str, DispatchInfo]]):
        pass

    def restore_scheduled_job(self, job_id: str):
        pass

    def remove_scheduled_job(self, job_id: str):
        pass
