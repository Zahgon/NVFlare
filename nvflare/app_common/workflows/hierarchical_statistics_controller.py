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

import json
import os
from typing import Dict, List, Optional

from nvflare.apis.controller_spec import Task
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.apis.signal import Signal
from nvflare.app_common.abstract.statistics_spec import Histogram, StatisticConfig
from nvflare.app_common.app_constant import StatisticsConstants as StC
from nvflare.app_common.statistics.hierarchical_numeric_stats import get_global_stats
from nvflare.app_common.workflows.statistics_controller import StatisticsController
from nvflare.fuel.utils import fobs


class HierarchicalStatisticsController(StatisticsController):
    def __init__(
        self,
        statistic_configs: Dict[str, dict],
        writer_id: str,
        wait_time_after_min_received: int = 1,
        result_wait_timeout: int = 10,
        precision=4,
        min_clients: Optional[int] = None,
        enable_pre_run_task: bool = True,
        hierarchy_config: str = None,
    ):
        """Controller for hierarchical statistics.

        Args:
            statistic_configs: defines the input statistic to be computed and each statistic's configuration, see below for details.
            writer_id: ID for StatisticsWriter. The StatisticWriter will save the result to output specified by the
               StatisticsWriter
            wait_time_after_min_received: numbers of seconds to wait after minimum number of clients specified has received.
            result_wait_timeout: numbers of seconds to wait until we received all results.
               Notice this is after the min_clients have arrived, and we wait for result process
               callback, this becomes important if the data size to be processed is large
            precision:  number of precision digits
            min_clients: if specified, min number of clients we have to wait before process.
            hierarchy_config: Hierarchy specification file providing details about all the clients and their hierarchy.

        This class is derived from 'StatisticsController' and overrides only methods required to output calculated global
        statistics in given hierarchical order.

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

        For 'hierarchy_config', below is an example hierarchy specification with 4 level hierarchy for 9 NVFLARE clients with the names ranging
        from 'Device-1' to 'Device-9' and with hierarchical levels named 'Manufacturers', 'Orgs', 'Locations', 'Devices' with
        'Manufacturers' being the top most hierarchical level and "Devices" being the lowest hierarchical level:

        .. code-block:: text

           {
                "Manufacturers": [
                    {
                    "Name": "Manufacturer-1",
                    "Orgs": [
                        {
                        "Name": "Org-1",
                        "Locations": [
                            {
                            "Name": "Location-1",
                            "Devices": ["Device-1", "Device-2"]
                            },
                            {
                            "Name": "Location-2",
                            "Devices": ["Device-3"]
                            }
                        ]
                        },
                        {
                        "Name": "Org-2",
                        "Locations": [
                            {
                            "Name": "Location-1",
                            "Devices": ["Device-4", "Device-5"]
                            },
                            {
                            "Name": "Location-2",
                            "Devices": ["Device-6"]
                            }
                        ]
                        }
                    ]
                    },
                    {
                    "Name": "Manufacturer-2",
                    "Orgs": [
                        {
                        "Name": "Org-3",
                        "Locations": [
                            {
                            "Name": "Location-1",
                            "Devices": ["Device-7", "Device-8"]
                            },
                            {
                            "Name": "Location-6",
                            "Devices": ["Device-9"]
                            }
                        ]
                        }
                    ]
                    }
                ]
            }

        """
        super().__init__(
            statistic_configs,
            writer_id,
            wait_time_after_min_received,
            result_wait_timeout,
            precision,
            min_clients,
            enable_pre_run_task,
        )
        self.hierarchy_config = hierarchy_config

    def statistics_task_flow(self, abort_signal: Signal, fl_ctx: FLContext, statistic_task: str):
        """Statistics task flow for the given task.

        Args:
            abort_signal: Abort signal.
            fl_ctx: The FLContext.
            statistic_task: Statistics task.
        """
        pass

    def _recursively_round_global_stats(self, global_stats):
        """Apply given precision to the calculated global statistics.

        Args:
            global_stats: Global stats.

        Returns:
            A dict containing global stats with applied precision.
        """
        pass

    def _combine_all_statistics(self):
        """Get combined global statistics with precision applied.

        Returns:
            A dict containing global statistics with precision applied.
        """
        pass

    def _prepare_inputs(self, statistic_task: str) -> Shareable:
        """Prepare inputs for the given task.

        Args:
            statistic_task: Statistics task.

        Returns:
            A dict containing inputs.
        """
        pass
