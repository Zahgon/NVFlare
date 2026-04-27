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
import importlib
import inspect
import pkgutil
from typing import Callable, Dict, List, Optional

from nvflare.apis.fl_component import FLComponent
from nvflare.fuel.common.excepts import ConfigError
from nvflare.fuel.utils.class_loader import load_class
from nvflare.fuel.utils.components_utils import create_classes_table_static
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.security.logging import secure_format_exception

DEPRECATED_PACKAGES = ["nvflare.app_common.pt", "nvflare.app_common.homomorphic_encryption"]


def instantiate_class(class_path, init_params):
    """Method for creating an instance for the class.

    Args:
        class_path: full path of the class
        init_params: A dictionary that contains the name of the transform and constructor input
        arguments. The transform name will be appended to `medical.common.transforms` to make a
        full name of the transform to be built.
    """
    pass


def get_class_path_from_config(
    config_dict: dict,
    resolve_name: Optional[Callable[[str], Optional[str]]] = None,
) -> str:
    """Resolve a component config dict to a fully qualified class path.

    Config key precedence: path → class_path → name. The first key present
    is used; the others are ignored. Key presence is used, not truthiness:
    e.g. path="" or path=None is still "path present", so path is validated
    and raises ConfigError instead of falling through to class_path or name.
    When only "name" is present, resolve_name(class_name) is called to get
    the module name.

    Args:
        config_dict: Config with "path", "class_path", or "name" (see precedence above).
        resolve_name: Callable that takes a class name and returns module name or None.
            Required when config uses "name".

    Returns:
        Fully qualified class path string.

    Raises:
        ConfigError: Invalid or missing path/class_path/name.
    """
    pass


class ModuleScanner:
    def __init__(self, base_pkgs: List[str], module_names: List[str], exclude_libs=True):
        """Loads specified modules from base packages and then constructs a class to module name mapping.

        Args:
            base_pkgs: base packages to look for modules in
            module_names: module names to load
            exclude_libs: excludes modules containing .libs if True. Defaults to True.
        """
        self.base_pkgs = base_pkgs
        self.module_names = module_names
        self.exclude_libs = exclude_libs

        self._logger = get_obj_logger(self)
        self._class_table = create_classes_table_static()

    def create_classes_table(self):
        pass

    def get_module_name(self, class_name) -> Optional[str]:
        """Gets the name of the module that contains this class.

        Args:
            class_name: The name of the class

        Returns:
            The module name if found.
        """
        pass


def _retrieve_parameters(class__, parameters):
    pass


def get_component_init_parameters(component):
    """To retrieve the initialize parameters of an object from the class constructor.

    Args:
        component: a class instance

    Returns:

    """
    pass
