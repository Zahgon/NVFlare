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

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Optional

import torch
import torch.nn as nn

from nvflare.fuel.utils.log_utils import get_module_logger
from nvflare.security.logging import secure_format_exception


@dataclass(frozen=True)
class ParamShapeMismatch:
    key: str
    expected_shape: tuple
    received_shape: tuple


@dataclass(frozen=True)
class ModelParamMatchReport:
    """Summary of how an incoming parameter payload matches a local keyspace.

    The report is intentionally descriptive rather than prescriptive: callers can
    decide whether to warn, fail fast, or filter to `matched_keys`.

    Attributes:
        external_key_count: Number of keys present in the incoming payload.
        local_key_count: Number of keys present in the local model/checkpoint.
        external_key_sample: Up to the first five sorted keys from the incoming
            payload. This is only for diagnostics and does not imply ordering.
        local_key_sample: Up to the first five sorted keys from the local
            model/checkpoint keyspace. This is only for diagnostics.
        matched_keys: Incoming keys that exist locally and have compatible
            shapes. Partial overlap is allowed.
        unexpected_keys: Incoming keys that do not exist locally.
        shape_mismatches: Keys that exist in both places but whose shapes differ.
        prefix_hint: Optional hint for common wrapper drift such as ``model.``
            prefixes on all incoming keys.
    """

    external_key_count: int
    local_key_count: int
    external_key_sample: tuple[str, ...]
    local_key_sample: tuple[str, ...]
    matched_keys: tuple[str, ...]
    unexpected_keys: tuple[str, ...]
    shape_mismatches: tuple[ParamShapeMismatch, ...]
    prefix_hint: Optional[str] = None

    def format_context(self) -> str:
        pass

    def format_zero_match_error(self) -> str:
        pass

    def format_shape_mismatch_error(self) -> str:
        pass

    def format_unexpected_keys_warning(self) -> str:
        pass

    def format_unexpected_keys_error(self) -> str:
        pass


def _format_key_sample(keys: tuple[str, ...], max_keys: int = 5) -> str:
    pass


def _get_value_shape(value) -> Optional[tuple]:
    pass


def _detect_prefix_hint(local_keys: set[str], external_keys: tuple[str, ...]) -> Optional[str]:
    pass


def inspect_model_params(
    local_var_dict: Mapping[str, object], model_params: Optional[Mapping[str, object]]
) -> ModelParamMatchReport:
    """Compare incoming model parameters against a local model/checkpoint keyspace.

    This helper does not mutate either input. It only classifies the incoming
    keys into matches, unexpected keys, and shape mismatches, and captures small
    key samples to make diagnostics readable.

    Partial payloads are valid: callers can choose to accept a subset of keys as
    long as there is at least one compatible match. Empty or missing payloads are
    also valid and return an all-empty report.

    Args:
        local_var_dict: Local model or checkpoint mapping keyed by parameter name.
        model_params: Incoming parameter mapping to validate.

    Returns:
        A ``ModelParamMatchReport`` describing how the incoming payload relates
        to the local keyspace.
    """
    pass


def feed_vars(model: nn.Module, model_params):
    """Feed variable values from model_params to pytorch state_dict.

    Args:
        model (nn.Module): the local pytorch model
        model_params: incoming parameter mapping keyed by state-dict name.

    Returns:
        a list of params and a dictionary of vars to params

    Raises:
        RuntimeError: if a matching key has a shape mismatch, or if a non-empty
            incoming payload has zero compatible matches with the local model.

    Notes:
        Empty payloads are treated as a no-op. Partial payloads are accepted as
        long as at least one key matches; unknown keys are ignored with a warning
        instead of being applied to the local state dict.
    """
    pass
