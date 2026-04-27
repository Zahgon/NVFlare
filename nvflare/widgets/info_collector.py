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

import datetime

from nvflare.apis.analytix import AnalyticsData
from nvflare.apis.dxo import from_shareable
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable

from .widget import Widget


class GroupInfoCollector(object):
    def __init__(self):
        """Records the information using a dict of dict.

        Note:
           Key is group name and value is the information dictionary.
        """
        self.info = {}

    def set_info(self, group_name: str, info: dict):
        pass

    def add_info(self, group_name: str, info: dict):
        pass


class InfoCollector(Widget):
    CATEGORY_STATS = "stats"
    CATEGORY_ERROR = "error"

    EVENT_TYPE_GET_STATS = "info_collector.get_stats"
    CTX_KEY_STATS_COLLECTOR = "info_collector.stats_collector"

    def __init__(self):
        """A widget for information collection.

        Note:
           self.categories structure:
                category (dict)
                    group (dict)
                        key/value (dict)
        """
        super().__init__()
        self.categories = {}
        self.engine = None

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def get_run_stats(self) -> dict:
        """Gets status for this current run.

        Returns:
            A dictionary that contains the status for this run.
        """
        pass

    def add_info(self, category_name: str, group_name: str, key: str, value):
        """Adds information to the specified category / group.

        Args:
            category_name (str): The top level distinction is called category.
            group_name (str): One level down category is called group
            key (str): The key to be recorded inside the dict.
            value (str): The value to be recorded inside the dict.
        """
        pass

    def set_info(self, category_name: str, group_name: str, info: dict):
        """Sets information to the specified category / group.

        Args:
            category_name (str): The top level distinction is called category.
            group_name (str): One level down category is called group
            info (dict): The dict to be recorded.

        Note:
            This sets the entire dictionary vs add_info only add a key-value pair.
        """
        pass

    def get_category(self, category_name: str):
        """Gets the category dict.

        Args:
            category_name (str): The name of the category.

        Returns:
            A dictionary of specified category.
        """
        pass

    def get_group(self, category_name: str, group_name: str):
        """Gets the group dict.

        Args:
            category_name (str): The name of the category.
            group_name (str): The name of the group_name.

        Returns:
            A dictionary of specified category/group.
        """
        pass

    def reset_all(self):
        """Resets all information collected."""
        pass

    def reset_category(self, category_name: str):
        """Resets the specified category information collected.

        Args:
            category_name (str): The name of the category.
        """
        pass

    def reset_group(self, category_name: str, group_name: str):
        """Resets the specified category/group information collected.

        Args:
            category_name (str): The name of the category.
            group_name (str): The name of the group_name.
        """
        pass

    def add_error(self, group_name: str, key: str, err: str):
        """Adds error information to error category.

        Args:
            group_name (str): One level down category is called group
            key (str): The key to be recorded inside the dict.
            err (str): The error value to be put in.
        """
        pass

    def get_errors(self):
        """Gets the error category information."""
        pass

    def reset_errors(self):
        """Resets the error category information."""
        pass
