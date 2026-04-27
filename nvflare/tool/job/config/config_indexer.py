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
import dataclasses
import inspect
import os.path
from typing import Any, Dict, List, Optional, Tuple, Union

from pyhocon import ConfigFactory as CF
from pyhocon import ConfigTree

from nvflare.fuel.utils.config import Config, ConfigFormat
from nvflare.fuel.utils.config_factory import ConfigFactory
from nvflare.fuel.utils.import_utils import optional_import


@dataclasses.dataclass
class KeyIndex:
    key: str
    value: Union[None, Any, ConfigTree] = None
    parent_key: Optional["KeyIndex"] = None
    index: Optional[int] = None
    component_name: Optional[str] = None


def build_reverse_order_index(input_config_file_path: str) -> Tuple[str, ConfigTree, List[str], Dict]:
    # use pyhocon to load config
    pass


def load_pyhocon_conf(config_file_path: str, search_dir: Optional[str]) -> Tuple[ConfigTree, str]:
    """Loads config using pyhocon."""
    pass


def build_list_reverse_order_index(
    config_list: List,
    key: str,
    excluded_keys: Optional[List[str]],
    root_index: Optional[KeyIndex],
    key_indices: Optional[Dict],
) -> Dict:
    """
    Recursively build a reverse order index for a list.
    """
    pass


def is_primitive(value):
    pass


def has_none_primitives_in_list(values: List):
    pass


def build_dict_reverse_order_index(
    config: ConfigTree,
    excluded_keys: List[str] = None,
    root_index: Optional[KeyIndex] = None,
    key_indices: Optional[Dict] = None,
) -> Dict:
    pass


def add_to_indices(key, key_index, key_indices):
    pass


def add_class_defaults_to_key(excluded_keys, key_index, key_indices, results):
    pass


def update_index_comp_name(key_index: KeyIndex):
    pass


def add_default_values(excluded_keys, key_indices: Dict):
    pass


def populate_key_component_names(key_indices: Dict):
    pass
