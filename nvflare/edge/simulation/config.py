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
import builtins
import importlib
import json
import os
import re
import sys
from typing import Any, Type

from nvflare.edge.simulation.device_task_processor import DeviceTaskProcessor
from nvflare.fuel.utils.validation_utils import check_positive_int, check_positive_number, check_str

VAR_PATTERN = re.compile(r"\{(.*?)}")


def load_class(class_path) -> Type:

    pass


class ConfigParser:
    def __init__(self, config_file: str):
        self.job_name = None
        self.get_job_timeout = None
        self.processor = None
        self.endpoint = None
        self.num_devices = 100
        self.num_workers = 10
        self.processor_class = None
        self.processor_args = None
        self.parse(config_file)

    def get_processor(self, variables: dict = None) -> DeviceTaskProcessor:

        pass

    def get_endpoint(self):
        pass

    def get_num_devices(self):
        pass

    def get_num_workers(self):
        pass

    def get_job_name(self):
        pass

    def parse(self, config_file: str):
        pass

    def _variable_substitution(self, args: Any, variables: dict) -> Any:
        pass
