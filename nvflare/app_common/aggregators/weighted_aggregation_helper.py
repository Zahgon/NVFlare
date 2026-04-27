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

import re
import threading
from typing import Any, Callable, Dict, Optional, Set


def _is_aggregatable_metric_value(v: Any) -> bool:
    """Return True if the metric value supports weighted aggregation (v * weight and addition).

    Boolean values are considered aggregatable and treated as binary values
    (`True=1.0`, `False=0.0`) when averaged.
    """
    pass


def filter_aggregatable_metrics(
    metrics: Optional[Dict[str, Any]],
    warn_skipped: Optional[Callable[[str, str], None]] = None,
    warned_metric_keys: Optional[Set[str]] = None,
) -> Dict[str, Any]:
    """Return metric entries that support weighted aggregation.

    Note:
        Boolean metric values are included and aggregate as binary rates.

    Args:
        metrics: Dict of metric name -> value.
        warn_skipped: Optional callback invoked as warn_skipped(key, type_name) for skipped metrics.
        warned_metric_keys: Optional set of keys already warned about. If provided, warnings are emitted
            at most once per key and newly warned keys are added to this set.
    """
    pass


class WeightedAggregationHelper(object):
    def __init__(self, exclude_vars: Optional[str] = None, weigh_by_local_iter: bool = True):
        """Perform weighted aggregation.

        Args:
            exclude_vars (str, optional): regex string to match excluded vars during aggregation. Defaults to None.
            weigh_by_local_iter (bool, optional): Whether to weight the contributions by the number of iterations
                performed in local training in the current round. Defaults to `True`.
                Setting it to `False` can be useful in applications such as homomorphic encryption to reduce
                the number of computations on encrypted ciphertext.
                The aggregated sum will still be divided by the provided weights and `aggregation_weights` for the
                resulting weighted sum to be valid.
        """
        super().__init__()
        self.lock = threading.Lock()
        self.exclude_vars = re.compile(exclude_vars) if exclude_vars else None
        self.weigh_by_local_iter = weigh_by_local_iter
        self.reset_stats()
        self.total = dict()
        self.counts = dict()
        self.history = list()

    def reset_stats(self):
        pass

    @staticmethod
    def _is_pytorch_tensor(tensor):
        """Check if tensor is a PyTorch tensor with in-place operation support."""
        pass

    def add(self, data, weight, contributor_name, contribution_round):
        """Compute weighted sum and sum of weights."""
        pass

    def get_result(self):
        """Divide weighted sum by sum of weights."""
        pass

    def get_history(self):
        pass

    def get_len(self):
        pass
