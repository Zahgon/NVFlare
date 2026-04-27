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

import os
import uuid
from datetime import datetime

EXCLUDED_ACTIONS = {
    "scheduler.check_resource",
    "_check_session",
    "_commands",
    "__aux_command__",
}


class Auditor(object):
    def __init__(self, audit_file_name: str):
        """Manages the audit file to log events.

        Args:
            audit_file_name (str): the location to save audit log file
        """
        assert isinstance(audit_file_name, str), "audit_file_name must be str"
        if os.path.exists(audit_file_name):
            assert os.path.isfile(audit_file_name), "audit_file_name is not a valid file"

        # create/open the file
        self.audit_file = open(audit_file_name, "a")

    def add_event(self, user: str, action: str, ref: str = "", msg: str = "") -> str:

        pass

    def add_job_event(
        self, job_id: str, scope_name: str = "", task_name: str = "", task_id: str = "", ref: str = "", msg: str = ""
    ) -> str:
        pass

    def close(self):
        pass


class AuditService(object):
    """Service for interacting with Auditor to add events to log."""

    the_auditor = None

    @staticmethod
    def initialize(audit_file_name: str):
        pass

    @staticmethod
    def get_auditor():
        pass

    @staticmethod
    def add_event(user: str, action: str, ref: str = "", msg: str = "") -> str:
        pass

    @staticmethod
    def add_job_event(
        job_id: str, scope_name: str = "", task_name: str = "", task_id: str = "", ref: str = "", msg: str = ""
    ) -> str:
        pass

    @staticmethod
    def close():
        pass
