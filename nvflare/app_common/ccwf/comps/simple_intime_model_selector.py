# Copyright (c) 2023, NVIDIA CORPORATION.  All rights reserved.
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

import numpy as np

from nvflare.apis.dxo import DataKind, MetaKey, from_shareable
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.app_event_type import AppEventType
from nvflare.widgets.widget import Widget


class SimpleIntimeModelSelector(Widget):
    def __init__(
        self, weigh_by_local_iter=False, aggregation_weights=None, validation_metric_name=MetaKey.INITIAL_METRICS
    ):
        """Handler to determine if the model is globally best.

        Args:
            weigh_by_local_iter (bool, optional): whether the metrics should be weighted by trainer's iteration number.
            aggregation_weights (dict, optional): a mapping of client name to float for aggregation. Defaults to None.
            validation_metric_name (str, optional): key used to save initial validation metric in the DXO meta properties (defaults to MetaKey.INITIAL_METRICS).
        """
        super().__init__()

        self.val_metric = self.best_val_metric = -np.inf
        self.weigh_by_local_iter = weigh_by_local_iter
        self.validation_metric_name = validation_metric_name
        self.aggregation_weights = aggregation_weights or {}

        self.logger.info(f"model selection weights control: {aggregation_weights}")
        self._reset_stats()

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def _startup(self):
        pass

    def _reset_stats(self):
        pass

    def _before_accept(self, fl_ctx: FLContext):
        pass

    def _before_aggregate(self, fl_ctx):
        pass
