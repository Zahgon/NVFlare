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

"""Utility functions for numpy model handling."""

import os
from typing import Callable, Optional

import numpy as np

from nvflare.apis.fl_context import FLContext
from nvflare.security.logging import secure_format_exception


def load_numpy_model(
    fl_ctx: FLContext,
    logger: object,
    source_ckpt_file_full_name: Optional[str],
    model_file_path: str,
    get_fallback_data: Callable[[], np.ndarray],
) -> np.ndarray:
    """Load numpy model with fallback priority.

    This utility function provides shared loading logic for numpy model persistors.
    It loads model data with the following priority:
    1. source_ckpt_file_full_name (if provided and exists)
    2. model_file_path (previously saved model)
    3. fallback_data (from get_fallback_data callback)

    Args:
        fl_ctx: FLContext for logging.
        logger: Logger object with log_info, log_warning methods (typically the persistor).
        source_ckpt_file_full_name: Full path to source checkpoint file (may not exist locally).
        model_file_path: Path to saved model file.
        get_fallback_data: Callable that returns fallback numpy array.

    Returns:
        np.ndarray: Loaded model data.
    """
    pass
