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

from typing import Dict, Tuple

from nvflare.apis.fl_component import FLComponent
from nvflare.app_common.abstract.statistics_spec import Histogram
from nvflare.app_common.app_constant import StatisticsConstants as StC
from nvflare.app_common.statistics.statistics_privacy_cleanser import StatisticsPrivacyCleanser


class HistogramBinsCleanser(FLComponent, StatisticsPrivacyCleanser):
    def __init__(self, max_bins_percent):
        """
        max_bins_percent:   max number of bins allowed in terms of percent of local data size.
                            Set this number to avoid number of bins equal or close equal to the
                            data size, which can lead to data leak.
                            for example: max_bins_percent = 10, means 10%
                            number of bins < max_bins_percent /100 * local count
        """
        super().__init__()
        self.max_bins_percent = max_bins_percent
        self.validate_inputs()

    def validate_inputs(self):
        pass

    def hist_bins_validate(self, client_name: str, statistics: Dict) -> Dict[str, Dict[str, bool]]:
        pass

    def apply(self, statistics: dict, client_name: str) -> Tuple[dict, bool]:
        pass
