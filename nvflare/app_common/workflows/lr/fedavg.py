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
"""
Federated Averaging for Logistic Regression with Newton-Raphson method
using Numpy
"""
from typing import List, Optional

import numpy as np

from nvflare.apis.fl_constant import FLMetaKey
from nvflare.app_common.abstract.fl_model import FLModel
from nvflare.app_common.aggregators.weighted_aggregation_helper import WeightedAggregationHelper
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.np.constants import NPConstants
from nvflare.app_common.np.np_model_persistor import NPModelPersistor
from nvflare.app_common.workflows.base_fedavg import BaseFedAvg
from nvflare.app_common.workflows.lr.np_persistor import LRModelPersistor


class FedAvgLR(BaseFedAvg):
    def __init__(
        self,
        damping_factor: float,
        epsilon: float = 1.0,
        model_dir: str = "models",
        model_name: str = "weights.npy",
        n_features: int = 13,
        aggregator: WeightedAggregationHelper = WeightedAggregationHelper(),
        persistor: Optional[NPModelPersistor] = None,
        *args,
        **kwargs,
    ):
        """
        Initialize the FedAvgLR class for Federated Averaging with Newton-Raphson optimization.

        Args:
            damping_factor (float): Damping factor for Newton-Raphson updates, used to control the step size.
            epsilon (float, optional): Regularization factor to avoid empty Hessian matrix inversion. Defaults to 1.0.
            model_dir (str, optional): Directory to save and load the model. Defaults to "models".
            model_name (str, optional): Name of the model file. Defaults to "weights.npy".
            n_features (int, optional): Number of features in the dataset. Defaults to 13.
            aggregator (WeightedAggregationHelper, optional): Helper for weighted aggregation of model updates.
            persistor (Optional[NPModelPersistor], optional): Custom persistor for model saving and loading. If not provided, a default LRModelPersistor is used.
            *args: Additional positional arguments passed to the base class.
            **kwargs: Additional keyword arguments passed to the base class.

        This class implements the Federated Averaging algorithm using the Newton-Raphson method for optimization.
        It supports flexible model persistence through customizable persistors, allowing integration with different
        storage backends or model formats.
        """
        super().__init__(*args, **kwargs)
        self.damping_factor = damping_factor
        self.epsilon = epsilon
        self.model_dir = model_dir
        self.model_name = model_name
        self.n_features = n_features
        self.aggregator = aggregator
        self._default_persistor = LRModelPersistor(
            model_dir=self.model_dir, model_name=self.model_name, n_features=self.n_features
        )
        self.persistor = persistor

    def run(self) -> None:
        """
        The run function executes the logic of federated
        second order Newton-Raphson optimization.

        """
        pass

    def newton_raphson_aggregator_fn(self, results: List[FLModel]):
        """
        Custom aggregator function for second order Newton-Raphson
        optimization.

        This uses the default thread-safe WeightedAggregationHelper,
        which implement a weighted average of all values received from
        a `result` dictionary.

        Args:
            results: a list of `FLModel`s. Each `FLModel` is received
                from a client. The field `params` is a dictionary that
                contains values to be aggregated: the gradient and hessian.
        """
        pass

    def update_model(self, model, model_update, replace_meta=True) -> FLModel:
        """
        Update logistic regression parameters based on
        aggregated gradient and hessian.

        """
        pass

    def load_model(self) -> FLModel:
        pass

    def save_model(self, model: FLModel) -> None:
        pass
