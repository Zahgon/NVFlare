# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
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
from abc import abstractmethod
from typing import Optional

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import ReservedKey
from nvflare.apis.fl_context import FLContext
from nvflare.edge.constants import EdgeContextKey, EdgeEventType
from nvflare.edge.simulation.simulator import Simulator
from nvflare.edge.web.models.job_request import JobRequest
from nvflare.edge.web.models.result_report import ResultReport
from nvflare.edge.web.models.selection_request import SelectionRequest
from nvflare.edge.web.models.task_request import TaskRequest
from nvflare.widgets.widget import Widget


class SimulationRunner(Widget):

    def __init__(self):
        Widget.__init__(self)
        self.simulator = None
        self.register_event_handler(EventType.START_RUN, self._sr_start_run)
        self.register_event_handler(EventType.END_RUN, self._sr_end_run)

    @abstractmethod
    def create_simulator(self, fl_ctx: FLContext) -> Optional[Simulator]:
        pass

    def _sr_start_run(self, event_type: str, fl_ctx: FLContext):
        pass

    def _sr_end_run(self, event_type: str, fl_ctx: FLContext):
        pass

    def _post_request(self, request, device, engine):
        pass

    def _run(self):
        pass
