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

import copy
import importlib
import os
from typing import Any, Dict, List, Optional

from nvflare.apis.analytix import ANALYTIC_EVENT_TYPE
from nvflare.fuel.utils.import_utils import optional_import
from nvflare.job_config.api import FedJob
from nvflare.recipe.spec import Recipe

TRACKING_REGISTRY = {
    "mlflow": {
        "package": "mlflow",
        "receiver_module": "nvflare.app_opt.tracking.mlflow.mlflow_receiver",
        "receiver_class": "MLflowReceiver",
    },
    "tensorboard": {
        "package": "tensorboard",
        "receiver_module": "nvflare.app_opt.tracking.tb.tb_receiver",
        "receiver_class": "TBAnalyticsReceiver",
    },
    "wandb": {
        "package": "wandb",
        "receiver_module": "nvflare.app_opt.tracking.wandb.wandb_receiver",
        "receiver_class": "WandBReceiver",
    },
}

MODEL_LOCATOR_REGISTRY = {
    "pytorch": {
        "locator_module": "nvflare.app_opt.pt.file_model_locator",
        "locator_class": "PTFileModelLocator",
        "persistor_param": "pt_persistor_id",
    },
    "numpy": {
        "locator_module": "nvflare.app_common.np.np_model_locator",
        "locator_class": "NPModelLocator",
        "persistor_param": None,  # NPModelLocator doesn't use persistor_id
    },
    "tensorflow": {
        "locator_module": "nvflare.app_opt.tf.file_model_locator",
        "locator_class": "TFFileModelLocator",
        "persistor_param": "tf_persistor_id",
    },
}


def _has_cross_site_eval_workflow(job: FedJob) -> bool:
    """Check if CrossSiteModelEval workflow is already configured on server."""
    pass


def add_experiment_tracking(
    recipe: Recipe,
    tracking_type: str,
    tracking_config: Optional[dict] = None,
    client_side: bool = False,
    server_side: bool = True,
):
    """Add experiment tracking to a recipe.

    Adds tracking receivers to the server and/or clients to collect and log metrics during training.

    Args:
        recipe: Recipe instance to augment with experiment tracking.
        tracking_type: Type of tracking to enable ("mlflow", "tensorboard", or "wandb").
        tracking_config: Optional configuration dict for the tracking receiver.
        client_side: If True, add tracking to all clients (each client tracks locally).
        server_side: If True, add tracking to server (aggregates metrics from all clients). Default: True.

    Examples:
        # Server-side tracking (default - federated metrics)
        add_experiment_tracking(recipe, "mlflow", {"tracking_uri": "..."})

        # Client-side tracking only (each client tracks independently)
        add_experiment_tracking(recipe, "mlflow", {...}, client_side=True, server_side=False)

        # Both server and client tracking
        add_experiment_tracking(recipe, "mlflow", {...}, client_side=True, server_side=True)
    """
    pass


