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

from math import sqrt
from typing import Dict, List, TypeVar

from nvflare.app_common.abstract.statistics_spec import Bin, BinRange, DataType, Feature, Histogram, HistogramType
from nvflare.app_common.app_constant import StatisticsConstants as StC
from nvflare.app_opt.statistics.quantile_stats import get_quantiles
from nvflare.fuel.utils.log_utils import get_module_logger

T = TypeVar("T")

logger = get_module_logger(name=__name__)


def get_global_feature_data_types(
    client_feature_dts: Dict[str, Dict[str, List[Feature]]],
) -> Dict[str, Dict[str, DataType]]:
    pass


def get_global_stats(
    global_metrics: dict, client_metrics: dict, metric_task: str, statistic_configs: Dict[str, dict], precision: int = 4
) -> dict:
    # we need to calculate the metrics in specified order
    pass


def accumulate_metrics(metrics: dict, global_metrics: dict, precision: int) -> dict:
    pass


def get_min_or_max_values(metrics: dict, global_metrics: dict, fn2, precision: int = 4) -> dict:
    """Use 2 argument function to calculate fn2(global, client), for example, min or max.

    .. note::

        The global min/max values are min/max of all clients and all datasets.

    Args:
        metrics: client's metric
        global_metrics: global metrics
        fn2: two-argument function such as min or max
        precision: decimal number precision

    Returns: Dict[dataset, Dict[feature, int]]

    """
    pass


def bins_to_dict(bins: List[Bin]) -> Dict[BinRange, float]:
    pass


def accumulate_hists(
    metrics: Dict[str, Dict[str, Histogram]], global_hists: Dict[str, Dict[str, Histogram]], precision: int = 4
) -> Dict[str, Dict[str, Histogram]]:
    pass


def get_means(sums: dict, counts: dict, precision: int = 4) -> dict:
    pass


def filter_numeric_features(ds_features: Dict[str, List[Feature]]) -> Dict[str, List[Feature]]:
    pass
