# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
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

from typing import List, Tuple, Union

import numpy as np

from nvflare.apis.dxo import DXO, DataKind, MetaKey
from nvflare.apis.dxo_filter import DXOFilter
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable

# Keep temporary SVT arrays bounded for large models.
_SVT_CHUNK_SIZE = 1_000_000


def _sample_partition_counts(group_counts: List[int], total_to_sample: int, replace: bool) -> List[int]:
    """Partition ``total_to_sample`` across groups while preserving the total.

    The last group absorbs any remaining samples after the sequential draws so the
    returned counts always sum to ``total_to_sample``. When ``replace`` is ``True``,
    a group can receive more selected samples than accepted entries because the
    downstream selection step samples from that group's accepted entries with
    replacement.
    """
    pass


class SVTPrivacy(DXOFilter):
    def __init__(
        self, fraction=0.1, epsilon=0.1, noise_var=0.1, gamma=1e-5, tau=1e-6, data_kinds: [str] = None, replace=True
    ):
        """Implementation of the standard Sparse Vector Technique (SVT) differential privacy algorithm.

        lambda_rho = gamma * 2.0 / epsilon
        threshold = tau + np.random.laplace(scale=lambda_rho)

        Args:
            fraction (float, optional): used to determine dataset threshold. Defaults to 0.1.
            epsilon (float, optional): Defaults to 0.1.
            noise_var (float, optional): additive noise. Defaults to 0.1.
            gamma (float, optional): Defaults to 1e-5.
            tau (float, optional): Defaults to 1e-6.
            data_kinds (str, optional): Defaults to None.
            replace (bool): whether to sample with replacement. Defaults to True.
        """
        if not data_kinds:
            data_kinds = [DataKind.WEIGHT_DIFF, DataKind.WEIGHTS]

        super().__init__(supported_data_kinds=[DataKind.WEIGHTS, DataKind.WEIGHT_DIFF], data_kinds_to_filter=data_kinds)

        self.fraction = fraction  # fraction of the model to upload
        self.epsilon = epsilon
        self.eps_2 = None  # to be derived from eps_1
        self.noise_var = noise_var
        self.gamma = gamma
        self.tau = tau
        self.replace = replace

    def process_dxo(self, dxo: DXO, shareable: Shareable, fl_ctx: FLContext) -> Union[None, DXO]:
        """Compute the differentially private SVT.

        Args:
            dxo: information from client
            shareable: that the dxo belongs to
            fl_ctx: context provided by workflow

        Returns: filtered result.
        """
        pass
