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

import copy
import hashlib
import os
import random
import resource
import threading
import time
from abc import ABC
from typing import List, Union

from nvflare.fuel.f3.cellnet.cell import Cell
from nvflare.fuel.f3.cellnet.connector_manager import ConnectorData
from nvflare.fuel.f3.cellnet.core_cell import Message
from nvflare.fuel.f3.cellnet.defs import MessageHeaderKey, ReturnCode
from nvflare.fuel.f3.cellnet.fqcn import FQCN
from nvflare.fuel.f3.cellnet.utils import make_reply
from nvflare.fuel.f3.stats_pool import StatsPoolManager
from nvflare.fuel.utils.admin_name_utils import is_valid_admin_client_name
from nvflare.fuel.utils.config_service import ConfigService
from nvflare.fuel.utils.log_utils import get_obj_logger

_CHANNEL = "_net_manager"
_TOPIC_PEERS = "peers"
_TOPIC_CELLS = "cells"
_TOPIC_ROUTE = "route"
_TOPIC_START_ROUTE = "start_route"
_TOPIC_STOP = "stop"
_TOPIC_STOP_CELL = "stop_cell"
_TOPIC_URL_USE = "url_use"
_TOPIC_CONNS = "conns"
_TOPIC_SPEED = "speed"
_TOPIC_ECHO = "echo"
_TOPIC_STRESS = "stress"
_TOPIC_CHANGE_ROOT = "change_root"
_TOPIC_BULK_TEST = "bulk_test"
_TOPIC_BULK_ITEM = "bulk_item"
_TOPIC_MSG_STATS = "msg_stats"
_TOPIC_LIST_POOLS = "list_pools"
_TOPIC_SHOW_POOL = "show_pool"
_TOPIC_COMM_CONFIG = "comm_config"
_TOPIC_CONFIG_VARS = "config_vars"
_TOPIC_PROCESS_INFO = "process_info"
_TOPIC_HEARTBEAT = "heartbeat"

_ONE_K = bytes([1] * 1024)


class _Member:

    STATE_UNKNOWN = 0
    STATE_ONLINE = 1
    STATE_OFFLINE = 2

    def __init__(self, fqcn):
        self.fqcn = fqcn
        self.state = _Member.STATE_UNKNOWN
        self.last_heartbeat_time = time.time()
        self.lock = threading.Lock()


class SubnetMonitor(ABC):
    def __init__(self, subnet_id: str, member_cells: List[str], trouble_alert_threshold: float):
        if not member_cells:
            raise ValueError("member cells must not be empty")
        self.agent = None
        self.subnet_id = subnet_id
        self.trouble_alert_threshold = trouble_alert_threshold
        self.lock = threading.Lock()
        self.members = {}
        for m in member_cells:
            self.members[m] = _Member(m)

    def member_online(self, member_cell_fqcn: str):
        pass

    def member_offline(self, member_cell_fqcn: str):
        pass

    def put_member_online(self, member: _Member):
        pass

    def put_member_offline(self, member: _Member):
        pass

    def stop_subnet(self):
        pass


