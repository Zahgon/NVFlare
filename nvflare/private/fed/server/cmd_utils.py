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

from typing import List

from nvflare.apis.job_def import DEFAULT_STUDY, JobMetaKey
from nvflare.apis.server_engine_spec import ServerEngineSpec
from nvflare.fuel.hci.conn import Connection
from nvflare.fuel.hci.proto import MetaKey, MetaStatusValue, ReplyKeyword, make_meta
from nvflare.fuel.hci.server.authz import PreAuthzReturnCode
from nvflare.fuel.hci.server.constants import ConnProps
from nvflare.fuel.utils.admin_name_utils import is_valid_admin_client_name
from nvflare.private.fed.server.admin import FedAdminServer
from nvflare.security.study_registry import StudyRegistryService


class CommandUtil(object):

    TARGET_CLIENTS = "target_clients"
    TARGET_CLIENT_TOKENS = "target_client_tokens"
    TARGET_CLIENT_NAMES = "target_client_names"
    TARGET_TYPE = "target_type"

    TARGET_TYPE_CLIENT = "client"
    TARGET_TYPE_SERVER = "server"
    TARGET_TYPE_ALL = "all"

    JOB_ID = "job_id"
    JOB = "job"

    def _get_study_auth_context(self, conn: Connection):
        pass

    def _apply_study_role_for_authz(self, conn: Connection) -> bool:
        # Study membership is checked at session creation time. The certificate role remains
        # the effective role for study-scoped authorization, so there is nothing to substitute here.
        pass

    def command_authz_required(self, conn: Connection, args: List[str]) -> PreAuthzReturnCode:
        pass

    def authorize_client_operation(self, conn: Connection, args: List[str]) -> PreAuthzReturnCode:
        pass

    def validate_command_targets(self, conn: Connection, args: List[str]) -> str:
        """Validate specified args and determine and set target type and target names in the Connection.

        The args must be like this:

            target_type client_names ...

        where target_type is one of 'all', 'client', 'server'

        Args:
            conn: A Connection object.
            args: Specified arguments.

        Returns:
            An error message. It is empty "" if no error found.
        """
        pass

    def must_be_project_admin(self, conn: Connection, args: List[str]):
        # This helper intentionally checks the certificate role. project_admin-only operations
        # must stay scoped to the cert/global role.
        pass

    def authorize_server_operation(self, conn: Connection, args: List[str]):
        pass

    def send_request_to_clients(self, conn, message):
        pass

    @staticmethod
    def get_job_name(meta: dict) -> str:
        """Gets job name from job meta."""
        pass

    def process_replies_to_table(self, conn: Connection, replies):
        """Process the clients' replies and put in a table format.

        Args:
            conn: A Connection object.
            replies: replies from clients
        """
        pass

    def _process_replies_to_string(self, conn: Connection, replies) -> str:
        """Process the clients replies and put in a string format.

        Args:
            conn: A Connection object.
            replies: replies from clients

        Returns:
            A string response.
        """
        pass
