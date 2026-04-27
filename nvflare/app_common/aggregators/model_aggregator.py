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


from abc import abstractmethod

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.abstract.aggregator import Aggregator
from nvflare.app_common.abstract.fl_model import FLModel
from nvflare.app_common.utils.fl_model_utils import FLModelUtils


class ModelAggregator(Aggregator):
    """
    Abstract class for aggregating FLModels.
    Subclasses need to implement accept_model and aggregate_model methods.
    """

    def __init__(self):
        self.fl_ctx = None

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    @abstractmethod
    def accept_model(self, model: FLModel):
        """needs to implement logic to accept a model, e.g. add to sum, count, etc."""
        pass

    @abstractmethod
    def aggregate_model(self) -> FLModel:
        """needs to implement aggregation logic and reset any internal stats"""
        pass

    @abstractmethod
    def reset_stats(self):
        """needs to implement logic to reset any internal stats"""
        pass

    def accept(self, shareable: Shareable, fl_ctx: FLContext) -> bool:
        """called by ScatterAndGather"""
        pass

    def aggregate(self, fl_ctx: FLContext) -> Shareable:
        """called by ScatterAndGather"""
        pass

    def reset(self, fl_ctx: FLContext):
        """called by ScatterAndGather"""
        pass

    def info(self, message: str):
        pass

    def warning(self, message: str):
        pass

    def error(self, message: str):
        pass

    def exception(self, message: str):
        pass
