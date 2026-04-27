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

import copy
from typing import List

import numpy as np

from nvflare.apis.fl_constant import FLMetaKey
from nvflare.app_common.abstract.fl_model import FLModel
from nvflare.app_common.aggregators.weighted_aggregation_helper import WeightedAggregationHelper
from nvflare.app_common.app_constant import AlgorithmConstants, AppConstants

from .base_fedavg import BaseFedAvg


class Scaffold(BaseFedAvg):
    """Controller for Scaffold Workflow. *Note*: This class is based on `ModelController`.
    Implements [SCAFFOLD](https://proceedings.mlr.press/v119/karimireddy20a.html).

    Provides the implementations for the `run` routine, controlling the main workflow:
        - def run(self)

    The parent classes provide the default implementations for other routines.

    Args:
        num_clients (int, optional): The number of clients. Defaults to 3.
        num_rounds (int, optional): The total number of training rounds. Defaults to 5.
        persistor_id (str, optional): ID of the persistor component. Defaults to "persistor".
        ignore_result_error (bool or None, optional): How to handle client result errors.
            - None: Dynamic mode (default) - ignore errors if min_responses still reachable, panic otherwise.
            - False: Strict mode - panic on any client error.
            - True: Resilient mode - always ignore client errors.
        allow_empty_global_weights (bool, optional): whether to allow empty global weights. Some pipelines can have
            empty global weights at first round, such that clients start training from scratch without any global info.
            Defaults to False.
        memory_gc_rounds (int, optional): Run memory cleanup (gc.collect + malloc_trim) every N rounds.
            Set to 0 to disable. Defaults to 0 (inherited from BaseFedAvg).
    """

    def initialize(self, fl_ctx):
        pass

    def run(self) -> None:
        pass


def scaffold_aggregate_fn(results: List[FLModel]) -> FLModel:
    # aggregates both the model weights and the SCAFFOLD control terms

    pass