class NetAgent:
    def __init__(self, cell, change_root_cb=None, agent_closed_cb=None):
        if isinstance(cell, Cell):
            cell = cell.core_cell
        self.cell = cell
        self.change_root_cb = change_root_cb
        self.agent_closed_cb = agent_closed_cb
        self.logger = get_obj_logger(self)

        cell.register_request_cb(
            channel=_CHANNEL,
            topic=_TOPIC_CELLS,
            cb=self._do_report_cells,
        )

        cell.register_request_cb(
            channel=_CHANNEL,
            topic=_TOPIC_ROUTE,
            cb=self._do_route,
        )

        cell.register_request_cb(
            channel=_CHANNEL,
            topic=_TOPIC_START_ROUTE,
            cb=self._do_start_route,
        )

        cell.register_request_cb(
            channel=_CHANNEL,
            topic=_TOPIC_STOP,
            cb=self._do_stop,
        )

        cell.register_request_cb(
            channel=_CHANNEL,
            topic=_TOPIC_STOP_CELL,
            cb=self._do_stop_cell,
        )

        cell.register_request_cb(
            channel=_CHANNEL,
            topic=_TOPIC_PEERS,
            cb=self._do_peers,
        )

        cell.register_request_cb(
            channel=_CHANNEL,
            topic=_TOPIC_CONNS,
            cb=self._do_connectors,
        )

        cell.register_request_cb(
            channel=_CHANNEL,
            topic=_TOPIC_URL_USE,
            cb=self._do_url_use,
        )

        cell.register_request_cb(
            channel=_CHANNEL,
            topic=_TOPIC_SPEED,
            cb=self._do_speed,
        )

        cell.register_request_cb(
            channel=_CHANNEL,
            topic=_TOPIC_ECHO,
            cb=self._do_echo,
        )

        cell.register_request_cb(
            channel=_CHANNEL,
            topic=_TOPIC_STRESS,
            cb=self._do_stress,
        )

        cell.register_request_cb(
            channel=_CHANNEL,
            topic=_TOPIC_CHANGE_ROOT,
            cb=self._do_change_root,
        )

        cell.register_request_cb(
            channel=_CHANNEL,
            topic=_TOPIC_BULK_TEST,
            cb=self._do_bulk_test,
        )

        cell.register_request_cb(
            channel=_CHANNEL,
            topic=_TOPIC_BULK_ITEM,
            cb=self._do_bulk_item,
        )

        cell.register_request_cb(
            channel=_CHANNEL,
            topic=_TOPIC_MSG_STATS,
            cb=self._do_msg_stats,
        )

        cell.register_request_cb(
            channel=_CHANNEL,
            topic=_TOPIC_LIST_POOLS,
            cb=self._do_list_pools,
        )

        cell.register_request_cb(
            channel=_CHANNEL,
            topic=_TOPIC_SHOW_POOL,
            cb=self._do_show_pool,
        )

        cell.register_request_cb(
            channel=_CHANNEL,
            topic=_TOPIC_COMM_CONFIG,
            cb=self._do_comm_config,
        )

        cell.register_request_cb(
            channel=_CHANNEL,
            topic=_TOPIC_CONFIG_VARS,
            cb=self._do_config_vars,
        )

        cell.register_request_cb(
            channel=_CHANNEL,
            topic=_TOPIC_PROCESS_INFO,
            cb=self._do_process_info,
        )
        cell.register_request_cb(
            channel=_CHANNEL,
            topic=_TOPIC_HEARTBEAT,
            cb=self._do_heartbeat,
        )

        self.heartbeat_thread = None
        self.monitor_thread = None
        self.asked_to_close = False
        self.subnets = {}
        self.monitors = {}
        self.hb_lock = threading.Lock()
        self.monitor_lock = threading.Lock()

    def add_to_subnet(self, subnet_id: str, monitor_fqcn: str = FQCN.ROOT_SERVER):
        pass

    def add_subnet_monitor(self, monitor: SubnetMonitor):
        pass

    def stop_subnet(self, monitor: SubnetMonitor):
        pass

    def delete_subnet_monitor(self, subnet_id: str):
        pass

    def close(self):
        pass

    def _subnet_heartbeat(self):
        pass

    @staticmethod
    def _check_monitor(m: SubnetMonitor):
        pass

    def _monitor_subnet(self):
        pass

    def _do_heartbeat(self, request: Message) -> Union[None, Message]:
        pass

    def _do_stop(self, request: Message) -> Union[None, Message]:
        pass

    def _do_stop_cell(self, request: Message) -> Union[None, Message]:
        pass

    def _do_route(self, request: Message) -> Union[None, Message]:
        pass

    def _do_start_route(self, request: Message) -> Union[None, Message]:
        pass

    def _do_peers(self, request: Message) -> Union[None, Message]:
        pass

    def get_peers(self, target_fqcn: str) -> (Union[None, dict], List[str]):
        pass

    @staticmethod
    def _connector_info(info: ConnectorData) -> dict:
        pass

    def _get_connectors(self) -> dict:
        pass

    def _do_connectors(self, request: Message) -> Union[None, Message]:
        pass

    def get_connectors(self, target_fqcn: str) -> (dict, dict):
        pass

    def request_cells_info(self) -> (str, List[str]):
        pass

    def _get_url_use_of_cell(self, url: str):
        pass

    def get_url_use(self, url) -> dict:
        pass

    def _do_url_use(self, request: Message) -> Union[None, Message]:
        pass

    def get_route_info(self, target_fqcn: str) -> (dict, dict):
        pass

    def start_route(self, from_fqcn: str, target_fqcn: str) -> (str, dict, dict):
        pass

    def _do_report_cells(self, request: Message) -> Union[None, Message]:
        pass

    def stop(self):
        # ask all children to stop
        pass

    def stop_cell(self, target: str) -> str:
        pass

    def _request_speed_test(self, target_fqcn: str, num, size) -> Message:
        pass

    def _do_speed(self, request: Message) -> Union[None, Message]:
        pass

    def _do_echo(self, request: Message) -> Union[None, Message]:
        pass

    def _do_stress_test(self, params):
        pass

    def _do_stress(self, request: Message) -> Union[None, Message]:
        pass

    def start_stress_test(self, targets: list, num_rounds=10, timeout=5.0):
        pass

    def speed_test(self, from_fqcn: str, to_fqcn: str, num_tries, payload_size) -> dict:
        pass

    def change_root(self, new_root_url: str):
        pass

    def _do_change_root(self, request: Message) -> Union[None, Message]:
        pass

    def start_bulk_test(self, targets: list, size: int):
        pass

    def _do_bulk_test(self, request: Message) -> Union[None, Message]:
        pass

    def _do_bulk_item(self, request: Message) -> Union[None, Message]:
        pass

    def get_msg_stats_table(self, target: str, mode: str):
        pass

    def _do_msg_stats(self, request: Message) -> Union[None, Message]:
        pass

    def get_pool_list(self, target: str):
        pass

    def _do_list_pools(self, request: Message) -> Union[None, Message]:
        pass

    def show_pool(self, target: str, pool_name: str, mode: str):
        pass

    def _do_show_pool(self, request: Message) -> Union[None, Message]:
        pass

    def get_comm_config(self, target: str):
        pass

    def get_config_vars(self, target: str):
        pass

    def get_process_info(self, target: str):
        pass

    def _do_comm_config(self, request: Message) -> Union[None, Message]:
        pass

    def _do_config_vars(self, request: Message) -> Union[None, Message]:
        pass

    def _do_process_info(self, request: Message) -> Union[None, Message]:

        pass

    def _broadcast_to_subs(self, topic: str, message=None, timeout=1.0):
        pass
