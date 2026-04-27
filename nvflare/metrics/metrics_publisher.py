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


from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import FLContextKey, ReservedTopic
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.fuel.data_event.data_bus import DataBus
from nvflare.metrics.metrics_keys import METRICS_EVENT_TYPE, MetricKeys


def publish_app_metrics(metrics: dict, metric_name: str, tags: dict, data_bus: DataBus) -> None:
    pass


def convert_metrics_to_event(
    comp: FLComponent,
    metrics: dict,
    metric_name: str,
    tags: dict,
    fl_ctx: FLContext,
) -> None:
    pass


def collect_metrics(
    comp: FLComponent,
    streaming_to_server: bool,
    metrics: dict,
    metric_name: str,
    tags: dict,
    data_bus: DataBus,
    fl_ctx: FLContext,
):

    pass
