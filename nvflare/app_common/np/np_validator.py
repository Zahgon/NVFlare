# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
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

import numpy as np

from nvflare.apis.dxo import DXO, DataKind, from_shareable
from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.app_common.app_constant import AppConstants
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.security.logging import secure_format_exception

from .constants import NPConstants


class NPValidator(Executor):
    def __init__(
        self,
        epsilon=1,
        sleep_time=0,
    ):
        # Init functions of components should be very minimal. Init
        # is called when json is read. A big init will cause json loading to halt
        # for long time.
        super().__init__()

        self.logger = get_obj_logger(self)
        self._random_epsilon = epsilon
        self._sleep_time = sleep_time
        self._validate_task_name = AppConstants.TASK_VALIDATION
        self._submit_model_task_name = AppConstants.TASK_SUBMIT_MODEL

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        # if event_type == EventType.START_RUN:
        #     Create all major components here. This is a simple app that doesn't need any components.
        # elif event_type == EventType.END_RUN:
        #     # Clean up resources (closing files, joining threads, removing dirs etc.)
        pass

    def execute(
        self,
        task_name: str,
        shareable: Shareable,
        fl_ctx: FLContext,
        abort_signal: Signal,
    ) -> Shareable:
        # Any long tasks should check abort_signal regularly.
        # Otherwise, abort client will not work.
        pass
