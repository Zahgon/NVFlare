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

import bz2
import math
from typing import Any, Optional, Union

import numpy as np
import torch


class AdaQuantizer:
    def __init__(self, weight: float = 0.01, compression: bool = True) -> None:
        """Implements the ADAQUANT quantization scheme,
            for further details refer to the paper https://arxiv.org/abs/2208.05174

        Args:
            weight: a hyperparameter for the trade-off between quantization size and error
            compression: whether to compress the resulting integer quantized tensor

        """

        self.weight = weight
        self.compression = compression

    def quantize(self, values_tensor: torch.Tensor) -> tuple[Union[torch.Tensor, np.ndarray], dict]:
        pass

    def dequantized(self, quantized_tensor: torch.Tensor, quant_state: dict) -> torch.Tensor:
        pass

    def get_offset(self, tensor: torch.Tensor) -> float:
        pass

    def get_number_of_quantization_levels(
        self, element_size: int, values_tensor: torch.Tensor
    ) -> Optional[tuple[float, int, Any]]:
        pass