def add_cross_site_evaluation(
    recipe: Recipe,
    submit_model_timeout: int = 600,
    validation_timeout: int = 6000,
):
    """Add cross-site evaluation to an existing recipe.

    This utility automatically configures cross-site evaluation by:
    - Auto-detecting the framework from the recipe
    - Adding the appropriate model locator
    - Adding the CrossSiteModelEval controller
    - Adding ValidationJsonGenerator for results
    - Auto-adding the appropriate validator to clients (for NumPy recipes)

    **For standalone CSE without training**, use `NumpyCrossSiteEvalRecipe` instead.

    **Note**: This utility is designed for adding CSE to training recipes. If you call it on
    a CSE-only recipe (e.g., `NumpyCrossSiteEvalRecipe`), it will detect this and skip
    adding duplicate validators automatically.

    **WARNING**: Do not call this function multiple times on the same recipe instance.
    This function is idempotent and will raise a RuntimeError if called more than once
    on the same recipe to prevent duplicate component registration.

    **IMPORTANT for PyTorch**: Your client training script must handle validation tasks by
    checking `flare.is_evaluate()` and returning metrics without training. Example pattern:

        ```python
        # In your client script:
        while flare.is_running():
            input_model = flare.receive()
            model.load_state_dict(input_model.params)

            # Evaluate model (always required)
            metrics = evaluate(model, test_loader)

            # Handle CSE validation task
            if flare.is_evaluate():
                output_model = flare.FLModel(metrics=metrics)
                flare.send(output_model)
                continue  # Skip training for validation-only tasks

            # Normal training code here...
        ```

    Example (NumPy - fully automatic):
        ```python
        from nvflare.app_common.np.recipes import NumpyFedAvgRecipe
        from nvflare.recipe.utils import add_cross_site_evaluation

        recipe = NumpyFedAvgRecipe(
            name="my-job", model=[1.0, 2.0, 3.0], min_clients=2, num_rounds=3, train_script="client.py"
        )

        # That's it! Framework auto-detected, validator auto-added
        add_cross_site_evaluation(recipe)
        ```

    Example (PyTorch - requires client script support):
        ```python
        from nvflare.app_opt.pt.recipes import FedAvgRecipe
        from nvflare.recipe.utils import add_cross_site_evaluation

        recipe = FedAvgRecipe(
            name="my-job", min_clients=2, num_rounds=3,
            model=MyModel(), train_script="client.py"
        )

        # Note: client.py must handle flare.is_evaluate() for validation
        add_cross_site_evaluation(recipe)
        ```

    Example (TensorFlow - Client API pattern, recommended):
        ```python
        from nvflare.app_opt.tf.recipes import FedAvgRecipe
        from nvflare.recipe.utils import add_cross_site_evaluation

        recipe = FedAvgRecipe(
            name="my-job", min_clients=2, num_rounds=3,
            model=MyTFModel(), train_script="client.py"
        )

        # Note: client.py must handle flare.is_evaluate() for validation
        add_cross_site_evaluation(recipe)
        ```

    Example (TensorFlow - Component-based alternative):
        ```python
        from nvflare.app_opt.tf.recipes import FedAvgRecipe
        from nvflare.app_opt.tf.tf_validator import TFValidator
        from nvflare.recipe.utils import add_cross_site_evaluation

        recipe = FedAvgRecipe(
            name="my-job", min_clients=2, num_rounds=3,
            model=MyTFModel(), train_script="client.py"
        )

        add_cross_site_evaluation(recipe)

        # Optional: manually add TFValidator for component-based validation
        validator = TFValidator(model=my_model, data_loader=test_loader)
        recipe.job.to_clients(validator, tasks=["validate"])
        ```

    Args:
        recipe: Recipe instance to augment with cross-site evaluation.
        submit_model_timeout: Timeout (seconds) for submitting models to clients. Defaults to 600.
        validation_timeout: Timeout (seconds) for validation tasks on clients. Defaults to 6000.

    Raises:
        ValueError: If the recipe doesn't have a framework attribute or uses an unsupported framework.
        RuntimeError: If cross-site evaluation has already been added to this recipe.

    Note:
        - Currently supports PyTorch, NumPy, and TensorFlow frameworks.
        - **NumPy recipes using `NumpyFedAvgRecipe`**: Validators (NPValidator) are automatically
          added to clients to handle validation tasks. The function intelligently detects if validators
          are already configured by checking for executors handling TASK_VALIDATION, avoiding duplicates
          for CSE-only recipes (like `NumpyCrossSiteEvalRecipe`).
        - **Unified `FedAvgRecipe` with `framework=FrameworkType.NUMPY`**: Uses the same Client API
          validation pattern as PyTorch and TensorFlow. Your client script should handle
          `flare.is_evaluate()` and return metrics for validation tasks.
        - **PyTorch recipes**: No separate validator component is needed. The client training script
          handles validation tasks through the Client API's `flare.is_evaluate()` check. See the
          hello-pt example for implementation pattern.
        - **TensorFlow recipes**: Similar to PyTorch, uses the Client API pattern. The client script
          should handle validation tasks via `flare.is_evaluate()` check.
    """
    pass


def _has_task_executor(job, task_name: str) -> bool:
    """Check if any executor is already configured for the specified task.

    This function inspects the job's internal structure to determine if a validator
    or executor is already handling the specified task. It uses defensive programming
    to handle potential variations in the internal API structure.

    IMPORTANT: This function accesses the private attribute job._deploy_map because:
    1. No public API exists in FedJob to query configured executors
    2. This check is necessary to avoid adding duplicate validators for CSE
    3. Without this, we'd rely on fragile string matching on recipe class names

    The implementation uses defensive programming (hasattr checks, try-except) to
    minimize fragility. If FedJob's internal structure changes, this function will
    gracefully return False rather than crashing.

    Future improvement: FedJob could provide a public method like get_executors(target)
    to make this check safer and more maintainable.

    Args:
        job: FedJob instance to check
        task_name: Task name to check for (e.g., AppConstants.TASK_VALIDATION)

    Returns:
        True if an executor is already configured for this task, False otherwise
    """
    pass


