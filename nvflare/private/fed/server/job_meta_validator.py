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

import collections
import logging
from io import BytesIO
from typing import Optional, Set, Tuple
from zipfile import ZipFile

from nvflare.apis.app_validation import AppValidationKey
from nvflare.apis.fl_constant import JobConstants
from nvflare.apis.job_def import ALL_SITES, SERVER_SITE_NAME, JobMetaKey
from nvflare.apis.job_meta_validator_spec import JobMetaValidatorSpec
from nvflare.fuel.utils.config import ConfigFormat
from nvflare.fuel.utils.config_factory import ConfigFactory
from nvflare.private.fed.utils.fed_utils import extract_participants
from nvflare.security.logging import secure_format_exception

CONFIG_FOLDER = "/config/"
CUSTOM_FOLDER = "/custom/"

MAX_CLIENTS = 1000000

logger = logging.getLogger(__name__)


class JobMetaValidator(JobMetaValidatorSpec):
    """Job validator"""

    def _validate_zf(self, job_name, zf):
        pass

    def validate(self, job_name: str, job_data: bytes) -> Tuple[bool, str, dict]:
        """Validate job

        Args:
            job_name (str): Job name
            job_data (bytes): Job ZIP data

        Returns:
            Tuple[bool, str, dict]: (is_valid, error_message, meta)
        """
        pass

    @staticmethod
    def _validate_meta(job_name: str, zf: ZipFile) -> Optional[dict]:
        pass

    @staticmethod
    def _validate_deploy_map(job_name: str, meta: dict) -> list:

        pass

    def _validate_app(self, job_name: str, meta: dict, zip_file: ZipFile) -> None:

        pass

    @staticmethod
    def _convert_value_to_int(v) -> int:
        pass

    def _validate_min_clients(self, job_name: str, meta: dict, clients: set) -> None:
        pass

    @staticmethod
    def _validate_mandatory_clients(job_name: str, meta: dict, clients: set) -> None:
        pass

    @staticmethod
    def _validate_resource(job_name: str, meta: dict) -> None:
        pass

    _VALID_LAUNCHER_MODES = {"process", "docker", "k8s"}

    @staticmethod
    def _validate_launcher_spec(job_name: str, meta: dict) -> None:
        pass

    @staticmethod
    def _get_all_clients(site_list: Optional[list]) -> Set[str]:

        pass

    @staticmethod
    def _entry_exists(zip_file: ZipFile, path: str) -> bool:
        pass

    @staticmethod
    def _config_exists(zip_file: ZipFile, zip_folder, init_config_path: str) -> bool:
        def match(parent: ZipFile, config_path: str):
            pass
        pass
