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
import os
import pathlib
import shutil
import sys
import tempfile
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from pyhocon import ConfigFactory as CF
from pyhocon import ConfigTree, HOCONConverter

from nvflare.fuel.utils.config import ConfigFormat
from nvflare.fuel_opt.utils.pyhocon_loader import PyhoconConfig
from nvflare.tool.job.job_client_const import CONFIG_CONF, JOB_TEMPLATES

CONFIG_VERSION = "version"
CURRENT_CONFIG_VERSION = 2
TARGET_POC = "poc"
TARGET_PROD = "prod"


def get_home_dir() -> Path:
    pass


def get_package_root() -> Path:
    """
    Get the nvflare package root folder, e.g.
        /usr/local/python/3.10/lib/python3.10/site-packages/nvflare
    """
    pass


def get_hidden_nvflare_config_path(hidden_nvflare_dir: str) -> str:
    """
    Get the path for the hidden nvflare configuration file.
    Args:
        hidden_nvflare_dir: ~/.nvflare directory
    Returns:
        str: The path to the hidden nvflare configuration file.
    """
    pass


def get_or_create_hidden_nvflare_dir():
    pass


def get_hidden_nvflare_dir() -> pathlib.Path:
    pass


def load_config(config_file_path) -> Optional[ConfigTree]:
    pass


def _get_optional_config_value(nvflare_config: Optional[ConfigTree], *keys: str):
    pass


def _config_to_plain_dict(nvflare_config: Optional[ConfigTree]) -> dict:
    pass


def _has_legacy_config_keys(nvflare_config: Optional[ConfigTree]) -> bool:
    pass


def migrate_config_to_v2(nvflare_config: Optional[ConfigTree]) -> ConfigTree:
    pass


def find_startup_kit_location(target: Optional[str] = None) -> str:
    pass


def load_hidden_config_state() -> Tuple[str, Optional[ConfigTree], bool]:
    pass


def persist_hidden_config_migration(hidden_nvflare_config_file: str, migrated_config: ConfigTree):
    pass


def ensure_hidden_config_migrated():
    pass


def backup_hidden_config_file(hidden_nvflare_config_file: str) -> Optional[str]:
    pass


def print_hidden_config_migration_notice(hidden_nvflare_config_file: str, backup_path: Optional[str]):
    pass


def load_hidden_config() -> ConfigTree:
    pass


def create_startup_kit_config(
    nvflare_config: ConfigTree,
    target: str,
    startup_kit_dir: Optional[str] = None,
) -> ConfigTree:
    """
    Args:
        startup_kit_dir: specified startup kit location
        nvflare_config (ConfigTree): The existing nvflare configuration.

    Returns:
        ConfigTree: The merged configuration tree.
    """
    pass


def create_poc_workspace_config(nvflare_config: ConfigTree, poc_workspace_dir: Optional[str] = None) -> ConfigTree:
    """
    Args:
        poc_workspace_dir: specified poc_workspace_dir
        nvflare_config (ConfigTree): The existing nvflare configuration.

    Returns:
        ConfigTree: The merged configuration tree.
    """
    pass


def create_job_template_config(nvflare_config: ConfigTree, job_templates_dir: Optional[str] = None) -> ConfigTree:
    """
    Args:
        job_templates_dir: specified job template directory
        nvflare_config (ConfigTree): The existing nvflare configuration.

    Returns:
        ConfigTree: The merged configuration tree.
    """
    pass


def check_dir(dir_path: str):
    pass


def get_startup_kit_dir(startup_kit_dir: Optional[str] = None) -> str:
    # Compatibility wrapper for legacy callers: no explicit target means "use the POC kit".
    pass


def get_startup_kit_dir_for_target(startup_kit_dir: Optional[str] = None, target: Optional[str] = None) -> str:
    pass


def check_startup_dir(startup_kit_dir):
    pass


def find_job_templates_location(job_templates_dir: Optional[str] = None):
    def check_job_templates_dir(job_temp_dir: str):
        pass
    pass


def get_curr_dir():
    pass


def is_dir_empty(path: str):
    pass


def hocon_to_string(target_fmt: ConfigFormat, dst_config: ConfigTree):
    pass


def save_configs(app_configs: Dict[str, Tuple], keep_origin_format: bool = True):
    pass


def save_config(dst_config: ConfigTree, dst_path, keep_origin_format: bool = True):
    pass


def get_hidden_config() -> (str, ConfigTree):
    pass


def print_hidden_config(dst_path: str, dst_config: ConfigTree):
    pass


def find_in_list(arr: List, item) -> bool:
    pass


def append_if_not_in_list(arr: List, item) -> List:
    pass
