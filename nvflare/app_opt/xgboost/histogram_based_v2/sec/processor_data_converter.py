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
from typing import Dict, List, Tuple

from nvflare.apis.fl_context import FLContext
from nvflare.app_opt.xgboost.histogram_based_v2.sec.dam import DamDecoder, DamEncoder
from nvflare.app_opt.xgboost.histogram_based_v2.sec.data_converter import (
    AggregationContext,
    DataConverter,
    FeatureAggregationResult,
    FeatureContext,
)

DATA_SET_GH_PAIRS = 1
DATA_SET_AGGREGATION = 2
DATA_SET_AGGREGATION_WITH_FEATURES = 3
DATA_SET_AGGREGATION_RESULT = 4
DATA_SET_HISTOGRAMS = 5
DATA_SET_HISTOGRAMS_RESULT = 6

SCALE_FACTOR = 1000000.0  # Preserve 6 decimal places


class ProcessorDataConverter(DataConverter):
    def __init__(self):
        super().__init__()
        self.features = []
        self.feature_list = None
        self.num_samples = 0

    def decode_gh_pairs(self, buffer: bytes, fl_ctx: FLContext) -> List[Tuple[int, int]]:
        pass

    def decode_aggregation_context(self, buffer: bytes, fl_ctx: FLContext) -> AggregationContext:
        pass

    def encode_aggregation_result(
        self, aggr_results: Dict[int, List[FeatureAggregationResult]], fl_ctx: FLContext
    ) -> bytes:
        pass

    def decode_histograms(self, buffer: bytes, fl_ctx: FLContext) -> List[float]:
        pass

    def encode_histograms_result(self, histograms: List[float], fl_ctx: FLContext) -> bytes:
        pass

    @staticmethod
    def get_bin_size(cuts: [int], feature_id: int) -> int:
        pass

    @staticmethod
    def slot_to_bin(cuts: [int], slot: int) -> Tuple[int, int]:

        pass

    @staticmethod
    def float_to_int(value: float) -> int:
        pass

    @staticmethod
    def int_to_float(value: int) -> float:
        pass

    @staticmethod
    def to_float_array(result: FeatureAggregationResult) -> List[float]:
        pass
