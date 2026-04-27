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

from __future__ import absolute_import

import argparse
import os
import pathlib
import shutil
import sys
from typing import Optional

from nvflare.apis.utils.format_check import name_check
from nvflare.lighter.constants import CtxKey, ParticipantType, PropKey
from nvflare.lighter.entity import participant_from_dict
from nvflare.lighter.prov_utils import prepare_builders, prepare_packager
from nvflare.lighter.provisioner import Provisioner
from nvflare.lighter.spec import Project
from nvflare.lighter.tree_prov import hierachical_provision
from nvflare.lighter.utils import load_yaml

adding_client_error_msg = """
name: $SITE-NAME
org: $ORGANIZATION_NAME
components:
    resource_manager:    # This id is reserved by system.  Do not change it.
        path: nvflare.app_common.resource_managers.gpu_resource_manager.GPUResourceManager
        args:
            num_of_gpus: 4,
            mem_per_gpu_in_GiB: 16
    resource_consumer:    # This id is reserved by system.  Do not change it.
        path: nvflare.app_common.resource_consumers.gpu_resource_consumer.GPUResourceConsumer
        args:
"""

adding_user_error_msg = """
name: $USER_EMAIL_ADDRESS
org: $ORGANIZATION_NAME
role: $ROLE
"""


_provision_parser = None


def _normalize_and_validate_studies(project_dict: dict, participant_defs: list, api_version: int) -> dict:
    pass


def _project_generation_result(workspace: str, project_yml: str):
    pass


def define_provision_parser(parser):
    pass


def copy_project(project: str, dest: str):
    pass


def handle_provision(args):
    pass


def gen_default_project_config(src_project_name, dest_project_file):
    pass


def _normalize_project_name(project_dict):
    pass


def provision_for_edge(params, project_dict):
    pass


def provision(
    args,
    project_dict: dict,
    project_full_path: str,
    workspace_full_path: str,
    add_user_full_path: Optional[str] = None,
    add_client_full_path: Optional[str] = None,
):
    pass


def prepare_project(project_dict, add_user_file_path=None, add_client_file_path=None):
    pass


def add_extra_clients(add_client_file_path, participant_defs):
    pass


def add_extra_users(add_user_file_path, participant_defs):
    pass


def main():
    pass


if __name__ == "__main__":
    main()
