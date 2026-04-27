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

from typing import Optional, Tuple

from nvflare.app_common.abstract.params_converter import ParamsConverter
from nvflare.client.config import ExchangeFormat
from nvflare.fuel.utils.import_utils import optional_import


def _load_converter(module: str, name: str, format_name: str):
    pass


def create_default_params_converters(
    server_expected_format: str,
    params_exchange_format: str,
    train_task_name: str,
    eval_task_name: str,
    submit_model_task_name: str,
) -> Tuple[Optional[ParamsConverter], Optional[ParamsConverter]]:
    """Create default from/to NVFlare converters for common Client API formats."""
    pass
