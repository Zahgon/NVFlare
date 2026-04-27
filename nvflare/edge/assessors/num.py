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
import random
import threading
import time
from typing import Optional

from nvflare.apis.dxo import DXO
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.edge.aggregators.num_dxo import NumDXOAggregator
from nvflare.edge.assessor import Assessment, Assessor
from nvflare.edge.mud import BaseState, ModelUpdate, StateUpdateReply, StateUpdateReport


class _ModelState:

    def __init__(self, aggr: NumDXOAggregator):
        self.aggregator = aggr
        self.devices = {}
        self.last_update_time = None

    def accept(self, model_update: ModelUpdate, fl_ctx: FLContext):
        pass


class NumAssessor(Assessor):

    def __init__(
        self,
        num_updates_for_model,
        max_model_version,
        max_model_history,
        device_selection_size,
        min_hole_to_fill=1,
        device_reuse=True,
    ):
        Assessor.__init__(self)
        self.current_model_version = 0
        self.current_model = None
        self.current_selection_version = 0
        self.current_selection = {}
        self.updates = {}  # model_version => _ModelState
        self.available_devices = {}
        self.used_devices = {}
        self.num_updates_for_model = num_updates_for_model
        self.max_model_version = max_model_version
        self.max_model_history = max_model_history
        self.device_selection_size = device_selection_size
        self.min_hole_to_fill = min_hole_to_fill
        self.device_reuse = device_reuse
        self.update_lock = threading.Lock()
        self.start_time = None

    def start_task(self, fl_ctx: FLContext) -> Shareable:
        pass

    def _generate_new_model(self, fl_ctx: FLContext):
        pass

    def process_child_update(self, update: Shareable, fl_ctx: FLContext) -> (bool, Optional[Shareable]):
        pass

    def _do_child_update(self, update: Shareable, fl_ctx: FLContext) -> (bool, Optional[Shareable]):
        pass

    def _fill_selection(self, fl_ctx: FLContext):
        pass

    def assess(self, fl_ctx: FLContext) -> Assessment:
        pass
