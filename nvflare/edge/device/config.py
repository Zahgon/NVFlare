# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
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
import inspect
from typing import Any, List


class ConfigError(Exception):
    pass


class ConfigKey:
    NAME = "name"
    TYPE = "type"
    ARGS = "args"
    TRAINER = "trainer"
    EXECUTORS = "executors"
    COMPONENTS = "components"
    IN_FILTERS = "in_filters"
    OUT_FILTERS = "out_filters"
    HANDLERS = "handlers"


class TrainConfig:

    def __init__(self, objects: dict, in_filters, out_filters, event_handlers, executors: dict):
        self.objects = objects
        self.in_filters = in_filters
        self.out_filters = out_filters
        self.event_handlers = event_handlers
        self.executors = executors

    def find_executor(self, task_name: str):
        pass


class ComponentResolver:
    """A ComponentResolver resolves component spec into a device-native object."""

    def __init__(self, comp_type, name, args, obj_class=None):
        self.comp_type = comp_type
        self.comp_name = name

        if not args:
            args = {}
        self.comp_args = args
        self.obj_class = obj_class

    def resolve(self) -> Any:
        """Resolve the component spec and create device-native object.

        Returns: a device-native object or None if failed.

        """
        pass


def _determine_value(item: Any, resolvers: dict) -> Any:
    """Determine value of the specified item: recursively replace component refs with the ComponentResolver objects
    of the referenced components.

    Args:
        item: the item whose value is to be determined
        resolvers: table of resolvers

    Returns:

    """
    pass


def _find_obj(item, obj_table):
    """Try to find the native object(s) for the item: recursively process all ComponentResolvers and replace them
     with their native objects following the structure of the item (list or dict).

    Args:
        item: the item to be processed
        obj_table: the object table that contains objects already created

    Returns: the item itself (with referenced components replaced with objects);
        or in case that the item is a ComponentResolver, the native object created by it

    """
    pass


def _try_to_resolve(resolver: ComponentResolver, obj_table: dict) -> Any:
    """Try to create device-native object. If created, place the obj in the obj_table.

    Args:
        resolver: the ComponentResolver that will try to resolve its component
        obj_table: object table that keeps objects of resolved components

    Returns: the resolved object, or None if the resolver is not ready

    For the resolver to be ready, all of its args must be resolved already, meaning that if an arg
    references another component, the referenced component must be resolved.

    """
    pass


def _process_components(component_config: dict, resolver_registry: dict):
    # Step 1: create a ComponentResolver for each component spec in the config
    pass


def _resolve_ref(ref, obj_table: dict):
    pass


def _process_refs(refs: List[str], obj_table: dict):
    pass


def process_train_config(config: dict, resolver_registry: dict) -> TrainConfig:
    pass
