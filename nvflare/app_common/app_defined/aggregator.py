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

from abc import ABC, abstractmethod
from typing import Any

from nvflare.apis.dxo import DXO, DataKind, from_shareable
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.abstract.aggregator import Aggregator
from nvflare.app_common.abstract.model import ModelLearnableKey
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.app_event_type import AppEventType

from .component_base import ComponentBase


class AppDefinedAggregator(Aggregator, ComponentBase, ABC):
    def __init__(self):
        Aggregator.__init__(self)
        ComponentBase.__init__(self)
        self.current_round = None
        self.base_model_obj = None

    def handle_event(self, event_type, fl_ctx: FLContext):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def processing_training_result(self, client_name: str, trained_weights: Any, trained_meta: dict) -> bool:
        pass

    @abstractmethod
    def aggregate_training_result(self) -> (Any, dict):
        pass

    def accept(self, shareable: Shareable, fl_ctx: FLContext) -> bool:
        pass

    def aggregate(self, fl_ctx: FLContext) -> Shareable:
        pass
