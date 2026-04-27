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
import threading
from typing import Union

import numpy as np
import torch
from bitsandbytes.functional import quantize_4bit, quantize_blockwise

from nvflare.apis.dxo import DXO, DataKind, MetaKey
from nvflare.apis.dxo_filter import DXOFilter
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_opt.pt.quantization.constant import DATA_TYPE, QUANTIZATION_TYPE

from .ada_quant import AdaQuantizer


class ModelQuantizer(DXOFilter):
    def __init__(
        self,
        quantization_type="float16",
    ):
        """Filter to quantize Shareable object to reduce communication burden.

        Args:
            quantization_type: method used for quantization

        """

        # support weight and weight_diff data kinds
        data_kinds = [DataKind.WEIGHTS, DataKind.WEIGHT_DIFF]
        super().__init__(supported_data_kinds=data_kinds, data_kinds_to_filter=data_kinds)

        # assign quantization type and check if it is valid
        self.logger.info("Using model quantizer.")
        quantization_type = quantization_type.lower()
        if quantization_type.upper() not in QUANTIZATION_TYPE:
            raise ValueError(f"Invalid quantization type: {quantization_type}, valid: {QUANTIZATION_TYPE}")

        self.quantization_type = quantization_type

        # quantization constants
        self.NP_FP16_MIN = np.finfo(np.float16).min
        self.NP_FP16_MAX = np.finfo(np.float16).max
        self.TS_FP16_MIN = torch.finfo(torch.float16).min
        self.TS_FP16_MAX = torch.finfo(torch.float16).max

        # Lock to ensure thread-safe quantization for concurrent client requests
        # In 1-N server scenarios, multiple clients may process the same task data
        # Key by id(dxo.data) since different DXO wrappers may share the same data dict
        self._quantization_locks = {}  # data_id -> threading.Lock
        self._quantized_results = {}  # data_id -> quantized DXO (metadata for waiting threads)
        self._quantization_errors = {}  # data_id -> Exception (if quantization failed)
        self._data_refcounts = {}  # data_id -> number of threads using this data
        self._locks_lock = threading.Lock()  # protect the dictionaries

    def quantization(self, params: dict, fl_ctx: FLContext):
        pass

    def process_dxo(self, dxo: DXO, shareable: Shareable, fl_ctx: FLContext) -> Union[None, DXO]:
        """Filter process apply to the Shareable object.

        Args:
            dxo: data to be processed
            shareable: that the dxo belongs to
            fl_ctx: FLContext

        Returns: DXO object with quantized weights

        """
        pass
