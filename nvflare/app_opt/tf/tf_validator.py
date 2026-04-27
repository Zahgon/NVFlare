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

import tensorflow as tf

from nvflare.apis.dxo import DXO, DataKind, from_shareable
from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_opt.tf.utils import unflat_layer_weights_dict
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.security.logging import secure_format_exception


class TFValidator(Executor):
    def __init__(
        self,
        model: tf.keras.Model,
        data_loader=None,
        metric_fn=None,
    ):
        """Component-based TensorFlow Validator for cross-site evaluation.

        This validator provides an alternative to the Client API pattern (flare.is_evaluate()) for
        TensorFlow cross-site evaluation. Use this when you prefer a component-based approach or when
        your validation logic is separate from your training script.

        **When to use TFValidator vs Client API pattern:**

        Use TFValidator (component-based) when:
        - You prefer explicit validation components separate from training logic
        - Your validation code is reusable across multiple projects
        - You want validation to work without modifying your training script
        - Your recipe is CSE-only (no training, only validation)

        Use Client API pattern (flare.is_evaluate()) when:
        - Your validation logic is tightly coupled with training (e.g., same preprocessing)
        - You want a single script that handles both training and validation
        - You're already using Client API for training (recommended for most cases)

        **Default recommendation**: Use Client API pattern (like PyTorch) for consistency and simplicity.
        TFValidator is provided for flexibility and backward compatibility with NumPy-style workflows.

        Example (Component-based with TFValidator):
            ```python
            from nvflare.app_opt.tf.recipes import FedAvgRecipe
            from nvflare.app_opt.tf.tf_validator import TFValidator
            from nvflare.recipe.utils import add_cross_site_evaluation

            # Create recipe
            recipe = FedAvgRecipe(
                name="my-job",
                min_clients=2,
                num_rounds=3,
                model=my_model,
                train_script="client.py"
            )

            # Add CSE
            add_cross_site_evaluation(recipe)

            # Manually add TFValidator if you prefer component-based validation
            validator = TFValidator(
                model=my_model,
                data_loader=test_loader,
                metric_fn=lambda model, loader: {"accuracy": model.evaluate(loader)[1]}
            )
            recipe.job.to_clients(validator, tasks=["validate"])
            ```

        Example (Client API pattern - recommended):
            ```python
            # In client.py:
            while flare.is_running():
                input_model = flare.receive()
                # Load model weights...

                metrics = evaluate(model, test_loader)

                if flare.is_evaluate():  # CSE validation task
                    flare.send(flare.FLModel(metrics=metrics))
                    continue

                # Normal training...
            ```

        Args:
            model: TensorFlow Keras model to validate
            data_loader: Optional data loader for validation. If None, user must provide validation logic.
            metric_fn: Optional metric function that takes (model, data_loader) and returns dict of metrics.
                      If None, uses default accuracy evaluation.
        """
        super().__init__()

        self.logger = get_obj_logger(self)
        self.model = model
        self.data_loader = data_loader
        self.metric_fn = metric_fn
        self._validate_task_name = AppConstants.TASK_VALIDATION

    def execute(
        self,
        task_name: str,
        shareable: Shareable,
        fl_ctx: FLContext,
        abort_signal: Signal,
    ) -> Shareable:
        pass
