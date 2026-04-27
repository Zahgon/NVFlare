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
from typing import List, Optional

import numpy as np
from pandas.api.types import is_bool_dtype, is_datetime64_any_dtype, is_float_dtype, is_integer_dtype

from nvflare.app_common.abstract.statistics_spec import Bin, BinRange, DataType


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        pass


def dtype_to_data_type(dtype) -> DataType:
    # Use pandas type-checking functions so that both numpy dtypes and pandas
    # nullable ExtensionDtypes (Int64Dtype, Float64Dtype, BooleanDtype, StringDtype, …)
    # are classified correctly.
    pass


def get_std_histogram_buckets(nums: np.ndarray, num_bins: int = 10, br: Optional[BinRange] = None):
    pass
