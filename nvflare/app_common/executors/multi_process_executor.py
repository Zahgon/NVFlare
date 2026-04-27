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
import os
import shlex
import subprocess
import threading
import time
from abc import abstractmethod
from nvflare.apis.event_type import EventType
from nvflare.apis.executor import Executor
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import ConfigVarName, FLContextKey, ReturnCode, SystemConfigs
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.apis.utils.fl_context_utils import get_serializable_data
from nvflare.fuel.common.multi_process_executor_constants import (
    CommunicateData,
    CommunicationMetaData,
    MultiProcessCommandNames,
)
from nvflare.fuel.f3.cellnet.core_cell import Message as CellMessage
from nvflare.fuel.f3.cellnet.core_cell import MessageHeaderKey
from nvflare.fuel.f3.cellnet.core_cell import ReturnCode as F3ReturnCode
from nvflare.fuel.f3.cellnet.core_cell import make_reply as F3make_reply
from nvflare.fuel.f3.cellnet.fqcn import FQCN
from nvflare.fuel.utils.class_utils import ModuleScanner
from nvflare.fuel.utils.component_builder import ComponentBuilder
from nvflare.fuel.utils.config_service import ConfigService
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.private.defs import CellChannel, CellChannelTopic, new_cell_message
from nvflare.security.logging import secure_format_exception
class WorkerComponentBuilder(ComponentBuilder):
    FL_PACKAGES = ["nvflare"]
    FL_MODULES = ["client", "app"]
    def __init__(self) -> None:
        """Component to build workers."""
        super().__init__()
        self.module_scanner = ModuleScanner(WorkerComponentBuilder.FL_PACKAGES, WorkerComponentBuilder.FL_MODULES, True)
    def get_module_scanner(self):
        pass
class MultiProcessExecutor(Executor):
    def __init__(self, executor_id=None, num_of_processes=1, components=None):
        """Manage the multi-process execution life cycle.
        Arguments:
            executor_id: executor component ID
            num_of_processes: number of processes to create
            components: a dictionary for component classes to their arguments
        """
        super().__init__()
        self.executor_id = executor_id
        self.components_conf = components
        self.components = {}
        self.handlers = []
        self._build_components(components)
        if not isinstance(num_of_processes, int):
            raise TypeError("{} must be an instance of int but got {}".format(num_of_processes, type(num_of_processes)))
        if num_of_processes < 1:
            raise ValueError(f"{num_of_processes} must >= 1.")
        self.num_of_processes = num_of_processes
        self.executor = None
        self.execute_result = None
        self.execute_complete = None
        self.engine = None
        self.logger = get_obj_logger(self)
        self.conn_clients = []
        self.exe_process = None
        self.stop_execute = False
        self.relay_threads = []
        self.finalized = False
        self.event_lock = threading.Lock()
        self.relay_lock = threading.Lock()
    @abstractmethod
    def get_multi_process_command(self) -> str:
        """Provide the command for starting multi-process execution.
        Returns:
            multi-process starting command
        """
        pass
    def _build_components(self, components):
        pass
    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass
    def _pass_event_to_rank_processes(self, event_type: str, fl_ctx: FLContext):
        pass
    def initialize(self, fl_ctx: FLContext):
        pass
    def _initialize_multi_process(self, fl_ctx: FLContext):
        pass
    def receive_execute_result(self, request: CellMessage) -> CellMessage:
        pass
    def _relay_fire_event(self, request: CellMessage) -> CellMessage:
        pass
    def execute(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass
    def _execute_multi_process(
        self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal
    ) -> Shareable:
        pass
    def finalize(self, fl_ctx: FLContext):
        """This is called when exiting/aborting the executor."""
        pass
