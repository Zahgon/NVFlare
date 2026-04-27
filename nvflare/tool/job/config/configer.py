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
from typing import Any, Dict, List, Optional, Tuple

from pyhocon import ConfigFactory, ConfigTree

from nvflare.fuel.utils.config import ConfigFormat
from nvflare.lighter.tool_consts import NVFLARE_PREFIX
from nvflare.tool.job.config.config_indexer import KeyIndex, build_reverse_order_index
from nvflare.tool.job.job_client_const import (
    APP_CONFIG_DIR,
    APP_CONFIG_FILE_BASE_NAMES,
    APP_CONFIG_KEY,
    APP_SCRIPT_KEY,
    CONFIG_FED_CLIENT_CONF,
    DEFAULT_APP_NAME,
    JOB_META_BASE_NAME,
    META_APP_NAME,
)


def merge_configs_from_cli(cmd_args, app_names: List[str]) -> Tuple[Dict[str, Dict[str, tuple]], bool]:
    pass


def extract_string_with_index(input_string):
    """
    Extract the string before '[', the index within '[', and the string after ']'.

    Args:
        input_string (str): The input string containing the pattern '[index]'.

    Returns:
        list: A list of tuples containing the extracted components: (string_before, index, string_after).

    """
    pass


def filter_indices(app_indices_configs: Dict[str, Dict[str, Tuple]]) -> Dict[str, Dict[str, Dict[str, KeyIndex]]]:
    pass


def filter_config_name_and_values(
    excluded_key_list: List[str], key_indices: Dict[str, List[KeyIndex]]
) -> Dict[str, KeyIndex]:
    pass


def _cast_type(key_index, cli_value):
    """Casts cli_value to correct type.

    Since build_reverse_order_index is using pyhocon, we need to do the same here.
    """
    pass


def split_array_key(key: str) -> Tuple:
    pass


def convert_to_number(value: str):
    pass


def get_last_token(input_string):
    pass


def handle_key_in_path_notation_or_new_key(file: str, key: str, cli_value: str, config: ConfigTree, key_indices: Dict):

    pass


def merge_configs(
    app_indices_configs: Dict[str, Dict[str, tuple]], app_cli_file_configs: Dict[str, Dict[str, Dict]]
) -> Dict[str, Dict[str, tuple]]:
    """Merges configurations from indices_configs and cli_file_configs.

    Args:
        app_indices_configs (Dict[str, Dict[str, tuple]]): A dictionary containing indices and configurations.
        app_cli_file_configs (Dict[str, Dict[str, Dict]]): A dictionary containing CLI configurations.

    Returns:
        Dict[str, Dict[str, Tuple]]: A dictionary of {app_name: merged configurations}.
            Each of the merged configurations can be expressed in a Tuple: config, excluded_key_List, key_indices
    """
    pass


def get_root_index(key_index: KeyIndex) -> Optional[KeyIndex]:
    pass


def get_cli_config(cmd_args: Any, app_names: List[str]) -> Dict[str, Dict[str, Dict[str, str]]]:
    """Extracts configurations from command-line arguments and return them in a dictionary.

    Args:
        app_names: application names
        cmd_args: Command-line arguments containing configuration data.

    Returns:
        A dictionary containing the configurations extracted from the command-line arguments.
    """
    pass


def _is_meta_file(filename: str) -> bool:
    pass


def _parse_cli_config(
    job_folder: str, cli_configs: List[str], app_names: List[str]
) -> Dict[str, Dict[str, Dict[str, str]]]:
    """Extracts configurations from command-line arguments and return them in a dictionary.

    Args:
        job_folder: job_folder directory
        app_names: application names
        cli_configs: Array of CLI config option in the format of
           -f filename.conf  key1=v1 key2=v2
           where <app_name>/config is omitted, default to app/config
           or
           -f <app_name>/filename.conf  key1=v1 key2=v2
           where config is omitted, default to <app_name>/config/filename.conf
           or
           -f <app_name>/config/filename.conf  key1=v1 key2=v2
           or
           -f <app_name>/custom/filename.conf  key1=v1 key2=v2

           if filename.conf  is meta.conf, the <app_name> = __meta_app__

        separated by space
    Returns:
        A dictionary containing the configurations extracted from the command-line arguments.
    """
    pass


def get_config_file_path(app_name, input_file_path, job_folder):
    pass


def build_config_file_indices(job_folder: str, app_names: List[str]) -> Dict[str, Dict[str, Tuple]]:
    pass


def get_app_name_from_path(path: str):
    # path is in the format of the following:
    # path xxx.conf
    # path app1/xxx.conf
    # path app1/config/xxx.conf
    # path app1/custom/xxx.conf
    pass
