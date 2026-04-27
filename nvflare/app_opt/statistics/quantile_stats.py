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

from typing import Dict

from nvflare.app_common.app_constant import StatisticsConstants as StC
from nvflare.app_common.statistics.statistics_config_utils import get_target_quantiles
from nvflare.fuel.utils.log_utils import get_module_logger

try:
    from fastdigest import TDigest

    TDIGEST_AVAILABLE = True
except ImportError:
    TDIGEST_AVAILABLE = False


logger = get_module_logger(name="quantile_stats")


def get_quantiles(stats: Dict, statistic_configs: Dict, precision: int):

    pass


def merge_quantiles(metrics: Dict[str, Dict[str, Dict]], g_digest: dict) -> dict:

    pass


def compute_quantiles(g_digest: dict, quantile_config: Dict, precision: int) -> Dict:
    pass
