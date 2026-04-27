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
import importlib
from typing import Any, List

import numpy as np
import torch

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.abstract.model import ModelLearnable, ModelLearnableKey
from nvflare.app_common.abstract.shareable_generator import ShareableGenerator
from nvflare.app_common.app_constant import AppConstants
from nvflare.edge.constants import MsgKey
from nvflare.edge.model_protocol import ModelBufferType, ModelEncoding, ModelExchangeFormat, ModelNativeFormat
from nvflare.edge.models.model import export_model


class ExecutorchShareableGenerator(ShareableGenerator):
    def __init__(self, base_model_path: str, executorch_model_path: str, input_shape: List, output_shape: List):
        super().__init__()
        self.base_model_path = base_model_path
        self.executorch_model_path = executorch_model_path
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.model = None

    def _load_model(self, model_path: str, fl_ctx: FLContext) -> Any:
        """Load model from model path.

        Args:
            model_path (str): model path in format "module.submodule.ClassName"
            fl_ctx (FLContext): FL context

        Returns:
            model class instance
        """
        pass

    def _export_current_model(self) -> bytes:
        """Export current model in ExecutorTorch format."""
        pass

    def handle_event(self, event: str, fl_ctx: FLContext):
        pass

    def learnable_to_shareable(self, model_learnable: ModelLearnable, fl_ctx: FLContext) -> Shareable:
        """Convert ModelLearnable to Shareable.

        Args:
            model_learnable (ModelLearnable): model to be converted
            fl_ctx (FLContext): FL context

        Returns:
            Shareable: a shareable containing a DXO object.
        """
        pass

    def shareable_to_learnable(self, shareable: Shareable, fl_ctx: FLContext) -> ModelLearnable:
        """Convert Shareable to ModelLearnable.

        Supporting TYPE == TYPE_WEIGHT_DIFF or TYPE_WEIGHTS

        Args:
            shareable (Shareable): Shareable that contains a DXO object
            fl_ctx (FLContext): FL context

        Returns:
            A ModelLearnable object

        Raises:
            TypeError: if shareable is not of type shareable
            ValueError: if data_kind is not `DataKind.WEIGHTS` and is not `DataKind.WEIGHT_DIFF`
        """
        pass
