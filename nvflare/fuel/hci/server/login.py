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
import traceback
from typing import List

from nvflare.apis.job_def import DEFAULT_STUDY
from nvflare.apis.utils.format_check import name_check
from nvflare.fuel.f3.cellnet.defs import MessageHeaderKey
from nvflare.fuel.f3.message import Message as CellMessage
from nvflare.fuel.hci.conn import Connection
from nvflare.fuel.hci.proto import InternalCommands, ReplyKeyword
from nvflare.fuel.hci.reg import CommandModule, CommandModuleSpec, CommandSpec
from nvflare.fuel.hci.security import IdentityKey, get_identity_info
from nvflare.fuel.hci.server.constants import ConnProps
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.lighter.utils import cert_to_dict, load_crt_bytes
from nvflare.security.logging import secure_format_exception
from nvflare.security.study_registry import StudyRegistryService

from .reg import CommandFilter
from .sess import Session, SessionManager


class LoginModule(CommandModule, CommandFilter):
    def __init__(self, sess_mgr: SessionManager):
        """Login module.

        CommandModule containing the login commands to handle login and logout of admin clients, as well as the
        CommandFilter pre_command to check that a client is logged in with a valid session.

        Args:
            sess_mgr: SessionManager
        """
        if not isinstance(sess_mgr, SessionManager):
            raise TypeError("sess_mgr must be SessionManager but got {}.".format(type(sess_mgr)))

        self.session_mgr = sess_mgr
        self.logger = get_obj_logger(self)

    def get_spec(self):
        pass

    def handle_cert_login(self, conn: Connection, args: List[str]):
        def _reject(reason: str='', code: str=''):
            pass
        pass

    def handle_logout(self, conn: Connection, args: List[str]):
        pass

    def pre_command(self, conn: Connection, args: List[str]):
        pass

    def close(self):
        pass
