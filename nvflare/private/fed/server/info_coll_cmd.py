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

from nvflare.apis.fl_constant import AdminCommandNames
from nvflare.fuel.hci.conn import Connection
from nvflare.fuel.hci.proto import MetaStatusValue, make_meta
from nvflare.fuel.hci.reg import CommandModuleSpec, CommandSpec
from nvflare.fuel.hci.server.authz import PreAuthzReturnCode
from nvflare.fuel.hci.server.constants import ConnProps
from nvflare.private.defs import InfoCollectorTopic, RequestHeader
from nvflare.private.fed.server.admin import new_message
from nvflare.private.fed.server.server_engine_internal_spec import ServerEngineInternalSpec
from nvflare.widgets.info_collector import InfoCollector
from nvflare.widgets.widget import WidgetID

from .cmd_utils import CommandUtil
from .job_cmds import JobCommandModule


class InfoCollectorCommandModule(JobCommandModule, CommandUtil):
    """This class is for server side info collector commands.

    NOTE: we only support Server side info collector commands for now,
    due to the complexity of client-side process/child-process architecture.
    """

    CONN_KEY_COLLECTOR = "collector"

    def get_spec(self):
        pass

    def authorize_info_collection(self, conn: Connection, args: List[str]):
        pass

    def show_stats(self, conn: Connection, args: List[str]):
        pass

    def _collect_stats(self, conn: Connection, args: List[str], stats_func, msg_topic):
        pass

    def show_errors(self, conn: Connection, args: List[str]):
        pass

    def reset_errors(self, conn: Connection, args: List[str]):
        pass

    @staticmethod
    def _process_stats_replies(conn, replies, result: dict):
        pass
