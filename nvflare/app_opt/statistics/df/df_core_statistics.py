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
from abc import ABC
from math import sqrt
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from pandas.core.series import Series

from nvflare.app_common.abstract.statistics_spec import BinRange, Feature, Histogram, HistogramType, Statistics
from nvflare.app_common.app_constant import StatisticsConstants
from nvflare.app_common.statistics.numpy_utils import dtype_to_data_type, get_std_histogram_buckets
from nvflare.fuel.utils.import_utils import optional_import


class DFStatisticsCore(Statistics, ABC):
    def __init__(self, max_bin=None):
        # assumption: the data can be loaded and cached in the memory
        self.data: Optional[Dict[str, pd.DataFrame]] = None
        super(DFStatisticsCore, self).__init__()
        self.max_bin = max_bin

    def features(self) -> Dict[str, List[Feature]]:
        pass

    def count(self, dataset_name: str, feature_name: str) -> int:
        pass

    def sum(self, dataset_name: str, feature_name: str) -> float:
        pass

    def mean(self, dataset_name: str, feature_name: str) -> float:

        pass

    def stddev(self, dataset_name: str, feature_name: str) -> float:
        pass

    def variance_with_mean(
        self, dataset_name: str, feature_name: str, global_mean: float, global_count: float
    ) -> float:
        pass

    def histogram(
        self, dataset_name: str, feature_name: str, num_of_bins: int, global_min_value: float, global_max_value: float
    ) -> Histogram:

        pass

    def max_value(self, dataset_name: str, feature_name: str) -> float:
        """this is needed for histogram calculation, not used for reporting"""
        pass

    def min_value(self, dataset_name: str, feature_name: str) -> float:
        """this is needed for histogram calculation, not used for reporting"""
        pass

    def quantiles(self, dataset_name: str, feature_name: str, percents: List) -> Dict:
        pass
