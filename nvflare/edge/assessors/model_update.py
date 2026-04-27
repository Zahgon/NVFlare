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
import time
from typing import Optional

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.abstract.learnable_persistor import LearnablePersistor
from nvflare.app_common.abstract.model import ModelLearnable, model_learnable_to_dxo
from nvflare.app_common.app_event_type import AppEventType
from nvflare.edge.assessor import Assessment, Assessor
from nvflare.edge.mud import BaseState, StateUpdateReply, StateUpdateReport


class ModelUpdateAssessor(Assessor):
    def __init__(
        self,
        persistor_id,
        model_manager_id,
        device_manager_id,
        max_model_version,
        device_wait_timeout: Optional[float] = None,
        device_status_log_interval: Optional[float] = 30.0,
    ):
        """Initialize the ModelUpdateAssessor.
        Enable both asynchronous and synchronous model updates from clients.
        For asynchronous updates, the staleness is calculated based on the starting and current model version.
        And the aggregation scheme and weights are calculated following FedBuff paper "Federated Learning with Buffered Asynchronous Aggregation".

        Args:
            persistor_id (str): ID of the persistor component used to load and save models.
            model_manager_id (str): ID of the model manager component.
            device_manager_id (str): ID of the device manager component.
            max_model_version (int): Maximum model version to stop the workflow.
            device_wait_timeout (float, optional): Timeout in seconds for waiting for sufficient devices. None means no timeout. Default is None.
            device_status_log_interval (float, optional): Interval in seconds for logging device status. Default is 30 seconds.
        """
        Assessor.__init__(self)
        self.persistor_id = persistor_id
        self.model_manager_id = model_manager_id
        self.device_manager_id = device_manager_id
        self.persistor = None
        self.model_manager = None
        self.device_manager = None
        self.max_model_version = max_model_version
        self.update_lock = threading.Lock()
        self.device_wait_timeout = device_wait_timeout
        self.device_wait_start_time = None
        self._last_device_status_log_time = time.time()
        self.device_status_log_interval = device_status_log_interval
        self.register_event_handler(EventType.START_RUN, self._handle_start_run)

    def _is_device_wait_timeout_exceeded(self, fl_ctx: FLContext) -> bool:
        """Check if device wait timeout has been exceeded.

        Args:
            fl_ctx: FL context

        Returns:
            bool: True if timeout exceeded, False otherwise
        """
        pass

    def _log_device_status(self, fl_ctx: FLContext):
        """Log device status information independently of timeout logic."""
        pass

    def _handle_start_run(self, event_type: str, fl_ctx: FLContext):
        pass

    def start_task(self, fl_ctx: FLContext) -> Shareable:
        # empty base state to start with
        pass

    def process_child_update(self, update: Shareable, fl_ctx: FLContext) -> (bool, Optional[Shareable]):
        pass

    def _do_child_update(self, update: Shareable, fl_ctx: FLContext) -> (bool, Optional[Shareable]):
        pass

    def assess(self, fl_ctx: FLContext) -> Assessment:
        # Check if we're waiting for devices and timeout exceeded
        pass
