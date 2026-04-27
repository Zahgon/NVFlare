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

import json
import os.path
from functools import singledispatch

import numpy as np

from nvflare.apis.dxo import DataKind, from_shareable, get_leaf_dxos
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_context import FLContext
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.app_event_type import AppEventType
from nvflare.widgets.widget import Widget


@singledispatch
def to_serializable(val):
    """Default json serializable method."""
    pass


@to_serializable.register(np.float32)
def ts_float32(val):
    pass


class ValidationJsonGenerator(Widget):
    def __init__(self, results_dir=AppConstants.CROSS_VAL_DIR, json_file_name="cross_val_results.json"):
        """Catches VALIDATION_RESULT_RECEIVED event and generates a results.json containing accuracy of each
        validated model.

        Args:
            results_dir (str, optional): Name of the results directory. Defaults to cross_site_val
            json_file_name (str, optional): Name of the json file. Defaults to cross_val_results.json
        """
        super(ValidationJsonGenerator, self).__init__()

        self._results_dir = results_dir
        self._val_results = {}
        self._json_file_name = json_file_name

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass
