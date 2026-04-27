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

import re
from typing import Union

import numpy as np
import torch
from bitsandbytes.functional import QuantState, dequantize_4bit, dequantize_blockwise

from nvflare.apis.dxo import DXO, DataKind, MetaKey
from nvflare.apis.dxo_filter import DXOFilter
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_opt.pt.quantization.constant import QUANTIZATION_TYPE

from .ada_quant import AdaQuantizer


class ModelDequantizer(DXOFilter):
    def __init__(self):
        """Filter to dequantize Shareable object to recover from quantization

        Args:
            None

        """

        # support weight and weight_diff data kinds
        data_kinds = [DataKind.WEIGHTS, DataKind.WEIGHT_DIFF]
        super().__init__(supported_data_kinds=data_kinds, data_kinds_to_filter=data_kinds)
        self.logger.info("Using model dequantizer.")

    def dequantization(
        self,
        params: dict,
        quant_state: dict,
        quantization_type: str,
        source_datatype: dict,
        fl_ctx: FLContext,
    ):
        pass

    def process_dxo(self, dxo: DXO, shareable: Shareable, fl_ctx: FLContext) -> Union[None, DXO]:
        """Filter process apply to the Shareable object.

        Args:
            dxo: data to be processed
            shareable: that the dxo belongs to
            fl_ctx: FLContext

        Returns: DXO object with dequantized weights

        """
        pass
