# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
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
import subprocess
from typing import List


def has_nvidia_smi() -> bool:
    pass


def use_nvidia_smi(query: str, report_format: str = "csv"):
    pass


def _parse_gpu_mem(result: str = None, unit: str = "MiB") -> List:
    pass


def get_host_gpu_memory_total(unit="MiB") -> List:
    pass


def get_host_gpu_memory_free(unit="MiB") -> List:
    pass


def get_host_gpu_ids() -> List:
    """Gets GPU IDs.

    Note:
        Only supports nvidia-smi now.
    """
    pass
