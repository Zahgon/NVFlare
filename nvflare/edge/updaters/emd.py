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
import copy
import threading
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.abstract.aggregator import Aggregator
from nvflare.edge.mud import BaseState, Device, ModelUpdate, StateUpdateReply, StateUpdateReport
from nvflare.edge.updater import Updater


class AggregatorFactory(ABC):

    @abstractmethod
    def get_aggregator(self) -> Aggregator:
        pass


class ModelAggrState:

    def __init__(self, aggregator: Aggregator, model_version: int):
        self.aggregator = aggregator
        self.model_version = model_version
        self.devices: Dict[str, float] = {}

    def accept(self, contribution: Shareable, devices: Dict[str, float], fl_ctx: FLContext) -> bool:
        pass

    def to_model_update(self, fl_ctx: FLContext) -> ModelUpdate:
        pass

    def reset(self, fl_ctx: FLContext):
        pass


class EdgeModelUpdater(Updater):

    def __init__(self, aggr_factory_id: Union[str, AggregatorFactory], max_model_versions: int):
        Updater.__init__(self)
        self.aggr_factory_id = aggr_factory_id
        self.max_model_versions = max_model_versions
        self.aggr_factory = None
        self.aggr_states: Dict[int, ModelAggrState] = {}  # model_version => ModelAggrState
        self.available_devices: Dict[str, Device] = {}  # device_id => Device
        self._update_lock = threading.Lock()
        self.register_event_handler(EventType.START_RUN, self._emu_handle_start_run)

        if isinstance(aggr_factory_id, AggregatorFactory):
            self.aggr_factory = aggr_factory_id

    def _emu_handle_start_run(self, event_type: str, fl_ctx: FLContext):
        pass

    def start_task(self, task_data: Shareable, fl_ctx: FLContext) -> Any:
        # The task_data is a BaseState
        pass

    def prepare_update_for_parent(self, fl_ctx: FLContext) -> Optional[Shareable]:
        pass

    def process_parent_update_reply(self, reply: Shareable, fl_ctx: FLContext):
        pass

    def _update_one_model(self, mu: ModelUpdate, fl_ctx: FLContext):
        pass

    def process_child_update(self, update: Shareable, fl_ctx: FLContext) -> (bool, Optional[Shareable]):
        pass

    def end_task(self, fl_ctx: FLContext):
        pass
