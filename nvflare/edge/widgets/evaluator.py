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
import importlib
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, Optional, Union

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.app_common.abstract.model import ModelLearnableKey
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.app_event_type import AppEventType
from nvflare.fuel.utils.validation_utils import check_positive_int
from nvflare.widgets.widget import Widget

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class GlobalEvaluator(Widget):
    def __init__(
        self,
        model_path: Union[str, nn.Module, Dict],
        eval_frequency: int = 1,
        torchvision_dataset: Optional[Dict] = None,
        custom_dataset: Optional[Dict] = None,
    ):
        """Initialize the evaluator with either a dataset path or custom dataset.

        Args:
            model_path: PyTorch model to evaluate. Can be:
                - An nn.Module instance
                - A string class path (e.g., "mymodule.MyModel")
                - A dict config with 'path' and optional 'args' keys
                  (e.g., {"path": "mymodule.MyModel", "args": {"num_classes": 10}})
            eval_frequency: Frequency of evaluation (evaluate every N rounds)
            torchvision_dataset: Torchvision dataset (for standard datasets like CIFAR10)
            custom_dataset: Dictionary containing 'data' and 'labels' tensors
        """
        super().__init__()
        if torchvision_dataset is None and custom_dataset is None:
            raise ValueError("Must provide either torchvision_dataset or custom_dataset")
        if torchvision_dataset is not None and custom_dataset is not None:
            raise ValueError("Cannot provide both torchvision_dataset and custom_dataset")

        if isinstance(model_path, nn.Module):
            pass
        elif isinstance(model_path, dict):
            if "path" not in model_path:
                raise ValueError("model_path dict must contain 'path' key with the model class path")
        elif not isinstance(model_path, str):
            raise ValueError(
                f"model_path must be nn.Module, str class path, or dict config, but got {type(model_path)}"
            )

        # Validate eval_frequency - positive integer
        check_positive_int("eval_frequency", eval_frequency)

        self.model_path = model_path
        self.eval_frequency = eval_frequency
        self.torchvision_dataset = torchvision_dataset
        self.custom_dataset = custom_dataset
        self.batch_size = 4
        self.model = None
        self.data_loader = None
        self.tb_writer = None

        # Initialize thread pool, single worker to ensure evaluations are sequential
        # to avoid model version conflicts / extra GPU memory usage to sync multiple models
        self._thread_pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="GlobalEvaluator")

        # Register event handlers
        self.register_event_handler(EventType.START_RUN, self._initialize)
        self.register_event_handler(AppEventType.GLOBAL_WEIGHTS_UPDATED, self.evaluate)
        self.register_event_handler(EventType.END_RUN, self._handle_end_run)

    def _load_model_class(self, class_path: str, fl_ctx: FLContext) -> Any:
        """Load model class from class path.

        Args:
            class_path (str): model class path in format "module.submodule.ClassName"
            fl_ctx (FLContext): FL context

        Returns:
            model class (not instance)
        """
        pass

    def _instantiate_model(self, fl_ctx: FLContext) -> Optional[nn.Module]:
        """Instantiate model from model_path config.

        Args:
            fl_ctx (FLContext): FL context

        Returns:
            nn.Module instance or None on failure
        """
        pass

    def _create_data_loader(self):
        pass

    def _to_tensor(self, v) -> torch.Tensor:
        """Convert value to tensor, reusing memory when possible."""
        pass

    def _eval_model(self) -> Dict[str, float]:
        pass

    def _evaluate_async(self, global_weights: Dict, current_round: int, evaluation_id: str):
        """Run evaluation in a separate thread."""
        pass

    def _initialize(self, _event_type: str, fl_ctx: FLContext):
        # Initialize the model
        pass

    def _is_initialized(self) -> bool:
        """Check if the evaluator is properly initialized."""
        pass

    def evaluate(self, _event_type: str, fl_ctx: FLContext):
        # Safety check - ensure we're initialized
        pass

    def _handle_end_run(self, _event_type: str, fl_ctx: FLContext):
        """Handle the END_RUN event to ensure proper cleanup."""
        pass
