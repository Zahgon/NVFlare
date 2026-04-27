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
import json
import os
import re
from typing import List

from nvflare.fuel.common.excepts import ConfigError
from nvflare.security.logging import secure_format_exception

from .argument_utils import parse_vars
from .class_loader import load_class
from .class_utils import ModuleScanner, get_class_path_from_config, instantiate_class
from .dict_utils import extract_first_level_primitive, merge_dict
from .json_scanner import JsonObjectProcessor, JsonScanner, Node


class ConfigContext(object):
    def __init__(self):
        """Object containing configuration context."""
        self.app_root = ""
        self.vars = None
        self.config_json = None
        self.pass_num = 0


class _EnvUpdater(JsonObjectProcessor):
    def __init__(self, vs, element_filter=None):
        JsonObjectProcessor.__init__(self)
        if element_filter is not None and not callable(element_filter):
            raise ValueError("element_filter must be a callable function but got {}.".format(type(element_filter)))
        self.vars = copy.copy(vs)

        # make all os env vars available for config
        env_vars = dict(os.environ)
        if env_vars:
            for k, v in env_vars.items():
                # when referencing os env var, must use a $ sign prefix!
                var_name = "$" + k
                if var_name not in self.vars:
                    # only use env var when it is not locally defined!
                    self.vars[var_name] = v

        self.element_filter = element_filter
        self.num_updated = 0

    def process_element(self, node: Node):
        pass

    def substitute(self, element: str):
        pass


def resolve_var_refs(scanner: JsonScanner, var_values: dict):
    """Resolve var references in the config contained in the scanner

    Args:
        scanner: the scanner that contains config data to be resolved
        var_values: the dict that contains var values.

    Returns: None

    """
    pass


class Configurator(JsonObjectProcessor):
    def __init__(
        self,
        app_root: str,
        cmd_vars: dict,
        env_config: dict,
        wf_config_file_name: str,
        base_pkgs: List[str],
        module_names: List[str],
        exclude_libs=True,
        default_vars=None,
        num_passes=1,
        element_filter=None,
        var_processor=None,
    ):
        """Base class of Configurator to parse JSON configuration.

        Args:
            app_root: app root
            cmd_vars: command vars
            env_config: environment configuration
            wf_config_file_name: config file name
            base_pkgs: base packages
            module_names: module names
            exclude_libs: whether to exclude libs
            default_vars: default vars
            num_passes: number of passes
            element_filter: element filter
            var_processor: variable processor
        """
        JsonObjectProcessor.__init__(self)

        assert isinstance(app_root, str), "app_root must be str but got {}.".format(type(app_root))

        assert isinstance(num_passes, int), "num_passes must be int but got {}.".format(type(num_passes))
        assert num_passes > 0, "num_passes must > 0"

        if cmd_vars:
            assert isinstance(cmd_vars, dict), "cmd_vars must be dict but got {}.".format(type(cmd_vars))

        if env_config:
            assert isinstance(env_config, dict), "env_config must be dict but got {}.".format(type(env_config))

        assert isinstance(wf_config_file_name, str), "wf_config_file_name must be str but got {}.".format(
            type(wf_config_file_name)
        )
        assert os.path.isfile(wf_config_file_name), "wf_config_file_name {} is not a valid file".format(
            wf_config_file_name
        )
        assert os.path.exists(wf_config_file_name), "wf_config_file_name {} does not exist".format(wf_config_file_name)

        if default_vars is not None:
            assert isinstance(default_vars, dict), "default_vars must be dict but got {}.".format(type(default_vars))
        else:
            default_vars = {}

        self.cmd_vars = cmd_vars
        self.default_vars = default_vars
        self.app_root = app_root
        self.env_config = env_config
        self.wf_config_file_name = wf_config_file_name
        self.num_passes = num_passes
        self.element_filter = element_filter

        self.module_scanner = ModuleScanner(base_pkgs, module_names, exclude_libs)
        self.all_vars = None
        self.vars_from_cmd = None
        self.vars_from_env_config = None
        self.vars_from_wf_config = None
        self.config_ctx = None
        self.var_processor = var_processor

        with open(wf_config_file_name) as file:
            self.wf_config_data = json.load(file)

        self.json_scanner = JsonScanner(self.wf_config_data, wf_config_file_name)

    def _do_configure(self):
        pass

    def configure(self):
        pass

    def process_element(self, node: Node):
        pass

    def process_args(self, args: dict):
        pass

    def build_component(self, config_dict):
        pass

    def get_class_path(self, config_dict):
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
    """Get component reference.

    Args:
        component: string for component

    Returns: list of component and reference

    """
    pass
