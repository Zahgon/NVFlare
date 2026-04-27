# Copyright (c) 2026, NVIDIA CORPORATION.  All rights reserved.
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


"""
Feature Election Library for NVIDIA FLARE
High-level API for federated feature selection and training workflow.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

logger = logging.getLogger(__name__)


class FeatureElection:
    """
    High-level interface for Feature Election in NVIDIA FLARE.
    Simplifies integration with tabular datasets for federated feature selection.

    This class provides:
    - Easy data preparation and splitting
    - Local simulation for testing
    - Result management and persistence
    """

    def __init__(
        self,
        freedom_degree: float = 0.5,
        fs_method: str = "lasso",
        aggregation_mode: str = "weighted",
        auto_tune: bool = False,
        tuning_rounds: int = 5,
        eval_metric: str = "f1",
        wait_time_after_min_received: int = 10,
        fs_params: Optional[Dict] = None,
    ):
        if not 0 <= freedom_degree <= 1:
            raise ValueError("freedom_degree must be between 0 and 1")
        if aggregation_mode not in ["weighted", "uniform"]:
            raise ValueError("aggregation_mode must be 'weighted' or 'uniform'")
        if eval_metric not in ["f1", "accuracy"]:
            raise ValueError("eval_metric must be 'f1' or 'accuracy'")
        if tuning_rounds < 0:
            raise ValueError(f"tuning_rounds must be >= 0, got {tuning_rounds}")

        self.freedom_degree = freedom_degree
        self.fs_method = fs_method
        self.aggregation_mode = aggregation_mode
        self.auto_tune = auto_tune
        self.tuning_rounds = tuning_rounds
        self.eval_metric = eval_metric
        self.wait_time_after_min_received = wait_time_after_min_received
        # FS hyperparameters (e.g. {"alpha": 0.1} for Lasso) forwarded to the
        # executor; None means the executor uses its own defaults.
        self.fs_params = fs_params or {}

        # Storage for results
        self.global_mask = None
        self.selected_feature_names = None
        self.election_stats = {}

    def create_flare_job(
        self,
        job_name: str = "feature_election",
        output_dir: str = "jobs/feature_election",
        min_clients: int = 2,
        num_rounds: int = 5,
        client_sites: Optional[List[str]] = None,
    ) -> Dict[str, str]:
        """
        Generate FLARE job configuration.
        """
        pass

    def prepare_data_splits(
        self,
        df: pd.DataFrame,
        target_col: str,
        num_clients: int = 3,
        split_strategy: str = "stratified",
        split_ratios: Optional[List[float]] = None,
        random_state: int = 42,
        dirichlet_alpha: float = 0.5,
    ) -> List[Tuple[pd.DataFrame, pd.Series]]:
        """Prepare data splits for federated clients."""
        pass

    def simulate_election(
        self,
        client_data: List[Tuple[Union[pd.DataFrame, np.ndarray], Union[pd.Series, np.ndarray]]],
        feature_names: Optional[List[str]] = None,
    ) -> Dict:
        """Simulate election locally."""
        pass

    def apply_mask(self, X: Union[pd.DataFrame, np.ndarray]) -> Union[pd.DataFrame, np.ndarray]:
        """Apply global feature mask to new data."""
        pass

    def save_results(self, filepath: str):
        """Save results to JSON."""
        pass

    def load_results(self, filepath: str):
        """Load results from JSON."""
        pass


# --- HELPER FUNCTIONS ---


_FEATURE_ELECTION_INIT_PARAMS = {
    "aggregation_mode",
    "auto_tune",
    "tuning_rounds",
    "eval_metric",
    "wait_time_after_min_received",
    "fs_params",
}

_PREPARE_DATA_PARAMS = {
    "split_ratios",
    "random_state",
    "dirichlet_alpha",
}


def quick_election(
    df: pd.DataFrame,
    target_col: str,
    num_clients: int = 3,
    freedom_degree: float = 0.5,
    fs_method: str = "lasso",
    split_strategy: str = "stratified",
    **kwargs,
) -> Tuple[np.ndarray, Dict]:
    """
    Quick Feature Election for tabular data (one-line solution).

    ``**kwargs`` are routed to either :class:`FeatureElection` or
    :meth:`FeatureElection.prepare_data_splits` based on the parameter name.
    Recognised split parameters: ``split_ratios``, ``random_state``,
    ``dirichlet_alpha``.  All other kwargs are forwarded to
    :class:`FeatureElection` (e.g. ``aggregation_mode``, ``auto_tune``,
    ``fs_params``).
    """
    pass


def load_election_results(filepath: str) -> Dict:
    """
    Load election results from a JSON file.
    """
    pass
