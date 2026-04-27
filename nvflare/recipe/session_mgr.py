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
import tempfile
from typing import Dict, Optional

from nvflare.fuel.flare_api.api_spec import MonitorReturnCode
from nvflare.fuel.flare_api.flare_api import Session, new_secure_session
from nvflare.job_config.api import FedJob


def _job_monitor_callback(session: Session, job_id: str, job_meta, *cb_args, **cb_kwargs) -> bool:
    """Shared callback to print job meta during monitoring."""
    pass


class SessionManager:
    """Centralized session management for POC and Production environments.

    Handles all session operations including job submission, monitoring, and lifecycle management.
    Implements session caching to avoid multiple login/logout cycles.
    """

    def __init__(self, session_params: Dict[str, any]):
        self.session_params = session_params

    def _get_session(self):
        """Context manager that provides a session, with optional caching."""
        pass

    def submit_job(self, job: FedJob) -> str:
        """Submit a job and return job ID."""
        pass

    def get_job_status(self, job_id: str) -> Optional[str]:
        """Get the status of the job."""
        pass

    def abort_job(self, job_id: str) -> None:
        """Abort the running job."""
        pass

    def get_job_result(self, job_id: str, timeout: float = 0.0) -> Optional[str]:
        """Get the result workspace of the job."""
        pass
