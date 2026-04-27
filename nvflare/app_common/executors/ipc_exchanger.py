# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
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

import threading
import time
from typing import Union

from nvflare.apis.dxo import DXO, DataKind, from_shareable
from nvflare.apis.event_type import EventType
from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReturnCode, Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.app_common.app_constant import AppConstants
from nvflare.client.ipc import defs
from nvflare.fuel.f3.cellnet.cell import Cell, Message, MessageHeaderKey
from nvflare.fuel.f3.cellnet.cell import ReturnCode as CellReturnCode
from nvflare.fuel.f3.cellnet.utils import make_reply as make_cell_reply
from nvflare.security.logging import secure_format_traceback

_SHORT_SLEEP_TIME = 0.2


class _TaskContext:
    def __init__(self, task_name: str, task_id: str, fl_ctx: FLContext):
        self.task_id = task_id
        self.task_name = task_name
        self.fl_ctx = fl_ctx
        self.send_rc = None
        self.result_rc = None
        self.result_error = None
        self.result = None
        self.result_received_time = None
        self.result_waiter = threading.Event()

    def __str__(self):
        return f"'{self.task_name} {self.task_id}'"


class IPCExchanger(Executor):
    def __init__(
        self,
        send_task_timeout=5.0,
        resend_task_interval=2.0,
        agent_connection_timeout=60.0,
        agent_heartbeat_timeout=None,
        agent_heartbeat_interval=5.0,
        agent_ack_timeout=5.0,
        agent_id=None,
    ):
        """Constructor of IPCExchanger

        Args:
            send_task_timeout: when sending task to Agent, how long to wait for response
            resend_task_interval: when failed to send task to agent, how often to resend
            agent_heartbeat_timeout: time allowed to miss heartbeat ack from agent before stopping
            agent_connection_timeout: time allowed to miss heartbeat ack from agent for considering it disconnected
            agent_heartbeat_interval: how often to send heartbeats to the agent
            agent_ack_timeout: how long to wait for agent ack (for heartbeat and bye messages)
            agent_id: the unique ID of the agent. If not specified, will get it from job's meta
        """
        Executor.__init__(self)
        self.flare_agent_fqcn = None
        self.agent_ack_timeout = agent_ack_timeout
        self.agent_heartbeat_interval = agent_heartbeat_interval
        self.agent_heartbeat_timeout = agent_heartbeat_timeout
        self.agent_connection_timeout = agent_connection_timeout
        self.send_task_timeout = send_task_timeout
        self.resend_task_interval = resend_task_interval
        self.agent_id = agent_id
        self.last_agent_ack_time = time.time()
        self.engine = None
        self.cell = None
        self.is_done = False
        self.is_connected = False
        self.task_ctx = None

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def _say_goodbye(self):
        # say goodbye to agent
        pass

    def _monitor(self):
        # try to connect the flare agent
        pass

    def execute(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def _send_task(self, task_ctx: _TaskContext, msg, abort_signal):
        # keep sending until done
        pass

    def _do_execute(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def _ask_agent_to_abort_task(self, task_name, task_id):
        pass

    @staticmethod
    def _finish_result(task_ctx: _TaskContext, result_rc="", result=None, result_is_valid=True):
        pass

    def _receive_result(self, request: Message) -> Union[None, Message]:
        pass
