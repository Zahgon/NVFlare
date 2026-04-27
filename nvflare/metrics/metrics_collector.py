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


import time
from abc import ABC, abstractmethod
from typing import Dict, List

from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_context import FLContext
from nvflare.fuel.data_event.data_bus import DataBus
from nvflare.metrics.metrics_keys import MetricKeys, MetricTypes
from nvflare.metrics.metrics_publisher import collect_metrics


class MetricsCollector(FLComponent, ABC):
    def __init__(self, tags: dict, streaming_to_server: bool = False):
        """
        Args:
            tags: comma separated static tags. used to specify server, client, production, test etc.
        """
        super().__init__()

        self.tags = tags
        self.data_bus = DataBus()
        self.streaming_to_server = streaming_to_server

        self.event_start_time = {}

    @abstractmethod
    def get_single_events() -> List[str]:
        pass

    @abstractmethod
    def get_pair_events() -> Dict:
        pass

    def collect_event_metrics(self, event: str, tags, fl_ctx: FLContext):

        pass

    def publish_metrics(self, metrics: dict, metric_name: str, tags: dict, fl_ctx: FLContext):

        pass
