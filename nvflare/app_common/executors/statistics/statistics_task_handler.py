# Copyright (c) 2023, NVIDIA CORPORATION.  All rights reserved.
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

from typing import Dict, List, Optional

from nvflare.apis.fl_constant import ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.apis.signal import Signal
from nvflare.app_common.abstract.statistics_spec import Feature, Histogram, HistogramType, StatisticConfig, Statistics
from nvflare.app_common.abstract.task_handler import TaskHandler
from nvflare.app_common.app_constant import StatisticsConstants as StC
from nvflare.app_common.statistics.numeric_stats import filter_numeric_features
from nvflare.app_common.statistics.statisitcs_objects_decomposer import fobs_registration
from nvflare.app_common.statistics.statistics_config_utils import get_feature_bin_range, get_target_quantiles
from nvflare.fuel.utils import fobs
from nvflare.security.logging import secure_format_exception


class StatisticsTaskHandler(TaskHandler):
    """
    StatisticsTaskHandler is to be used together with StatisticsExecutor.

    StatisticsExecutor is client-side executor that perform local statistics generation and communication to
    FL Server global statistics controller. The actual local statistics calculation would delegate to
    Statistics spec implementor.

    """

    def __init__(self, generator_id: str, precision: int = 4):
        super().__init__(generator_id, Statistics)
        self.stats_generator: Optional[Statistics] = None
        self.precision = precision
        fobs_registration()

    def initialize(self, fl_ctx: FLContext):
        pass

    def execute_task(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def statistic_functions(self) -> dict:
        pass

    def _populate_result_statistics(self, statistics_result, ds_features, tm: StatisticConfig, shareable, fl_ctx, fn):
        pass

    def get_numeric_features(self) -> Dict[str, List[Feature]]:
        pass

    def pre_run(self, target_statistics: List[StatisticConfig]):
        pass

    def get_count(
        self,
        dataset_name: str,
        feature_name: str,
        statistic_configs: StatisticConfig,
        inputs: Shareable,
        fl_ctx: FLContext,
    ) -> int:

        pass

    def get_failure_count(
        self,
        dataset_name: str,
        feature_name: str,
        statistic_configs: StatisticConfig,
        inputs: Shareable,
        fl_ctx: FLContext,
    ) -> int:

        pass

    def get_sum(
        self,
        dataset_name: str,
        feature_name: str,
        statistic_configs: StatisticConfig,
        inputs: Shareable,
        fl_ctx: FLContext,
    ) -> float:

        pass

    def get_mean(
        self,
        dataset_name: str,
        feature_name: str,
        statistic_configs: StatisticConfig,
        inputs: Shareable,
        fl_ctx: FLContext,
    ) -> float:
        pass

    def get_stddev(
        self,
        dataset_name: str,
        feature_name: str,
        statistic_configs: StatisticConfig,
        inputs: Shareable,
        fl_ctx: FLContext,
    ) -> float:

        pass

    def get_variance_with_mean(
        self,
        dataset_name: str,
        feature_name: str,
        statistic_configs: StatisticConfig,
        inputs: Shareable,
        fl_ctx: FLContext,
    ) -> float:
        pass

    def get_histogram(
        self,
        dataset_name: str,
        feature_name: str,
        statistic_configs: StatisticConfig,
        inputs: Shareable,
        fl_ctx: FLContext,
    ) -> Histogram:

        pass

    def get_max_value(
        self,
        dataset_name: str,
        feature_name: str,
        statistic_configs: StatisticConfig,
        inputs: Shareable,
        fl_ctx: FLContext,
    ) -> float:
        """
        get randomized max value
        """
        pass

    def get_min_value(
        self,
        dataset_name: str,
        feature_name: str,
        statistic_configs: StatisticConfig,
        inputs: Shareable,
        fl_ctx: FLContext,
    ) -> float:
        """
        get randomized min value
        """
        pass

    def get_number_of_bins(self, feature_name: str, hist_config: dict) -> int:
        pass

    def get_bin_range(
        self, feature_name: str, global_min_value: float, global_max_value: float, hist_config: dict
    ) -> List[float]:

        pass

    def get_quantiles_and_centroids(
        self,
        dataset_name: str,
        feature_name: str,
        statistic_configs: StatisticConfig,
        inputs: Shareable,
        fl_ctx: FLContext,
    ) -> dict:
        pass

    def _get_global_value_from_input(self, statistic_key: str, dataset_name: str, feature_name: str, inputs):
        pass
