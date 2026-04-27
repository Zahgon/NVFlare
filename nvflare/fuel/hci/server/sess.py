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
import json
import threading
import time
import uuid
from typing import List

from nvflare.apis.job_def import DEFAULT_STUDY
from nvflare.fuel.f3.cellnet.defs import CellChannel
from nvflare.fuel.f3.message import Message as CellMessage
from nvflare.fuel.hci.base64_utils import b64str_to_str, str_to_b64str
from nvflare.fuel.hci.conn import Connection
from nvflare.fuel.hci.proto import InternalCommands, ReplyKeyword
from nvflare.fuel.hci.reg import CommandModule, CommandModuleSpec, CommandSpec
from nvflare.fuel.utils.time_utils import time_to_string
from nvflare.private.fed.utils.identity_utils import IdentityAsserter, TokenVerifier

LIST_SESSIONS_CMD_NAME = InternalCommands.LIST_SESSIONS
CHECK_SESSION_CMD_NAME = InternalCommands.CHECK_SESSION


class Session(object):
    def __init__(self, sess_id, user_name, org, role, origin_fqcn, active_study=DEFAULT_STUDY):
        """Object keeping track of an admin client session with token and time data."""
        self.sess_id = sess_id
        self.user_name = user_name
        self.user_org = org
        self.user_role = role
        self.active_study = active_study
        self.origin_fqcn = origin_fqcn
        self.start_time = time.time()
        self.last_active_time = time.time()

    def mark_active(self):
        pass

    def make_token(self, id_asserter: IdentityAsserter):
        pass

    @staticmethod
    def decode_token(token: str, id_asserter: IdentityAsserter = None):
        pass


class SessionManager(CommandModule):
    def __init__(self, cell, idle_timeout=1800, monitor_interval=5):
        """Session manager.

        Args:
            idle_timeout: session idle timeout
            monitor_interval: interval for obtaining updates when monitoring
        """
        if monitor_interval <= 0:
            monitor_interval = 5

        self.cell = cell
        self.sess_update_lock = threading.Lock()
        self.sessions = {}  # token => Session
        self.idle_timeout = idle_timeout
        self.monitor_interval = monitor_interval
        self.asked_to_stop = False
        self.monitor = threading.Thread(target=self.monitor_sessions)
        self.monitor.daemon = True
        self.monitor.start()

    def monitor_sessions(self):
        """Runs loop in a thread to end sessions that time out."""
        pass

    def shutdown(self):
        pass

    def create_session(self, user_name, user_org, user_role, origin_fqcn, active_study=DEFAULT_STUDY):
        """Creates new session with a new session token.

        Args:
            user_name: username for session
            user_org: org of the user
            user_role: user's role
            origin_fqcn: request origin FQCN
            id_asserter: used to sign session token

        Returns: Session

        """
        pass

    def recreate_session(self, token: str, origin_fqcn, id_asserter: IdentityAsserter):
        pass

    def get_session(self, token: str, id_asserter=None):
        pass

    def get_sessions(self):
        pass

    def end_session_by_token(self, token, reason=None):
        pass

    def end_session_by_id(self, sess_id: str, reason=None):
        pass

    def get_spec(self):
        pass

    def handle_list_sessions(self, conn: Connection, args: List[str]):
        """Lists sessions and the details in a table.

        Registered in the FedAdminServer with ``cmd_reg.register_module(sess_mgr)``.
        """
        pass

    def handle_check_session(self, conn: Connection, args: List[str]):
        pass
