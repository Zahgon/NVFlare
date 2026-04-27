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

import os
import time
from typing import Any, Dict, Optional, Set, Union

from nvflare.apis.fl_constant import FLMetaKey
from nvflare.app_common.abstract.fl_model import FLModel
from nvflare.app_common.aggregators.model_aggregator import ModelAggregator
from nvflare.app_common.aggregators.weighted_aggregation_helper import (
    WeightedAggregationHelper,
    filter_aggregatable_metrics,
)
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.app_event_type import AppEventType
from nvflare.app_common.utils.math_utils import parse_compare_criteria
from nvflare.app_common.utils.tensor_disk_offload_context import (
    apply_enable_tensor_disk_offload,
    restore_enable_tensor_disk_offload,
)
from nvflare.fuel.utils import fobs
from nvflare.fuel.utils.log_utils import center_message

from .base_fedavg import BaseFedAvg


class FedAvg(BaseFedAvg):
    """Controller for FedAvg Workflow with optional Early Stopping and Model Selection.

    *Note*: This class is based on the `ModelController`.
    Implements [FederatedAveraging](https://arxiv.org/abs/1602.05629).

    Uses InTime (streaming) aggregation for memory efficiency - each client result is
    aggregated immediately upon receipt rather than collecting all results first.

    Supports custom aggregators via the ModelAggregator interface.

    Provides the implementations for the `run` routine, controlling the main workflow:
        - def run(self)

    The parent classes provide the default implementations for other routines.

    For simple model persistence without complex ModelPersistor setup, you can:
    1. Pass `model` (dict of params) and `save_filename`
    2. Override `save_model()` and `load_model()` for framework-specific serialization

    Args:
        num_clients (int, optional): The number of clients. Defaults to 3.
        num_rounds (int, optional): The total number of training rounds. Defaults to 5.
        start_round (int, optional): The starting round number.
        persistor_id (str, optional): ID of the persistor component. Defaults to "persistor".
            If empty and model is provided, uses simple save_model/load_model methods.
        model (dict or FLModel, optional): Initial model parameters. If provided,
            this is used instead of loading from persistor. Defaults to None.
        save_filename (str, optional): Filename for saving the best model. Defaults to
            "FL_global_model.pt". Only used when persistor_id is empty.
        aggregator (ModelAggregator, optional): Custom aggregator for combining client
            model updates. Must implement accept_model(), aggregate_model(), reset_stats().
            If None, uses built-in weighted averaging (memory-efficient). Defaults to None.
        stop_cond (str, optional): Early stopping condition based on metric. String
            literal in the format of '<key> <op> <value>' (e.g. "accuracy >= 80").
            If None, early stopping is disabled. Defaults to None.
        patience (int, optional): The number of rounds with no improvement after which
            FL will be stopped. Only applies if stop_cond is set. Defaults to None.
        task_name (str, optional): Task name for training. Defaults to "train".
        exclude_vars (str, optional): Regex pattern for variables to exclude from
            aggregation. Defaults to None. Only used when no custom aggregator is provided.
        aggregation_weights (dict, optional): Per-client aggregation weights.
            Defaults to None (equal weights). Only used when no custom aggregator is provided.
        enable_tensor_disk_offload (bool, optional): Download tensors to disk during FOBS streaming
            instead of deserializing into memory. Reduces peak server memory from ~N× to ~1×
            model size during aggregation. When used with a custom aggregator, lazy refs are
            passed through directly and must be handled by that aggregator. Defaults to False.
    """

    def __init__(
        self,
        *args,
        model: Optional[Union[Dict, FLModel]] = None,
        save_filename: Optional[str] = "FL_global_model.pt",
        aggregator: Optional[ModelAggregator] = None,
        stop_cond: Optional[str] = None,
        patience: Optional[int] = None,
        task_name: Optional[str] = "train",
        exclude_vars: Optional[str] = None,
        aggregation_weights: Optional[Dict[str, float]] = None,
        enable_tensor_disk_offload: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        # Simple model persistence (alternative to persistor)
        self.model = model
        self.save_filename = save_filename

        # Custom aggregator (optional)
        self.aggregator = aggregator

        # Early stopping configuration
        self.stop_cond = stop_cond
        self.patience = patience
        self.task_name = task_name

        # Aggregation configuration (used only when no custom aggregator)
        self.exclude_vars = exclude_vars
        self.aggregation_weights = aggregation_weights or {}
        self.enable_tensor_disk_offload = enable_tensor_disk_offload

        # Parse stop condition
        if self.stop_cond:
            self.stop_condition = parse_compare_criteria(stop_cond)
        else:
            self.stop_condition = None

        # Early stopping state
        self.num_fl_rounds_without_improvement: int = 0
        self.best_target_metric_value: Any = None

        # InTime aggregation helpers (reset each round, used only when no custom aggregator)
        self._aggr_helper: Optional[WeightedAggregationHelper] = None
        self._aggr_metrics_helper: Optional[WeightedAggregationHelper] = None
        self._all_metrics: bool = True
        self._warned_metric_keys: Set[str] = set()  # warn at most once per key (across clients/rounds)
        self._received_count: int = 0
        self._expected_count: int = 0
        self._params_type = None  # Only store params_type, not full result

    def run(self) -> None:
        pass

    def _aggregate_one_result(self, result: FLModel) -> None:
        """Callback: aggregate ONE client result immediately (InTime aggregation)."""
        pass

    def _get_aggregated_result(self) -> FLModel:
        """Get the final aggregated result after all clients have responded."""
        pass

    def should_stop(self, metrics: Optional[Dict] = None) -> bool:
        """Checks whether the current FL experiment should stop.

        Args:
            metrics (Dict, optional): experiment metrics.

        Returns:
            True if the experiment should stop, False otherwise.
        """
        pass

    def is_curr_model_better(self, curr_model: FLModel) -> bool:
        """Checks if the new model is better than the current best model.

        Args:
            curr_model (FLModel): the new model to evaluate.

        Returns:
            True if the new model is better than the current best model, False otherwise
        """
        pass

    def load_model(self) -> FLModel:
        """Load model. Uses persistor if available, otherwise uses load_model_file.

        Override `load_model_file` for framework-specific deserialization (e.g., torch.load).

        Returns:
            FLModel: loaded model, or None if loading fails
        """
        pass

    def save_model(self, model: FLModel) -> None:
        """Save model. Uses persistor if available, otherwise uses save_model_file.

        Override `save_model_file` for framework-specific serialization (e.g., torch.save).

        Args:
            model (FLModel): model to save
        """
        pass

    def save_model_file(self, model: FLModel, filepath: str) -> None:
        """Save model to file. Override this for framework-specific serialization.

        Default implementation uses FOBS (pickle-compatible).
        For PyTorch, override with: torch.save(model.params, filepath)

        Args:
            model (FLModel): model to save
            filepath (str): path to save the model
        """
        pass

    def load_model_file(self, filepath: str) -> FLModel:
        """Load model from file. Override this for framework-specific deserialization.

        Default implementation uses FOBS (pickle-compatible).
        For PyTorch, override with: FLModel(params=torch.load(filepath))

        Args:
            filepath (str): path to load the model from

        Returns:
            FLModel: loaded model
        """
        pass
