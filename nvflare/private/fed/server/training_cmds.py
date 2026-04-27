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
import time
from typing import List

from nvflare.apis.client import Client
from nvflare.apis.fl_constant import AdminCommandNames, ReservedTopic, SiteType
from nvflare.fuel.data_event.data_bus import DataBus
from nvflare.fuel.hci.conn import Connection
from nvflare.fuel.hci.proto import ConfirmMethod, MetaKey, MetaStatusValue, ReplyKeyword, make_meta
from nvflare.fuel.hci.reg import CommandModule, CommandModuleSpec, CommandSpec
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.private.admin_defs import MsgHeader, ReturnCode
from nvflare.private.defs import ClientStatusKey, ScopeInfoKey, TrainingTopic
from nvflare.private.fed.server.admin import new_message
from nvflare.private.fed.server.server_engine_internal_spec import ServerEngineInternalSpec
from nvflare.private.fed.utils.fed_utils import get_scope_info
from nvflare.security.logging import secure_format_exception

from .cmd_utils import CommandUtil
from .server_engine import ServerEngine


def _server_status_value(engine: ServerEngineInternalSpec) -> str:
    pass


class TrainingCommandModule(CommandModule, CommandUtil):
    def __init__(self):
        """A class for training commands."""
        super().__init__()
        self.logger = get_obj_logger(self)

    def get_spec(self):
        pass

    # Shutdown
    def _shutdown_app_on_server(self, conn: Connection) -> str:
        pass

    def _shutdown_app_on_clients(self, conn: Connection) -> bool:
        pass

    def shutdown(self, conn: Connection, args: List[str]):
        pass

    # Remove Clients
    def remove_client(self, conn: Connection, args: List[str]):
        pass

    # Restart
    def _restart_clients(self, conn) -> str:
        pass

    def restart(self, conn: Connection, args: List[str]):
        pass

    # Check status
    def check_status(self, conn: Connection, args: List[str]):
        # TODO:: Need more discussion on what status to be shown
        pass

    def _process_client_status_replies(self, conn, replies):
        pass

    def _add_scope_info(self, table, site_name, scope_names: List[str], default_scope: str):
        pass

    def _process_scope_replies(self, table, conn, replies):
        pass

    def show_scopes(self, conn: Connection, args: List[str]):
        pass
