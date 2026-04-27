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

import inspect
import re
from functools import wraps

type_pattern_mapping = {
    "server": r"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$",
    "host_name": r"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$",
    "overseer": r"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$",
    "sp_end_point": r"^((([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9]):[0-9]*:[0-9]*)$",
    "client": r"^[A-Za-z0-9-_]+$",
    "job_name": r"^[A-Za-z0-9][A-Za-z0-9._-]*$",
    "relay": r"^[A-Za-z0-9-_]+$",
    "admin": r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$",
    "email": r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$",
    "org": r"^[A-Za-z0-9_]+$",
    "simple_name": r"^[A-Za-z0-9_]+$",
    "study": r"^[a-z0-9](?:[a-z0-9_-]{0,61}[a-z0-9])?$",
    "site": r"^[A-Za-z0-9-_]+$",
}


def name_check(name: str, entity_type: str):
    pass


def validate_class_methods_args(cls):
    pass


def validate_args(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        pass
    pass
