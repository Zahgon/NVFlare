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

import copy
from math import sqrt
from typing import Dict, List, TypeVar

from nvflare.app_common.abstract.statistics_spec import Bin, BinRange, DataType, Feature, Histogram, HistogramType
from nvflare.app_common.app_constant import StatisticsConstants as StC

T = TypeVar("T")


def get_initial_structure(client_metrics: dict, ordered_metrics: dict) -> dict:
    """Calculate initial output structure that is common at all the hierarchical levels.

    Args:
        client_metrics: Local stats for each client.
        ordered_metrics: Ordered target metrics.

    Returns:
        A dict containing initial output structure.
    """
    pass


def create_output_structure(
    client_metrics: dict, metric_task: str, ordered_metrics: dict, hierarchy_config: dict
) -> dict:
    """Recursively calculate the hierarchical global stats structure from the given hierarchy config.

    Args:
        client_metrics: Local stats for each client.
        metric_task: Statistics task.
        ordered_metrics: Ordered target metrics.
        hierarchy_config: Hierarchy configuration for the global stats.

    Returns:
        A dict containing hierarchical global stats structure.
    """
    def recursively_add_values(structure: dict, value_json: dict, metric_task: str, ordered_metrics: dict):
        pass
    pass


def get_output_structure(client_metrics: dict, metric_task: str, ordered_metrics: dict, hierarchy_config: dict) -> dict:
    """Create required global statistics hierarchical output structure.

    Args:
        client_metrics: Local stats for each client.
        metric_task: Statistics task.
        ordered_metrics: Ordered target metrics.
        hierarchy_config: Hierarchy configuration for the global stats.

    Returns:
        A dict containing hierarchical global stats structure that also includes
        top level global stats structure.
    """
    pass


def update_output_strcture(
    client_metrics: dict,
    metric_task: str,
    ordered_metrics: dict,
    global_metrics: dict,
) -> None:
    """Update global statistics hierarchical output structure with the new ordered metrics.

    Args:
        client_metrics: Local stats for each client.
        metric_task: Statistics task.
        ordered_metrics: Ordered target metrics.
        global_metrics: The current global metrics.

    Returns:
        A dict containing updated hierarchical global stats.
    """
    pass


def get_global_stats(global_metrics: dict, client_metrics: dict, metric_task: str, hierarchy_config: dict) -> dict:
    """Get global hierarchical statistics for the given hierarchy config.

    Args:
        global_metrics: The current global metrics.
        client_metrics: Local stats for each client.
        metric_task: Statistics task.
        hierarchy_config: Hierarchy configuration for the global stats.


    Returns:
        A dict containing global hierarchical statistics.
    """
    pass


def accumulate_hierarchical_metrics(
    metric: str, client_name: str, metrics: dict, global_metrics: dict, hierarchy_config: dict
) -> dict:
    """Accumulate metrics at each hierarchical level.

    Args:
        metric: Metric to accumulate.
        client_name: Client name.
        metrics: Client metrics.
        global_metrics: The current global metrics.
        hierarchy_config:  Hierarchy configuration for the global stats.

    Returns:
        A dict containing accumulated hierarchical global statistics.
    """
    def recursively_accumulate_hierarchical_metrics(metric: str, client_name: str, metrics: dict, global_metrics: dict, dataset: str, feature: str, org: list):
        pass
    pass


def get_hierarchical_mins_or_maxs(
    metric: str, client_name: str, metrics: dict, global_metrics: dict, hierarchy_config: dict
) -> dict:
    """Calculate min or max at each hierarchical level.

    Args:
        metric: Metric to accumulate.
        client_name: Client name.
        metrics: Client metrics.
        global_metrics: The current global metrics.
        hierarchy_config:  Hierarchy configuration for the global stats.

    Returns:
        A dict containing updated hierarchical global statistics with
        accumulated mins or maxs.
    """
    def recursively_update_org_mins_or_maxs(metric: str, client_name: str, metrics: dict, global_metrics: dict, dataset: str, feature: str, org: list, op: str):
        pass
    pass


def get_hierarchical_means(metric: str, global_metrics: dict) -> dict:
    """Calculate means at each hierarchical level.

    Args:
        metric: Metric to accumulate.
        global_metrics: The current global metrics.

    Returns:
        A dict containing updated hierarchical global statistics with
        accumulated means.
    """
    def recursively_update_org_means(metrics: dict, global_metrics: dict, dataset: str, feature: str):
        pass
    pass


def get_hierarchical_histograms(
    metric: str, client_name: str, metrics: dict, global_metrics: dict, hierarchy_config: dict
) -> dict:
    """Calculate histograms at each hierarchical level.

    Args:
        metric: Metric to accumulate.
        client_name: Client name.
        metrics: Client metrics.
        global_metrics: The current global metrics.
        hierarchy_config:  Hierarchy configuration for the global stats.

    Returns:
        A dict containing updated hierarchical global statistics with
        accumulated histograms.
    """
    def recursively_accumulate_org_histograms(metric: str, client_name: str, metrics: dict, global_metrics: dict, dataset: str, feature: str, org: list, histogram: dict):
        pass
    pass


def get_hierarchical_stddevs(global_metrics: dict) -> dict:
    """Calculate stddevs at each hierarchical level.

    Args:
        global_metrics: The current global metrics.

    Returns:
        A dict containing updated hierarchical global statistics with
        accumulated stddevs.
    """
    def recursively_update_org_stddevs(global_metrics: dict, dataset: str, feature: str):
        pass
    pass


def get_hierarchical_levels(data: dict, level: int = 0, levels_dict: dict = None) -> dict:
    """Calculate number of hierarchical levels from the given hierarchy config.

    Args:
        data: Hierarchy configuration for the global stats.
        level: The current hierarchical level (used for recursive calls).
        levels_dict: The accumulated levels dict (used for recursive calls).

    Returns:
        A dict containing containing hierarchical levels.
    """
    pass


def get_client_hierarchy(hierarchy_config: dict, client_name: str, path=None) -> list:
    """Calculate hierarchy for the given client name.

    Args:
        hierarchy_config: Hierarchy configuration for the global stats.
        client_name: Client name.
        path: The accumulated hierarchy path (used for recursive calls).

    Returns:
        A list containing hierarchy levels for the client.
    """
    pass


def bins_to_dict(bins: List[Bin]) -> Dict[BinRange, float]:
    """Convert histogram bins to a 'dict'.

    Args:
        bins: Histogram bins.

    Returns:
        A dict containing histogram bins.
    """
    pass


def filter_numeric_features(ds_features: Dict[str, List[Feature]]) -> Dict[str, List[Feature]]:
    """Filter numeric features.

    Args:
        ds_features: A features dict.

    Returns:
        A dict containing numeric features.
    """
    pass
