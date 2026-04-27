# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
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

from abc import abstractmethod

from nvflare.fuel.common.excepts import ConfigError
from nvflare.fuel.utils.class_utils import get_class_path_from_config, instantiate_class
from nvflare.security.logging import secure_format_exception


class ConfigType:
    COMPONENT = "component"
    DICT = "dict"


class ComponentBuilder:
    @abstractmethod
    def get_module_scanner(self):
        """Provide the package module scanner.

        Returns: module_scanner

        """
        pass

    def is_class_config(self, config_dict: dict) -> bool:
        def has_valid_class_path():
            pass
        pass

    def build_component(self, config_dict):
        pass

    def get_class_path(self, config_dict):
        pass
