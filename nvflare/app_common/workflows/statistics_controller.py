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

import time
from typing import Callable, Dict, List, Optional

from nvflare.apis.client import Client
from nvflare.apis.controller_spec import ClientTask, Task
from nvflare.apis.dxo import from_shareable
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.impl.controller import Controller
from nvflare.apis.shareable import Shareable
from nvflare.apis.signal import Signal
from nvflare.app_common.abstract.statistics_spec import Bin, Histogram, StatisticConfig
from nvflare.app_common.abstract.statistics_writer import StatisticsWriter
from nvflare.app_common.app_constant import StatisticsConstants as StC
from nvflare.app_common.statistics.numeric_stats import get_global_stats
from nvflare.app_common.statistics.statisitcs_objects_decomposer import fobs_registration
from nvflare.fuel.utils import fobs


class StatisticsController(Controller):
    def __init__(
        self,
        statistic_configs: Dict[str, dict],
        writer_id: str,
        wait_time_after_min_received: int = 1,
        result_wait_timeout: int = 10,
        precision=4,
        min_clients: Optional[int] = None,
        enable_pre_run_task: bool = True,
    ):
        """Controller for Statistics.

        Args:
            statistic_configs: defines the input statistic to be computed and each statistic's configuration, see below for details.
            writer_id: ID for StatisticsWriter. The StatisticWriter will save the result to output specified by the
               StatisticsWriter
            wait_time_after_min_received: numbers of seconds to wait after minimum numer of clients specified has received.
            result_wait_timeout: numbers of seconds to wait until we received all results.
               Notice this is after the min_clients have arrived, and we wait for result process
               callback, this becomes important if the data size to be processed is large
            precision:  number of precision digits
            min_clients: if specified, min number of clients we have to wait before process.

        For statistic_configs, the key is one of statistics' names sum, count, mean, stddev, histogram, and
        the value is the arguments needed. All other statistics except histogram require no argument.

        .. code-block:: text

            "statistic_configs": {
                "count": {},
                "mean": {},
                "sum": {},
                "stddev": {},
                "histogram": {
                    "*": {"bins": 20},
                    "Age": {"bins": 10, "range": [0, 120]}
                },
                quantile: {
                    "*": [25, 50, 75, 90],
                    "Age": [50, 75, 95]
                }
            },

        Histogram requires the following arguments:
            1) numbers of bins or buckets of the histogram
            2) the histogram range values [min, max]

        These arguments are different for each feature. Here are few examples:

        .. code-block:: text

            "histogram": {
                            "*": {"bins": 20 },
                            "Age": {"bins": 10, "range":[0,120]}
                         }

        The configuration specifies that the
        feature 'Age' will have 10 bins for and the range is within [0, 120).
        For all other features, the default ("*") configuration is used, with bins = 20.
        The range of histogram is not specified, thus requires the Statistics controller
        to dynamically estimate histogram range for each feature. Then this estimated global
        range (est global min, est. global max) will be used as the histogram range.

        To dynamically estimate such a histogram range, we need the client to provide the local
        min and max values in order to calculate the global bin and max value. In order to protect
        data privacy and avoid data leakage, a noise level is added to the local min/max
        value before sending to the controller. Therefore the controller only gets the 'estimated'
        values, and the global min/max are estimated, or more accurately, they are noised global min/max
        values.

        Here is another example:

        .. code-block:: text

            "histogram": {
                            "density": {"bins": 10, "range":[0,120]}
                         }

        In this example, there is no default histogram configuration for other features.

        This will work correctly if there is only one feature called "density"
        but will fail if there are other features in the dataset.

        In the following configuration:

        .. code-block:: text

            "statistic_configs": {
                "count": {},
                "mean": {},
                "stddev": {}
            }

        Only count, mean and stddev statistics are specified, so the statistics_controller
        will only set tasks to calculate these three statistics.

        """
        super().__init__()
        self.statistic_configs: Dict[str, dict] = statistic_configs
        self.writer_id = writer_id
        self.task_name = StC.FED_STATS_TASK
        self.client_statistics = {}
        self.global_statistics = {}
        self.client_features = {}
        self.result_wait_timeout = result_wait_timeout
        self.wait_time_after_min_received = wait_time_after_min_received
        self.precision = precision
        self.min_clients = min_clients
        self.result_cb_status = {}
        self.client_handshake_ok = {}

        self.enable_pre_run_task = enable_pre_run_task

        self.result_callback_fns: Dict[str, Callable] = {
            StC.STATS_1st_STATISTICS: self.results_cb,
            StC.STATS_2nd_STATISTICS: self.results_cb,
        }
        fobs_registration()
        self.fl_ctx = None
        self.abort_job_in_error = {
            ReturnCode.EXECUTION_EXCEPTION: True,
            ReturnCode.TASK_UNKNOWN: True,
            ReturnCode.EXECUTION_RESULT_ERROR: False,
            ReturnCode.TASK_DATA_FILTER_ERROR: True,
            ReturnCode.TASK_RESULT_FILTER_ERROR: True,
        }

    def start_controller(self, fl_ctx: FLContext):
        pass

    def control_flow(self, abort_signal: Signal, fl_ctx: FLContext):

        pass

    def stop_controller(self, fl_ctx: FLContext):
        pass

    def process_result_of_unknown_task(
        self, client: Client, task_name: str, client_task_id: str, result: Shareable, fl_ctx: FLContext
    ):
        pass

    def _get_all_statistic_configs(self) -> List[StatisticConfig]:

        pass

    def pre_run_task_flow(self, abort_signal: Signal, fl_ctx: FLContext):
        pass

    def statistics_task_flow(self, abort_signal: Signal, fl_ctx: FLContext, statistic_task: str):

        pass

    def handle_client_errors(self, rc: str, client_task: ClientTask, fl_ctx: FLContext):
        pass

    def results_pre_run_cb(self, client_task: ClientTask, fl_ctx: FLContext):
        pass

    def results_cb(self, client_task: ClientTask, fl_ctx: FLContext):
        pass

    def _validate_min_clients(self, min_clients: int, client_statistics: dict) -> bool:
        pass

    def post_fn(self, task_name: str, fl_ctx: FLContext):

        pass

    def _combine_all_statistics(self):
        pass

    @staticmethod
    def _apply_histogram_precision(bins: List[Bin], precision) -> List[Bin]:
        pass

    @staticmethod
    def _get_target_statistics(statistic_configs: dict, ordered_statistics: list) -> List[StatisticConfig]:
        # make sure the execution order of the statistics calculation

        pass

    def _prepare_inputs(self, statistic_task: str) -> Shareable:
        pass

    @staticmethod
    def _wait_for_all_results(
        logger,
        result_wait_timeout: float,
        requested_client_size: int,
        client_statistics: dict,
        sleep_time: float = 1,
        abort_signal=None,
    ) -> bool:
        """Waits for all results.

        For each statistic, we check if the number of requested clients (min_clients or all clients)
        is available, if not, we wait until result_wait_timeout.
        result_wait_timeout is reset for next statistic. result_wait_timeout is per statistic, not overall
        timeout for all results.

        Args:
            result_wait_timeout: timeout we have to wait for each statistic. reset for each statistic
            requested_client_size: requested client size, usually min_clients or all clients
            client_statistics: client specific statistics received so far
            abort_signal:  abort signal

        Returns: False, when job is aborted else True

        """
        pass

    def _get_result_cb(self, statistics_task: str):
        pass
