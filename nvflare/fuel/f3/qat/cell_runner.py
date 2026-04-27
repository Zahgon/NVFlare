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

import os
import shlex
import subprocess
import sys
import threading
import time

from nvflare.fuel.f3.cellnet.core_cell import CellAgent, CoreCell, Message, MessageHeaderKey, MessageType
from nvflare.fuel.f3.cellnet.fqcn import FQCN
from nvflare.fuel.f3.cellnet.net_agent import NetAgent
from nvflare.fuel.f3.mpm import MainProcessMonitor
from nvflare.fuel.f3.stats_pool import StatsPoolManager

from .net_config import NetConfig


class _RunnerInfo:
    def __init__(self, name: str, fqcn: str, process):
        self.name = name
        self.fqcn = fqcn
        self.process = process


class CellRunner:
    def __init__(
        self,
        config_path: str,
        config_file: str,
        my_name: str,
        parent_url: str = "",
        parent_fqcn: str = "",
        log_level: str = "info",
    ):
        self.new_root_url = None
        self.config_path = config_path
        self.config_file = config_file
        self.log_level = log_level
        self.waiter = threading.Event()

        if not parent_fqcn:
            my_fqcn = my_name
        else:
            my_fqcn = FQCN.join([parent_fqcn, my_name])

        net_config = NetConfig(config_file)
        self.root_url = net_config.get_root_url()
        self.children = net_config.get_children(my_name)
        self.clients = net_config.get_clients()
        self.create_internal_listener = self.children and len(self.children) > 0

        self.cell = CoreCell(
            fqcn=my_fqcn,
            root_url=self.root_url,
            secure=False,
            credentials={},
            create_internal_listener=self.create_internal_listener,
            parent_url=parent_url,
        )
        self.agent = NetAgent(
            self.cell,
            self._change_root,
            self._agent_closed,
        )

        self.child_runners = {}
        self.client_runners = {}

        self.cell.set_cell_connected_cb(cb=self._cell_connected)
        self.cell.set_cell_disconnected_cb(cb=self._cell_disconnected)
        self.cell.add_incoming_reply_filter(channel="*", topic="*", cb=self._filter_incoming_reply)
        self.cell.add_incoming_request_filter(channel="*", topic="*", cb=self._filter_incoming_request)
        self.cell.add_outgoing_reply_filter(channel="*", topic="*", cb=self._filter_outgoing_reply)
        self.cell.add_outgoing_request_filter(channel="*", topic="*", cb=self._filter_outgoing_request)
        self.cell.set_message_interceptor(cb=self._inspect_message)
        # MainProcessMonitor.add_run_monitor(self._check_new_root)

    def _inspect_message(self, message: Message):
        pass

    def _cell_connected(self, connected_cell: CellAgent):
        pass

    def _cell_disconnected(self, disconnected_cell: CellAgent):
        pass

    def _filter_incoming_reply(self, message: Message):
        pass

    def _filter_incoming_request(self, message: Message):
        pass

    def _filter_outgoing_reply(self, message: Message):
        pass

    def _filter_outgoing_request(self, message: Message):
        pass

    def _create_subprocess(self, name: str, parent_fqcn: str, parent_url: str, start_it=True):
        pass

    def start(self, start_all=True):
        pass

    def stop(self):
        # self.agent.stop()
        pass

    def _agent_closed(self):
        pass

    def _change_root(self, url: str):
        pass

    def dump_stats(self):
        pass

    def run(self):
        pass
