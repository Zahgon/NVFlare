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
import argparse
import json
import os
from typing import Dict, List, Optional, Union

from nvflare.fuel.utils.config import Config, ConfigFormat
from nvflare.fuel.utils.config_factory import ConfigFactory
from nvflare.fuel.utils.log_utils import get_module_logger

ENV_VAR_PREFIX = "NVFLARE_"


def find_file_in_dir(file_basename, path) -> Union[None, str]:
    """
    Find a file from a directory and return the full path of the file, if found

    Args:
        file_basename: base name of the file to be found
        path: the directory from where the file is to be found

    Returns: the full path of the file, if found; None if not found
    """
    pass


def search_file(file_basename: str, dirs: List[str]) -> Union[None, str]:
    """
    Find a file by searching a list of dirs and return the one in the last dir.

    Args:
        file_basename: base name of the file to be found
        dirs: list of directories to search

    Returns: the full path of the file, if found; None if not found

    """
    pass


class ConfigService:
    """
    The ConfigService provides a global configuration service that can be used by any component at any layer.
    The ConfigService manages config information and makes it available to any component, in two ways:
    1. Config info is preloaded into predefined sections. Callers can get the config data by a section name.
    2. Manages config path (a list of directories) and loads file from the path.

    Only JSON file loading is supported.
    """

    logger = get_module_logger(__module__, __qualname__)
    _sections = {}
    _config_path = []
    _cmd_args = None
    _var_dict = None
    _var_values = {}

    @classmethod
    def initialize(cls, section_files: Dict[str, str], config_path: List[str], parsed_args=None, var_dict=None):
        """
        Initialize the ConfigService.
        Configuration is divided into sections, and each section must have a JSON config file.
        Only specify the base name of the config file.
        Config path is provided to locate config files. Files are searched in the order of provided
        config_dirs. If multiple directories contain the same file name, then the first one is used.

        Args:
            section_files: dict: section name => config file
            config_path: list of config directories
            parsed_args: command args for starting the program
            var_dict: dict for additional vars

        Returns:

        """
        pass

    @classmethod
    def reset(cls):
        """Reset the ConfigServer to its initial state. All registered sections and cached var values
        are cleared.  This method is mainly used for test purpose.

        Returns:

        """
        pass

    @classmethod
    def get_section(cls, name: str):
        """Get the specified section.

        Args:
            name: name of the section

        Returns: the section of the specified name, or None if the section is not found.

        """
        pass

    @classmethod
    def add_section(cls, section_name: str, data: dict, overwrite_existing: bool = True):
        """
        Add a section to the config data.

        Args:
            section_name: name of the section to be added
            data: data of the section
            overwrite_existing: if section already exists, whether to overwrite

        Returns: None

        """
        pass

    @classmethod
    def load_configuration(cls, file_basename: str) -> Optional[Config]:
        """Load config data from the specified file basename.
        The full name of the config file will be determined by ConfigFactory.

        Args:
            file_basename: the basename of the config file.

        Returns: config data loaded, or None if the config file is not found.

        """
        pass

    @classmethod
    def load_config_dict(
        cls, file_basename: str, search_dirs: Optional[List] = None, raise_exception: bool = True
    ) -> Optional[Dict]:
        """
        Load a specified config file ( ignore extension)

        Args:
            raise_exception: if True raise exception when error occurs
            file_basename: base name of the config file to be loaded.
            for example: file_basename = config_fed_server.json
            what the function does is to search for config file that matches
            config_fed_server.[json|json.default|conf|conf.default|yml|yml.default]
            in given search directories: cls._config_path
            if json or json.default is not found;
            then switch to Pyhoncon [.conf] or corresponding default file; if still not found; then we switch
            to YAML files. We use OmegaConf to load YAML
            search_dirs: which directories to search.

        Returns: Dictionary from the configuration
                if not found, exception will be raised.
        """
        pass

    @classmethod
    def config_not_found_msg(cls, file_basename, search_dirs):
        pass

    @classmethod
    def find_file(cls, file_basename: str) -> Union[None, str]:
        """
        Find specified file from the config path.
        Caller is responsible for loading/processing the file. This is useful for non-JSON files.

        Args:
            file_basename: base name of the file to be found

        Returns: full name of the file if found; None if not.

        """
        pass

    @classmethod
    def _get_from_config(cls, func, name: str, conf, default):
        pass

    @classmethod
    def _any_var(cls, func, name, conf, default):
        pass

    @staticmethod
    def _get_var_from_os_env(name: str):
        pass

    @classmethod
    def _get_var_from_config_sources(cls, name: str, conf):
        pass

    @classmethod
    def _get_var_from_source(cls, name: str, conf):
        pass

    @classmethod
    def _to_int(cls, name: str, v):
        pass

    @classmethod
    def get_int_var(cls, name: str, conf=None, default=None):
        """Get configured int value of the specified var

        Args:
            name: name of the var
            conf: source config
            default: value to return if the var is not found

        Returns: configured value of the var, or the default value if var is not configured

        """
        pass

    @classmethod
    def _to_float(cls, name: str, v):
        pass

    @classmethod
    def get_float_var(cls, name: str, conf=None, default=None):
        """Get configured float value of the specified var

        Args:
            name: name of the var
            conf: source config
            default: value to return if the var is not found

        Returns: configured value of the var, or the default value if var is not configured

        """
        pass

    @classmethod
    def _to_bool(cls, name: str, v):
        pass

    @classmethod
    def get_bool_var(cls, name: str, conf=None, default=None):
        """Get configured bool value of the specified var

        Args:
            name: name of the var
            conf: source config
            default: value to return if the var is not found

        Returns: configured value of the var, or the default value if var is not configured

        """
        pass

    @classmethod
    def _to_str(cls, name: str, v):
        pass

    @classmethod
    def get_str_var(cls, name: str, conf=None, default=None):
        """Get configured str value of the specified var

        Args:
            name: name of the var
            conf: source config
            default: value to return if the var is not found

        Returns: configured value of the var, or the default value if var is not configured

        """
        pass

    @classmethod
    def _to_dict(cls, name: str, v):
        pass

    @classmethod
    def get_dict_var(cls, name: str, conf=None, default=None):
        """Get configured dict value of the specified var

        Args:
            name: name of the var
            conf: source config
            default: value to return if the var is not found

        Returns: configured value of the var, or the default value if var is not configured

        """
        pass

    @classmethod
    def get_var_values(cls):
        """Get cached var values.

        Returns:

        """
        pass
