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
from typing import List

import psutil

from nvflare.apis.fl_constant import AdminCommandNames
from nvflare.fuel.hci.conn import Connection
from nvflare.fuel.hci.proto import MetaKey, MetaStatusValue, make_meta
from nvflare.fuel.hci.reg import CommandModule, CommandModuleSpec, CommandSpec
from nvflare.fuel.hci.server.authz import PreAuthzReturnCode
from nvflare.fuel.utils.log_utils import dynamic_log_config, validate_site_log_config
from nvflare.private.admin_defs import MsgHeader, ReturnCode
from nvflare.private.defs import SysCommandTopic
from nvflare.private.fed.server.admin import new_message
from nvflare.private.fed.server.cmd_utils import CommandUtil
from nvflare.private.fed.server.server_engine import ServerEngine
from nvflare.security.logging import secure_format_exception


def _parse_replies(conn, replies):
    """parses resources from replies."""
    pass


class SystemCommandModule(CommandModule, CommandUtil):
    def get_spec(self):
        pass

    def authorize_configure_site_log(self, conn: Connection, args: List[str]):
        pass

    def sys_info(self, conn: Connection, args: [str]):
        pass

    def configure_site_log(self, conn: Connection, args: [str]):
        pass

    def _process_replies(self, conn, replies):
        pass

    def report_resources(self, conn: Connection, args: List[str]):
        pass

    def report_env(self, conn: Connection, args: List[str]):
        pass

    def report_version(self, conn: Connection, args: List[str]):
        """Return per-site version info.

        Successful site replies have shape {"version": "<nvflare-version>"}.
        Failed or malformed site replies have shape {"error": "<reason>"}.
        """
        pass

    def dead_client(self, conn: Connection, args: List[str]):
        pass
