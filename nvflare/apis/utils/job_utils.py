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

import io
import json
import os
from typing import Optional
from zipfile import ZipFile

from nvflare.apis.fl_constant import JobConstants
from nvflare.apis.job_def import ALL_SITES, JobMetaKey
from nvflare.fuel.utils.config import ConfigFormat
from nvflare.fuel.utils.config_factory import ConfigFactory
from nvflare.fuel.utils.zip_utils import normpath_for_zip, zip_directory_to_bytes


def _get_default_meta(job_folder_name: str) -> str:
    # A format string for the dummy meta.json
    pass


def convert_legacy_zipped_app_to_job(zip_data: bytes) -> bytes:
    """Convert a legacy app in zip into job layout in memory.

    Args:
        zip_data: The input zip data

    Returns:
        The converted zip data
    """
    pass


def load_job_def_bytes(from_path: str, def_name: str) -> bytes:
    """Load a job definition from specified path and return zipped bytes

    Args:
        from_path: path where the job definition is located
        def_name: name of the job

    Returns:

    """
    pass
