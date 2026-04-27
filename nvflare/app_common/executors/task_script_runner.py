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
import builtins
import os
import runpy
import sys
import traceback

from nvflare.client.in_process.api import TOPIC_ABORT
from nvflare.fuel.data_event.data_bus import DataBus
from nvflare.fuel.data_event.event_manager import EventManager
from nvflare.fuel.utils.log_utils import get_module_logger

print_fn = builtins.print


class TaskScriptRunner:
    logger = get_module_logger(__module__, __qualname__)

    def __init__(self, custom_dir: str, script_path: str, script_args: str = None, redirect_print_to_log=True):
        """Wrapper for function given function path and args

        Args:
            custom_dir (str): site name
            script_path (str): script file name, such as train.py
            script_args (str, Optional): script arguments to pass in.
        """

        self.redirect_print_to_log = redirect_print_to_log
        self.event_manager = EventManager(DataBus())
        self.script_args = script_args
        self.custom_dir = custom_dir
        self.script_path = script_path
        self.script_full_path = self.get_script_full_path(self.custom_dir, self.script_path)

    def run(self):
        """Call the task_fn with any required arguments."""
        pass

    def get_sys_argv(self):
        pass

    def get_script_full_path(self, custom_dir, script_path) -> str:
        pass


def log_print(*args, logger=TaskScriptRunner.logger, **kwargs):
    # Create a message from print arguments
    pass
