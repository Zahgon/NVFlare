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

import copy
import os
import random
import time

import numpy as np

from nvflare.apis.dxo import DXO, DataKind, MetaKey, from_shareable
from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import FLContextKey, ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.app_common.abstract.model import ModelLearnable
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.np.constants import NPConstants
from nvflare.security.logging import secure_format_exception


class NPTrainer(Executor):
    def __init__(
        self,
        delta=1,
        sleep_time=0,
        train_task_name=AppConstants.TASK_TRAIN,
        submit_model_task_name=AppConstants.TASK_SUBMIT_MODEL,
        validate_model_task_name=AppConstants.TASK_VALIDATION,
        model_name="best_numpy.npy",
        model_dir="model",
    ):
        # Init functions of components should be very minimal. Init
        # is called when json is read. A big init will cause json loading to halt
        # for long time.
        super().__init__()

        if not (isinstance(delta, float) or isinstance(delta, int)):
            raise TypeError("delta must be an instance of float or int.")

        self._delta = delta
        self._model_name = model_name
        self._model_dir = model_dir
        self._sleep_time = sleep_time
        self._train_task_name = train_task_name
        self._submit_model_task_name = submit_model_task_name
        self._validate_model_task_name = validate_model_task_name

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        # if event_type == EventType.START_RUN:
        #     Create all major components here. This is a simple app that doesn't need any components.
        # elif event_type == EventType.END_RUN:
        #     # Clean up resources (closing files, joining threads, removing dirs etc.)
        pass

    def _train(self, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal):
        # First we extract DXO from the shareable.
        pass

    def _submit_model(self, fl_ctx: FLContext, abort_signal: Signal):
        # Retrieve the local model saved during training.
        pass

    def execute(
        self,
        task_name: str,
        shareable: Shareable,
        fl_ctx: FLContext,
        abort_signal: Signal,
    ) -> Shareable:
        # Any long tasks should check abort_signal regularly. Otherwise, abort client
        # will not work.
        pass

    def _validate_model(self, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def _load_local_model(self, fl_ctx: FLContext):
        pass

    def _save_local_model(self, fl_ctx: FLContext, model: dict):
        # Save local model
        pass
