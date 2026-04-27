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
from nvflare.fuel.utils.class_utils import instantiate_class


def instantiate_from_config(obj_config: dict):
    """Create an object based on path and args info in the specified object config.

    Args:
        obj_config: config that contains class path and args for the object to be created

    Returns: created object

    """
    pass


def prepare_builders(project_dict: dict):
    """Create provision builders based on project info.

    Args:
        project_dict: the project info

    Returns: list of builder objects

    """
    pass


def prepare_packager(project_dict: dict):
    """Create provision packager object based on project info.

    Args:
        project_dict: project info.

    Returns: a packager object if specified in the project info.

    """
    pass
