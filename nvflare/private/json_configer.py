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
import copy
from typing import List, Union

from nvflare.fuel.common.excepts import ComponentNotAuthorized, ConfigError
from nvflare.fuel.utils.class_loader import load_class
from nvflare.fuel.utils.class_utils import ModuleScanner
from nvflare.fuel.utils.component_builder import ComponentBuilder
from nvflare.fuel.utils.config_factory import ConfigFactory
from nvflare.fuel.utils.config_service import ConfigService
from nvflare.fuel.utils.dict_utils import augment
from nvflare.fuel.utils.json_scanner import JsonObjectProcessor, JsonScanner, Node
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.fuel.utils.wfconf import resolve_var_refs
from nvflare.security.logging import secure_format_exception


class ConfigContext(object):
    def __init__(self):
        """To init thee ConfigContext."""
        self.config_json = None
        self.pass_num = 0


class JsonConfigurator(JsonObjectProcessor, ComponentBuilder):
    def __init__(
        self,
        config_file_name: Union[str, List[str]],
        base_pkgs: List[str],
        module_names: List[str],
        exclude_libs=True,
        num_passes=1,
        sys_vars=None,
    ):
        """To init the JsonConfigurator.

        Args:
            config_file_name: config filename or list of JSON config file names
            base_pkgs: base packages need to be scanned
            module_names: module names need to be scanned
            exclude_libs: True/False to exclude the libs folder
            num_passes: number of passes to parsing the config
            sys_vars: system vars
        """
        JsonObjectProcessor.__init__(self)
        self.logger = get_obj_logger(self)

        if not isinstance(num_passes, int):
            raise TypeError(f"num_passes must be int but got {num_passes}")
        if not num_passes > 0:
            raise ValueError(f"num_passes must > 0 but got {num_passes}")

        if isinstance(config_file_name, str):
            config_files = [config_file_name]
        elif isinstance(config_file_name, list):
            config_files = config_file_name
        else:
            raise TypeError(f"config_file_names must be str or list of strs but got {type(config_file_name)}")

        for f in config_files:
            if not ConfigFactory.has_config(f):
                raise FileNotFoundError(f"config_file_names {f} does not exist or not a file")

        self.config_file_names = config_files
        self.num_passes = num_passes
        self.sys_vars = sys_vars
        self.module_scanner = ModuleScanner(base_pkgs, module_names, exclude_libs)
        self.config_ctx = None

        config_data = {}
        for f in config_files:
            data = ConfigService.load_config_dict(f)
            try:
                augment(to_dict=config_data, from_dict=data, from_override_to=False)
            except Exception as e:
                raise RuntimeError("Error processing config file {}: {}".format(f, secure_format_exception(e)))

        self.config_data = config_data
        self.json_scanner = JsonScanner(config_data, config_files)
        self.build_auth_func = None
        self.build_auth_kwargs = None

    def set_component_build_authorizer(self, func, **kwargs):
        pass

    def authorize_and_build_component(self, config_dict, config_ctx: ConfigContext, node: Node):
        pass

    def get_module_scanner(self):
        pass

    def _do_configure(self):
        pass

    def configure(self):
        pass

    def process_element(self, node: Node):
        pass

    def is_configured_subclass(self, config_dict, base_class):
        pass

    def start_config(self, config_ctx: ConfigContext):
        pass

    def process_config_element(self, config_ctx: ConfigContext, node: Node):
        pass

    def finalize_config(self, config_ctx: ConfigContext):
        pass


def get_component_refs(component):
    pass
