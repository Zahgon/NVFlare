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

import re

from nvflare.apis.filter import Filter, FilterChainType, FilterContextKey, FilterSource
from nvflare.apis.fl_constant import FilterKey
from nvflare.fuel.utils.json_scanner import Node
from nvflare.private.json_configer import ConfigContext, ConfigError, JsonConfigurator


class FilterChain(object):
    def __init__(self, chain_type, direction):
        """To init the FilterChain."""
        self.chain_type = chain_type
        self.tasks = []
        self.filters = []
        self.direction = direction

    @classmethod
    def validate_direction(cls, direction):
        pass


class FedJsonConfigurator(JsonConfigurator):
    def __init__(
        self,
        config_file_name: str,
        base_pkgs: [str],
        module_names: [str],
        exclude_libs=True,
        is_server=True,
        sys_vars=None,
    ):
        """To init the FedJsonConfigurator.

        Args:
            config_file_name: config filename
            base_pkgs: base packages need to be scanned
            module_names: module names need to be scanned
            exclude_libs: True/False to exclude the libs folder
        """
        JsonConfigurator.__init__(
            self,
            config_file_name=config_file_name,
            base_pkgs=base_pkgs,
            module_names=module_names,
            exclude_libs=exclude_libs,
            sys_vars=sys_vars,
        )

        self.format_version = None
        self.handlers = []
        self.components = {}  # id => component
        self.task_data_filter_chains = []
        self.task_result_filter_chains = []
        self.current_filter_chain = None
        self.data_filter_table = None
        self.result_filter_table = None
        self.is_server = is_server

    def process_config_element(self, config_ctx: ConfigContext, node: Node):
        pass

    def validate_tasks(self, tasks):
        pass

    def validate_filter_chain(self, chain: FilterChain):
        pass

    def _process_result_filter_chain(self, node: Node):
        pass

    def _process_data_filter_chain(self, node: Node):
        pass

    def finalize_config(self, config_ctx: ConfigContext):
        pass

    def _build_filter_table(self, c, data_filter_table):
        pass
