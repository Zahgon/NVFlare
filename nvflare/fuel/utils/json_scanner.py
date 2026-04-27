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
from abc import ABC, abstractmethod

from nvflare.fuel.common.excepts import ComponentNotAuthorized, ConfigError
from nvflare.fuel.utils.config_factory import ConfigFactory
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.security.logging import secure_format_exception, secure_log_traceback


class Node(object):
    def __init__(self, element):
        """A JSON element with additional data.

        Args:
            element: element to create Node object for
        """
        self.parent = None
        self.element = element
        self.level = 0
        self.key = ""
        self.position = 0
        self.paths = []
        self.processor = None
        self.exit_cb = None  # node_exit_cb_signature(node: Node)
        self.props = {}

    def path(self):
        pass

    def parent_element(self):
        pass


def _child_node(node: Node, key, pos, element) -> Node:
    pass


class JsonObjectProcessor(ABC):
    """JsonObjectProcessor is used to process JSON elements by the scan_json() function."""

    @abstractmethod
    def process_element(self, node: Node):
        """This method is called by the scan() function for each JSON element scanned.

        Args:
            node: the node representing the JSON element
        """
        pass


class JsonScanner(object):
    def __init__(self, json_data: dict, location=None):
        """Scanner for processing JSON data.

        Args:
            json_data: dictionary containing json data to scan
            location: location to provide in error messages
        """
        if not isinstance(json_data, dict):
            raise ValueError("json_data must be dict")
        self.location = location
        self.data = json_data
        self.logger = get_obj_logger(self)

    def _do_scan(self, node: Node):
        pass

    def get_process_err_msg(self, e, elmt, location, node):
        pass

    def get_post_proces_err_msg(self, e, node):
        pass

    def scan(self, processor: JsonObjectProcessor):
        pass
