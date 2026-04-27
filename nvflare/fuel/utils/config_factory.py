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
from typing import List, Optional, Tuple

from nvflare.fuel.utils.config import Config, ConfigFormat, ConfigLoader
from nvflare.fuel.utils.import_utils import optional_import
from nvflare.fuel.utils.json_config_loader import JsonConfigLoader
from nvflare.fuel.utils.log_utils import get_module_logger


class ConfigFactory:
    logger = get_module_logger(__module__, __qualname__)

    OmegaConfLoader, omega_import_ok = optional_import(
        module="nvflare.fuel_opt.utils.omegaconf_loader", name="OmegaConfLoader"
    )
    PyhoconLoader, pyhocon_import_ok = optional_import(
        module="nvflare.fuel_opt.utils.pyhocon_loader", name="PyhoconLoader"
    )

    _fmt2Loader = {
        ConfigFormat.JSON: JsonConfigLoader(),
    }

    if omega_import_ok:
        _fmt2Loader.update({ConfigFormat.OMEGACONF: OmegaConfLoader()})

    if pyhocon_import_ok:
        _fmt2Loader.update({ConfigFormat.PYHOCON: PyhoconLoader()})

    @staticmethod
    def search_config_format(
        init_file_path: str, search_dirs: Optional[List[str]] = None, target_fmt: Optional[ConfigFormat] = None
    ) -> Tuple[Optional[ConfigFormat], Optional[str]]:
        """Finds the configuration format and the location (file_path) for given initial init_file_path and search directories.

        For example, the initial config file path given is `config_client.json`
        the search function will ignore the .json extension and search "config_client.xxx" in the given directory in
        specified extension search order. The first found file_path will be used as configuration.
        the ".xxx" is one of the extensions defined in the configuration format.

        Args:
            init_file_path: initial file_path for the configuration
            search_dirs: search directory. If none, the parent directory of init_file_path will be used as search dir
            target_fmt: (ConfigFormat) if specified, only this format searched, ignore all other formats.

        Returns:
            Tuple of None,None or ConfigFormat and real configuration file path

        """
        pass

    @staticmethod
    def get_file_basename(init_file_path):
        pass

    @staticmethod
    def load_config(
        file_path: str, search_dirs: Optional[List[str]] = None, target_fmt: Optional[ConfigFormat] = None
    ) -> Optional[Config]:
        """Finds the configuration for given initial init_file_path and search directories.

        For example, the initial config file path given is `config_client.json`
        the search function will ignore the .json extension and search "config_client.xxx" in the given directory in
        specified extension search order. The first found file_path will be used as configuration.
        the ".xxx" is one of the extensions defined in the configuration format.

        Args:
            file_path: initial file path
            search_dirs: search directory. If none, the parent directory of init_file_path will be used as search dir
            target_fmt: (ConfigFormat) if specified, only this format searched, ignore all other formats.

        Returns:
            None if not found, or Config

        """
        pass

    @staticmethod
    def get_config_loader(config_format: ConfigFormat) -> Optional[ConfigLoader]:
        """Returns ConfigLoader for given config_format

        Args:
            config_format: ConfigFormat

        Returns:
            the matching ConfigLoader for the given format

        """
        pass

    @staticmethod
    def match_config(parent, init_file_path, match_fn) -> bool:
        # we ignore the original extension
        pass

    @staticmethod
    def has_config(init_file_path: str, search_dirs: Optional[List[str]] = None) -> bool:
        pass
