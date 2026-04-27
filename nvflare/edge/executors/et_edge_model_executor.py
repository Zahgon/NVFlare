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

import base64
import time
from typing import Optional

import torch

from nvflare.apis.dxo import DataKind, from_dict
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReservedHeaderKey
from nvflare.edge.constants import CookieKey, MsgKey
from nvflare.edge.executors.edge_model_executor import EdgeModelExecutor, ModelUpdate
from nvflare.edge.executors.hug import TaskInfo
from nvflare.edge.model_protocol import ModelBufferType, ModelEncoding, ModelExchangeFormat, ModelNativeFormat
from nvflare.edge.models.model import DeviceModel, export_model_to_bytes
from nvflare.edge.mud import BaseState
from nvflare.edge.web.models.result_report import ResultReport


class ETEdgeModelExecutor(EdgeModelExecutor):
    def __init__(
        self,
        et_model: DeviceModel,
        input_shape,
        output_shape,
        aggr_factory_id: str,
        max_model_versions: int,
        update_timeout=60,
    ):
        """Initializes an edge model executor for on-device training using ExecuTorch.

        This constructor sets up the executor with a training-ready PyTorch model
        (wrapped to include loss computation), along with model input/output shapes
        and versioning/update control parameters.

        Args:
            et_model (DeviceModel): A PyTorch model wrapped for ExecuTorch export.
                See `nvflare/edge/models/model.py` for wrapping examples.
            input_shape (tuple): Shape of the input tensor (e.g., (1, 3, 224, 224)).
            output_shape (tuple): Shape of the label/output tensor (e.g., (1,) for class index).
            aggr_factory_id (str): Identifier used for selecting the model aggregation strategy.
            max_model_versions (int): Maximum number of model versions to retain or track.
            update_timeout (int, optional): Timeout in seconds for applying model updates. Defaults to 60.
        """
        EdgeModelExecutor.__init__(self, aggr_factory_id, max_model_versions, update_timeout)
        self.et_model = et_model
        self.input_shape = input_shape
        self.output_shape = output_shape

    def _export_model_weights_to_pte_b64str(self, model_weights) -> str:
        pass

    def _convert_task(self, task_state: BaseState, current_task: TaskInfo, fl_ctx: FLContext) -> dict:
        """Convert task_data to a plain dict"""
        pass

    def _convert_to_tensor_dxo(self, result_dict: dict, fl_ctx: FLContext):
        """Convert the result_dict to a tensor DXO"""
        pass

    def _convert_device_result_to_model_update(
        self, result_report: ResultReport, current_task: TaskInfo, fl_ctx: FLContext
    ) -> Optional[ModelUpdate]:
        pass
