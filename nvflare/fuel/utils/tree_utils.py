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
from typing import Any, List

from nvflare.fuel.common.fqn import FQN


def _build_path(obj: Any, path: list, get_name_f, get_parent_f, **kwargs):
    pass


def build_path(obj: Any, get_name_f, get_parent_f, **kwargs):
    """Build tree path for the specified object, which can be of any type.
    It is assumed that the object is already in an object tree. The tree path of an object is the list of objects
    that are traversed from the root to the object.

    Objects must have unique names.

    Args:
        obj: the object that the path will be built for
        get_name_f: the function that returns object name
        get_parent_f: the function that returns the object's parent object
        **kwargs: kwargs to be passed to the get_name_f and get_parent_f

    Returns: a tuple of (error, path).

    """
    pass


class Node:
    """Definition of Nodes that are elements of trees.
    The "self.obj" is the object associated with the node;
    The "self.parent" is the parent Node;
    The "self.children" is a list of child Nodes.
    """

    def __init__(self, obj: Any, parent):
        """Constructor of Node

        Args:
            obj: the object to be associated with the node
            parent: parent node of the node
        """
        self.obj = obj
        self.parent = parent  # a Node
        self.children = []  # child nodes


class Forest:
    """A forest contains one or more trees.
    Each entry in "self.roots" is the unique name of the root object.
    The "self.nodes" a dict of: name => Node. You can get the Node from an object name.
    """

    def __init__(self):
        """Constructor of Forest"""
        self.roots = []  # one or more names of the root nodes
        self.nodes = {}  # name => Node


def build_forest(objs: List[Any], get_name_f, get_fqn_f, **kwargs) -> Forest:
    """Builds a Forest from a list of objects.
    Each object must have a unique "name" and unique "fqn".
    This function builds trees based on the FQNs of the objects.

    Args:
        objs: objects for which to build the forest
        get_name_f: the function to get object name
        get_fqn_f: the function to get object fqn
        **kwargs: kwargs to be passed to get_name_f and get_fqn_f

    Returns: a Forest object

    """
    pass


def _dump_one(node: Node, get_name_f, **kwargs):
    pass


def forest_to_dict(forest: Forest, get_name_f, **kwargs) -> dict:
    """Output the forest into a dict that shows the structure of the forest.

    Args:
        forest: the forest to output
        get_name_f: function to get object name
        **kwargs: kwargs passed to get_name_f

    Returns: a dict that shows the structure of the forest

    """
    pass
