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

from typing import Iterator, Optional, Union

import numpy as np
import torch

from nvflare.apis.dxo import DXO, DataKind, from_shareable
from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.job_def import SERVER_SITE_NAME
from nvflare.apis.shareable import Shareable

from .types import TensorTopics


def clean_task_data(fl_ctx: FLContext):
    """Clean the task data in the FLContext.

    Args:
        fl_ctx (FLContext): The FLContext to clean the task data from.
    """
    pass


def clean_task_result(fl_ctx: FLContext):
    """Clean the task result in the FLContext.

    Args:
        fl_ctx (FLContext): The FLContext to clean the task result from.
    """
    pass


def get_topic_for_ctx_prop_key(ctx_prop_key: str) -> str:
    """Get the topic based on the context property key.

    Args:
        ctx_prop_key (str): The context property key.

    Returns:
        str: The topic associated with the context property key.
    """
    pass


def get_targets_from_ctx_and_prop_key(fl_ctx: FLContext, ctx_prop_key: str) -> list[str]:
    """Get the peer identity name from the FLContext.

    Args:
        fl_ctx (FLContext): The FLContext for the current operation.
    Returns:
        list[str]: The identity name(s) of the peer(s).
    """
    pass


def to_numpy_recursive(obj: Union[torch.Tensor, dict[str, torch.Tensor]]) -> Union[dict[str, np.ndarray], np.ndarray]:
    """Recursively convert torch tensors to numpy arrays with minimal memory duplication.

    Note: For CPU tensors, .numpy() returns a view sharing memory with the original tensor (zero-copy).
    For GPU tensors, data must be moved to CPU first, which creates a copy.
    Only the dictionary structure is duplicated, not the underlying tensor data (for CPU tensors).

    Args:
        obj: A torch.Tensor or dict containing torch.Tensors (possibly nested)

    Returns:
        A numpy array or dict containing numpy arrays. Tensor data is shared where possible (CPU tensors).
    """
    pass


def get_dxo_from_ctx(fl_ctx: FLContext, ctx_prop_key: str, tasks: list[str]) -> DXO:
    """Extract model parameters from the FLContext based on the provided property key.

    Args:
        fl_ctx (FLContext): The FLContext containing the data.
        ctx_prop_key (str): The context property key to extract data from.
        tasks (list[str]): The list of tasks to consider.

    Returns:
        dict[str, torch.Tensor]: A dictionary of data extracted from the FLContext.
    """
    pass


def chunk_tensors_from_params(
    params: dict[str, Union[torch.Tensor, dict]],
    parent_keys: Optional[list[str]] = None,
    chunk_size: Optional[int] = 10,
) -> Iterator[tuple[tuple[str], dict[str, torch.Tensor]]]:
    """
    Generator that yields tensors grouped by their immediate parent dictionary keys.

    Args:
        params: Dictionary with string keys and values that are either torch.Tensor or nested dicts.
        parent_keys: List of keys representing the current path (internal use, defaults to empty).
        chunk_size: Optional maximum number of tensors to yield at once per parent.

    Yields:
        A tuple containing:
        - List of parent keys (excluding the tensor key itself).
        - Dictionary mapping tensor key names to torch.Tensor instances.
    """
    pass


def update_params_with_tensors(
    params: dict, parents: list[str], tensors: dict[str, torch.Tensor], to_ndarray: bool = False
) -> None:
    """
    Updates the nested dictionary `params` at the location specified by
    `parents` with the provided tensor values from `tensors`.

    If `to_ndarray` is True, tensors are converted to numpy ndarrays before insertion.

    Args:
        params: The dictionary to update (possibly nested).
        parents: List of keys that specify the nested path within `params`.
        tensors: Dictionary mapping keys to torch.Tensor instances.
        to_ndarray: Whether to convert tensors to numpy arrays before updating.
    """
    pass


def merge_params_dicts(
    base_params: dict[str, dict],
    new_params: dict[str, dict],
    to_ndarray: bool = False,
) -> dict[str, dict]:
    """
    Merges two nested dictionaries of parameters.

    Args:
        base_params: The base dictionary to merge into.
        new_params: The new dictionary whose values will overwrite those in base_params.
        to_ndarray: If True, converts torch tensors to numpy arrays during merge.

    Returns:
        The merged dictionary with values from new_params overwriting those in base_params.
    """
    pass


def copy_non_tensor_params(params: dict[str, dict]) -> dict[str, dict]:
    """Recursively copy non-tensor parameters in the given dictionary.

    Args:
        params: The dictionary of parameters to copy from.

    Returns:
        A new dictionary containing only non-tensor parameters.
    """
    pass
