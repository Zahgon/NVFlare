# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
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
import inspect
from typing import Callable


def find_task_fn(task_fn_path) -> Callable:
    """Return function given a function path.

    Args:
        task_fn_path (str): function path

    Returns:
        function

    ex: train.main -> main
        custom/train.main -> main
        custom.train.main -> main
    """
    pass


def require_arguments(func):
    """Inspect function to get required arguments.

    Args:
        func: function

    Returns:
        require_args (bool), args_size (int), args_default_size (int)
    """
    pass
