# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
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
import os.path
from abc import ABC
from typing import Dict, List

from nvflare.apis.filter import Filter
from nvflare.apis.fl_component import FLComponent


class BaseAppConfig(ABC):
    """BaseAppConfig holds the base essential component data for the ServerApp and ClientApp, including the
    task_data_filters, task_result_filters, system components and used external scripts.

    """

    def __init__(self) -> None:
        super().__init__()

        self.task_data_filters = []  # list of tuples: (task_set, list of filters)
        self.task_result_filters = []  # list of tuples: (task_set, list of filters)
        self.components: Dict[str, object] = {}
        self.ext_scripts = []
        self.ext_dirs = []
        self.file_sources = []
        self.handlers: [FLComponent] = []
        self.additional_params: Dict[str, any] = {}  # additional configuration parameters

    def add_component(self, cid: str, component):
        pass

    def add_task_data_filter(self, tasks: List[str], filter: Filter):
        pass

    def add_task_result_filter(self, tasks: List[str], filter: Filter):
        pass

    def add_ext_script(self, ext_script: str):
        pass

    def add_ext_dir(self, ext_dir: str):
        pass

    def add_params(self, args: Dict[str, any]):
        """Add additional system configuration parameters to be included in the generated JSON configs.

        Args:
            args: Dictionary of configuration parameters (e.g., {"timeout": 600, "max_retries": 3})
        """
        pass

    @staticmethod
    def _add_task_filter(tasks, filter, taskset_filters: list):
        """Add a filter for a set of tasks.

        Args:
            tasks: the tasks that the filter will be added to.
            filter: the filter to be added.
            taskset_filters: this is a list of tuples. Each tuple contains a taskset and a list of filters
                already added to the taskset.

        Returns: None

        We first check whether the "tasks" already matches an entry's taskset in taskset_filters.
        If so, then add the filter to the entry.

        Otherwise, we then check whether the "tasks" overlaps with any entry's taskset. If so, this is not allowed
        and an exception will be raised.

        If the "tasks" doesn't exist nor conflicts with any entry in taskset_filters, we add a new entry to
        taskset_filters.
        """
        pass

    def add_file_source(self, src_path: str, dest_dir=None, app_folder_type=None):
        pass
