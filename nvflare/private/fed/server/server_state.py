# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
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

from __future__ import annotations

from abc import ABC, abstractmethod

from nvflare.apis.fl_context import FLContext
from nvflare.apis.overseer_spec import SP
from nvflare.fuel.utils.log_utils import get_module_logger

ACTION = "_action"
MESSAGE = "_message"

NIS = "Not In Service"
ABORT_RUN = "Abort Run"
SERVICE = "In Service"


class ServiceSession:
    def __init__(self, host: str = "", port: str = "", ssid: str = "") -> None:
        self.host = host
        self.service_port = port
        self.ssid = ssid


class ServerState(ABC):
    NOT_IN_SERVICE = {ACTION: NIS, MESSAGE: "Server not in service"}
    ABORT_CURRENT_RUN = {ACTION: ABORT_RUN, MESSAGE: "Abort current run"}
    IN_SERVICE = {ACTION: SERVICE, MESSAGE: "Server in service"}

    logger = get_module_logger(__module__, __qualname__)

    def __init__(self, host: str = "", port: str = "", ssid: str = "") -> None:
        self.host = host
        self.service_port = port
        self.ssid = ssid
        self.primary = False

    @abstractmethod
    def register(self, fl_ctx: FLContext) -> dict:
        pass

    @abstractmethod
    def heartbeat(self, fl_ctx: FLContext) -> dict:
        pass

    @abstractmethod
    def get_task(self, fl_ctx: FLContext) -> dict:
        pass

    @abstractmethod
    def submit_result(self, fl_ctx: FLContext) -> dict:
        pass

    @abstractmethod
    def aux_communicate(self, fl_ctx: FLContext) -> dict:
        pass

    @abstractmethod
    def handle_sd_callback(self, sp: SP, fl_ctx: FLContext) -> ServerState:
        pass


class ColdState(ServerState):
    def register(self, fl_ctx: FLContext) -> dict:
        pass

    def heartbeat(self, fl_ctx: FLContext) -> dict:
        pass

    def get_task(self, fl_ctx: FLContext) -> dict:
        pass

    def submit_result(self, fl_ctx: FLContext) -> dict:
        pass

    def aux_communicate(self, fl_ctx: FLContext) -> dict:
        pass

    def handle_sd_callback(self, sp: SP, fl_ctx: FLContext) -> ServerState:
        pass


class Cold2HotState(ServerState):
    def register(self, fl_ctx: FLContext) -> dict:
        pass

    def heartbeat(self, fl_ctx: FLContext) -> dict:
        pass

    def get_task(self, fl_ctx: FLContext) -> dict:
        pass

    def submit_result(self, fl_ctx: FLContext) -> dict:
        pass

    def aux_communicate(self, fl_ctx: FLContext) -> dict:
        pass

    def handle_sd_callback(self, sp: SP, fl_ctx: FLContext) -> ServerState:
        pass


class HotState(ServerState):
    def register(self, fl_ctx: FLContext) -> dict:
        pass

    def heartbeat(self, fl_ctx: FLContext) -> dict:
        pass

    def get_task(self, fl_ctx: FLContext) -> dict:
        pass

    def submit_result(self, fl_ctx: FLContext) -> dict:
        pass

    def aux_communicate(self, fl_ctx: FLContext) -> dict:
        pass

    def handle_sd_callback(self, sp: SP, fl_ctx: FLContext) -> ServerState:
        pass


class Hot2ColdState(ServerState):
    def register(self, fl_ctx: FLContext) -> dict:
        pass

    def heartbeat(self, fl_ctx: FLContext) -> dict:
        pass

    def get_task(self, fl_ctx: FLContext) -> dict:
        pass

    def submit_result(self, fl_ctx: FLContext) -> dict:
        pass

    def aux_communicate(self, fl_ctx: FLContext) -> dict:
        pass

    def handle_sd_callback(self, sp: SP, fl_ctx: FLContext) -> ServerState:
        pass


class ShutdownState(ServerState):
    def register(self, fl_ctx: FLContext) -> dict:
        pass

    def heartbeat(self, fl_ctx: FLContext) -> dict:
        pass

    def get_task(self, fl_ctx: FLContext) -> dict:
        pass

    def submit_result(self, fl_ctx: FLContext) -> dict:
        pass

    def aux_communicate(self, fl_ctx: FLContext) -> dict:
        pass

    def handle_sd_callback(self, sp: SP, fl_ctx: FLContext) -> ServerState:
        pass
