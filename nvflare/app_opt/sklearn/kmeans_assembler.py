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


import numpy as np
from sklearn.cluster import KMeans

from nvflare.apis.dxo import DXO, DataKind
from nvflare.apis.fl_context import FLContext
from nvflare.app_common.aggregators.assembler import Assembler
from nvflare.app_common.app_constant import AppConstants


class KMeansAssembler(Assembler):
    """Assembler for K-Means clustering using mini-batch aggregation strategy.

    This assembler implements the aggregation logic for federated K-Means clustering
    following the Mini-Batch K-Means approach where:
    - Round 0: Collect initial centers from all clients and perform one round of K-Means
      to generate the initial global centers
    - Subsequent rounds: Aggregate centers using weighted averaging based on counts,
      following the mini-batch update rule

    The assembler maintains:
    - center: Global cluster centers
    - count: Per-center counts for weighted aggregation
    """

    def __init__(self):
        super().__init__(data_kind=DataKind.WEIGHTS)
        # Aggregator needs to keep record of historical
        # center and count information for mini-batch kmeans
        self.center = None
        self.count = None
        self.n_cluster = 0

    def get_model_params(self, dxo: DXO):
        pass

    def assemble(self, data: dict[str, dict], fl_ctx: FLContext) -> DXO:
        pass