def collect_non_local_scripts(job: FedJob) -> List[str]:
    """Collect scripts that don't exist locally.

    This utility function is used by ExecEnv subclasses to validate script resources
    before deployment. Scripts are considered "non-local" if they are absolute paths
    that don't exist on the local machine.

    Args:
        job: The FedJob to check for non-local scripts.

    Returns:
        List of absolute script paths that don't exist on the local machine.
    """
    pass


def ensure_config_type_dict(config: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Ensure a component config dict has config_type 'dict' and is normalized for the config layer.

    Used by FedOpt-style recipes for optimizer_args and lr_scheduler_args: those dicts have 'path' or
    'class_path' plus 'args', and would otherwise be treated as component configs and instantiated
    during config scan (e.g. torch.optim.SGD without params). This function:
    - Accepts either 'path' or 'class_path' (for consistency with recipe model_config); if only
      'class_path' is set, copies it to 'path' so the component builder and runtime code work unchanged.
    - Sets config_type to 'dict' when missing so the component builder does not instantiate at load time;
      the optimizer/scheduler is instantiated at runtime when params/optimizer are available.

    Args:
        config: A component-style config dict (e.g. {'class_path': 'torch.optim.SGD', 'args': {'lr': 1.0}}
                or {'path': '...', 'args': {...}}) or None.

    Returns:
        A copy of config with config_type 'dict' if missing and path set from class_path if needed; None if config is None.
    """
    pass


def validate_ckpt(ckpt: Optional[str]) -> None:
    """Validate a checkpoint path if provided.

    For absolute paths: no local existence check (file may be a server-side path).
    For relative paths: verifies the file exists locally (it will be bundled into the job).

    Args:
        ckpt: Checkpoint file path to validate (e.g. initial_ckpt or eval_ckpt).

    Raises:
        ValueError: If relative path does not exist locally.
    """
    pass


def prepare_initial_ckpt(initial_ckpt: Optional[str], job) -> Optional[str]:
    """Prepare initial_ckpt for job deployment.

    - Relative path: treated as a local file. The file is bundled into the server
      app's custom directory and the basename is returned for runtime resolution.
    - Absolute path: treated as a server-side (remote) path and returned as-is.
      The file is expected to exist on the server at runtime.

    Args:
        initial_ckpt: Checkpoint file path (absolute or relative).
        job: BaseFedJob instance to add the file to.

    Returns:
        The checkpoint path to pass to the persistor:
        - None if initial_ckpt is None
        - Basename for relative paths (file is bundled into app/custom/)
        - Absolute path as-is for server-side checkpoints
    """
    pass


def extract_persistor_id(result: Any) -> str:
    pass


def resolve_initial_ckpt(initial_ckpt: Optional[str], prepared_initial_ckpt: Optional[str], job) -> Optional[str]:
    pass


def setup_custom_persistor(*, job, model_persistor=None) -> str:
    pass


def validate_dict_model_config(model: Any) -> None:
    """Validate recipe dict model config structure.

    Recipes accept model config with ``class_path`` (fully qualified class name).
    The job/config layer uses ``path``; recipes use ``class_path`` only.

    Args:
        model: Model input to validate.

    Raises:
        ValueError: If dict config is missing 'class_path' or value is not a string.
    """
    pass


def recipe_model_to_job_model(recipe_model: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and convert recipe model dict (class_path) to job/config format (path).

    Calls :func:`validate_dict_model_config` internally so callers do not need to
    validate separately. Recipes accept {"class_path": "module.Class", "args": {...}} only.
    The Job API and config parsing expect {"path": "module.Class", "args": {...}}.

    Args:
        recipe_model: Dict with 'class_path' and optional 'args'.

    Returns:
        Dict with 'path' and 'args' for use by PTModel, persistors, etc.
    """
    pass
