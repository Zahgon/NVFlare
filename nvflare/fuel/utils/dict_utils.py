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

import collections

from .validation_utils import check_object_type


def update(d, u):
    pass


def update_configs_with_envs(configs, env):
    pass


def merge_dict(dict1, dict2):
    pass


def extract_first_level_primitive(d):
    pass


def augment(to_dict: dict, from_dict: dict, from_override_to=False, append_list="components") -> str:
    """Augments the to_dict with the content from the from_dict.

        - Items in from_dict but not in to_dict are added to the to_dict
        - Items in both from_dict and to_dict must be ether dicts or list of dicts,
          and augment will be done on these items recursively
        - Non-dict/list items in both from_dict and to_dict are considered conflicts.

    Args:
        to_dict: the dict to be augmented
        from_dict: content to augment the to_dict
        from_override_to: content in from_dict overrides content in to_dict when conflict happens
        append_list: str or list of str: item keys for list to be appended

    Returns:
        An error message if any; empty str if success.

    .. note::

       The content of the to_dict is updated

    """
    pass


def _update_component_dict(comp_list: list, target: dict) -> str:
    pass


def update_components(target_dict: dict, from_dict: dict) -> str:
    """update components in target_dict with components from the from_dict.
    If a component with the same ID exists in both target_dict and from_dict, the component in from_dict
    will replace the one in target_dict.
    If a component only exists in from_dict, it will be added to the component list of target_dict.
    Args:
        target_dict: the dict to be updated
        from_dict: the dict that will be used to update the target_dict
    Returns:
    """
    pass
