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

from typing import List, Union

from nvflare.apis.filter import Filter, FilterChainType, FilterContextKey, FilterSource
from nvflare.apis.fl_constant import FilterKey
from nvflare.private.fed_json_config import FilterChain


class Scope(object):
    TASK_DATA_FILTERS_NAME = "task_data_filters"
    TASK_RESULT_FILTERS_NAME = "task_result_filters"

    def __init__(self):
        self.name = ""
        self.props = {}
        self.task_data_filters = {FilterKey.IN: [], FilterKey.OUT: []}
        self.task_result_filters = {FilterKey.IN: [], FilterKey.OUT: []}

    def set_name(self, name: str):
        pass

    def set_props(self, props: dict):
        pass

    def add_task_data_filter(self, f: Filter, direction):
        pass

    def add_task_result_filter(self, f: Filter, direction):
        pass


class PrivacyManager(object):
    def __init__(
        self, scopes: Union[None, List[Scope]], default_scope_name: Union[None, str], components: Union[None, dict]
    ):
        self.name_to_scopes = {}
        self.default_scope = None
        self.components = components

        if scopes:
            for s in scopes:
                if s.name in self.name_to_scopes:
                    raise ValueError(f"duplicate scopes defined for name '{s.name}'")
                self.name_to_scopes[s.name] = s
            if default_scope_name:
                self.default_scope = self.name_to_scopes.get(default_scope_name)
                if not self.default_scope:
                    raise ValueError(f"specified default scope '{default_scope_name}' does not exist")
            self.policy_defined = True
        else:
            self.policy_defined = False

    def get_scope(self, name: Union[None, str]):
        pass

    def is_policy_defined(self):
        pass


class PrivacyService(object):
    manager = None

    @staticmethod
    def initialize(manager: PrivacyManager):
        pass

    @staticmethod
    def get_scope(name: Union[None, str]):
        pass

    @staticmethod
    def is_policy_defined():
        pass

    @staticmethod
    def is_scope_allowed(scope_name: str):
        """Check whether the specified scope is allowed

        Args:
            scope_name: scope to be checked

        Returns:

        """
        pass

    @staticmethod
    def get_manager():
        pass
