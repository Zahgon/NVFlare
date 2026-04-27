# Copyright (c) 2023, NVIDIA CORPORATION.  All rights reserved.
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
from nvflare.apis.fl_constant import ReservedTopic
from nvflare.fuel.data_event.data_bus import DataBus
from nvflare.fuel.f3.cellnet.fqcn import FQCN
from nvflare.fuel.f3.cellnet.net_agent import NetAgent
from nvflare.fuel.f3.stats_pool import VALID_HIST_MODES, parse_hist_mode
from nvflare.fuel.hci.conn import Connection
from nvflare.fuel.hci.reg import CommandModule, CommandModuleSpec, CommandSpec
from nvflare.fuel.hci.server.constants import ConnProps
from nvflare.security.logging import secure_format_exception


def _to_int(s: str):
    pass


class NetManager(CommandModule):
    def __init__(self, agent: NetAgent, diagnose=False):
        self.agent = agent
        self.diagnose = diagnose
        data_bus = DataBus()
        data_bus.subscribe([ReservedTopic.STOP_CELLNET], self._stop_cellnet)

    def _stop_cellnet(self, topic: str, conn: Connection, db: DataBus):
        pass

    def get_spec(self) -> CommandModuleSpec:
        pass

    def _cmd_cells(self, conn: Connection, args: [str]):
        pass

    def _cmd_url_use(self, conn: Connection, args: [str]):
        pass

    def _cmd_route(self, conn: Connection, args: [str]):
        pass

    def _cmd_peers(self, conn: Connection, args: [str]):
        pass

    def _cmd_connectors(self, conn: Connection, args: [str]):
        pass

    def _cmd_speed_test(self, conn: Connection, args: [str]):
        pass

    def _cmd_stress_test(self, conn: Connection, args: [str]):
        pass

    def _cmd_bulk_test(self, conn: Connection, args: [str]):
        pass

    @staticmethod
    def _show_table_dict(conn: Connection, d: dict):
        pass

    def _cmd_msg_stats(self, conn: Connection, args: [str]):
        pass

    def _cmd_show_pool(self, conn: Connection, args: [str]):
        pass

    def _cmd_list_pools(self, conn: Connection, args: [str]):
        pass

    def _cmd_show_comm_config(self, conn: Connection, args: [str]):
        pass

    def _cmd_show_config_vars(self, conn: Connection, args: [str]):
        pass

    def _cmd_process_info(self, conn: Connection, args: [str]):
        pass

    def _cmd_change_root(self, conn: Connection, args: [str]):
        pass

    def _cmd_stop_net(self, conn: Connection, args: [str]):
        pass

    def _cmd_stop_cell(self, conn: Connection, args: [str]):
        pass
