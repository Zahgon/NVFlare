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

import base64
import logging
from abc import ABC, abstractmethod
from typing import Dict

from torch.utils.data import DataLoader, Dataset

from nvflare.apis.dxo import DXO, from_dict
from nvflare.edge.model_protocol import ModelBufferType, ModelEncoding, ModelNativeFormat, verify_payload
from nvflare.edge.simulation.device_task_processor import DeviceTaskProcessor
from nvflare.edge.web.models.job_response import JobResponse
from nvflare.edge.web.models.task_response import TaskResponse
from nvflare.fuel.utils.import_utils import optional_import
from nvflare.fuel.utils.validation_utils import check_positive_int

_load_for_executorch_for_training_from_buffer, _ = optional_import(
    "executorch.extension.training",
    name="_load_for_executorch_for_training_from_buffer",
    descriptor=(
        "executorch is required for {}. " "See: https://pytorch.org/executorch/stable/getting-started-setup.html"
    ),
)
get_sgd_optimizer, _ = optional_import(
    "executorch.extension.training",
    name="get_sgd_optimizer",
    descriptor=(
        "executorch is required for {}. " "See: https://pytorch.org/executorch/stable/getting-started-setup.html"
    ),
)

log = logging.getLogger(__name__)


def tensor_dict_to_json(d):
    pass


def clone_params(et_params):
    pass


def calc_params_diff(initial_p, last_p):
    pass


class ETTaskProcessor(DeviceTaskProcessor, ABC):
    """Base ExecutorTorch task processor."""

    def __init__(
        self,
        data_path: str,
        training_config: Dict = None,
    ):
        """Initialize the task processor.

        Args:
            data_path: Path to the dataset
            training_config: Configuration for training including:
                - batch_size (int): Size of each training batch (default: 32)
                - shuffle (bool): Whether to shuffle the dataset (default: True)
                - num_workers (int): Number of worker processes for data loading (default: 0)
                - learning_rate (float): Learning rate for optimization (default: 0.1)
                - momentum (float): Momentum factor (default: 0.0)
                - weight_decay (float): Weight decay factor (default: 0.0)
                - dampening (float): Dampening for momentum (default: 0.0)
                - nesterov (bool): Enables Nesterov momentum (default: False)
                - epoch (int): Number of training epochs (default: 1)
        """
        DeviceTaskProcessor.__init__(self)
        self.data_path = data_path
        self._dataset = None

        # Set default training configuration
        self.training_config = {
            "batch_size": 32,
            "shuffle": True,
            "num_workers": 0,
            "learning_rate": 0.1,
            "momentum": 0.0,
            "weight_decay": 0.0,
            "dampening": 0.0,
            "nesterov": False,
            "epoch": 1,
        }
        # Update with user-provided config
        if training_config:
            self.training_config.update(training_config)

        check_positive_int("epoch", self.training_config["epoch"])

    @abstractmethod
    def create_dataset(self, data_path: str) -> Dataset:
        """Create dataset for training.

        Note: This method may perform expensive I/O operations.

        Args:
            data_path: Path to dataset

        Returns:
            Dataset: PyTorch dataset for training
        """
        pass

    def get_dataset(self) -> Dataset:
        """Get the dataset, creating it if necessary (cached)."""
        pass

    def setup(self, job: JobResponse) -> None:
        """Set up the task processor for a new job.

        Args:
            job: Job response containing job information and configuration
        """
        pass

        # Additional setup could be added here, such as:
        # - Loading job-specific configurations
        # - Setting up logging/monitoring
        # - Initializing job-specific resources

    def shutdown(self) -> None:
        """Clean up resources when shutting down."""
        pass
        # Add cleanup code here if needed

    def run_training(self, et_model, total_epochs: int = 1) -> Dict:
        """Run training loop.

        Args:
            et_model: ExecutorTorch model
            total_epochs: Number of epochs to train

        Returns:
            dict: Training results with parameter differences
        """
        pass

    def process_task(self, task: TaskResponse) -> dict:
        """Process received task and return results.

        Args:
            task: The task response containing model and instructions

        Returns:
            dict: Results from training

        Raises:
            ValueError: If task data is invalid or protocol validation fails
            RuntimeError: If training operations fail
        """
        pass
