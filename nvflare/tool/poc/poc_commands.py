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
import errno
import json
import os
import random
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, OrderedDict, Tuple

import yaml
from pyhocon import ConfigFactory as CF

from nvflare.cli_exception import CLIException
from nvflare.cli_unknown_cmd_exception import CLIUnknownCmdException
from nvflare.fuel.utils.config import ConfigFormat
from nvflare.fuel.utils.gpu_utils import get_host_gpu_ids
from nvflare.lighter.constants import PropKey, ProvisionMode
from nvflare.lighter.prov_utils import prepare_builders, prepare_packager
from nvflare.lighter.provision import gen_default_project_config, prepare_project
from nvflare.lighter.provisioner import Provisioner
from nvflare.lighter.utils import (
    load_yaml,
    update_project_server_name_config,
    update_server_default_host,
    update_storage_locations,
)
from nvflare.tool.api_utils import shutdown_system
from nvflare.tool.poc.service_constants import FlareServiceConstants as SC
from nvflare.utils.cli_utils import get_hidden_nvflare_config_path, get_or_create_hidden_nvflare_dir, hocon_to_string

DEFAULT_WORKSPACE = "/tmp/nvflare/poc"
DEFAULT_PROJECT_NAME = "example_project"

CMD_PREPARE_POC = "prepare"
CMD_PREPARE_JOBS_DIR = "prepare-jobs-dir"
CMD_START_POC = "start"
CMD_STOP_POC = "stop"
CMD_CLEAN_POC = "clean"


def client_gpu_assignments(clients: List[str], gpu_ids: List[int]) -> Dict[str, List[int]]:
    pass


def get_service_command(
    cmd_type: str, prod_dir: str, service_dir, service_config: Dict, study: Optional[str] = None
) -> str:
    pass


def get_stop_cmd(poc_workspace: str, service_dir_name: str):
    pass


def get_nvflare_home() -> Optional[str]:
    pass


def get_upload_dir(startup_dir) -> str:
    pass


def is_dir_empty(path: str):
    pass


def prepare_jobs_dir(cmd_args):
    pass


def _prepare_jobs_dir(
    jobs_dir: str, workspace: str, config_packages: Optional[Tuple] = None, force: bool = False
) -> bool:
    pass


def get_prod_dir(workspace, project_name: str = DEFAULT_PROJECT_NAME):
    pass


def gen_project_config_file(workspace: str) -> str:
    pass


def verify_host(host_name: str) -> bool:
    pass


def verify_hosts(project_config: OrderedDict):
    pass


def get_project_hosts(project_config) -> List[str]:
    pass


def get_fl_server_name(project_config: OrderedDict) -> str:
    pass


def get_fl_admins(project_config: OrderedDict, is_project_admin: bool):
    pass


def get_other_admins(project_config: OrderedDict):
    pass


def get_proj_admin(project_config: OrderedDict):
    pass


def get_fl_client_names(project_config: OrderedDict) -> List[str]:
    pass


def local_provision(
    clients: List[str],
    number_of_clients: int,
    workspace: str,
    docker_image: str,
    use_he: bool = False,
    project_conf_path: str = "",
) -> Tuple:
    pass


def get_service_config(project_config):
    pass


def save_project_config(project_config, project_file):
    pass


def update_server_name(project_config):
    pass


def is_docker_run(project_config: OrderedDict):
    pass


def update_static_file_builder(docker_image: str, project_config: OrderedDict):
    # need to keep the order of the builders
    pass


def add_docker_builder(use_docker: bool, project_config: OrderedDict):
    pass


def add_he_builder(use_he: bool, project_config: OrderedDict):
    pass


def update_clients(clients: List[str], n_clients: int, project_config: OrderedDict) -> OrderedDict:
    pass


def prepare_clients(clients, number_of_clients):
    pass


def save_startup_kit_dir_config(workspace, project_name):
    pass


def prepare_poc(cmd_args):
    pass


def _prepare_poc(
    clients: List[str],
    number_of_clients: int,
    workspace: str,
    docker_image: Optional[str] = None,
    use_he: bool = False,
    project_conf_path: str = "",
    examples_dir: Optional[str] = None,
    force: bool = False,
) -> bool:
    pass


def _get_running_poc_context(workspace: str):
    pass


def _ensure_poc_stopped(
    workspace: str, timeout_in_sec: int = 30, poll_interval: float = 1.0, project_config=None, service_config=None
):
    pass


def prepare_poc_provision(
    clients: List[str],
    number_of_clients: int,
    workspace: str,
    docker_image: str,
    use_he: bool = False,
    project_conf_path: str = "",
    examples_dir: Optional[str] = None,
) -> Dict:
    pass


def get_examples_dir(examples_dir):
    pass


def _sort_service_cmds(cmd_type, service_cmds: list, service_config) -> list:
    def sort_first(val):
        pass
    pass


def get_cmd_path(poc_workspace, service_name, cmd):
    pass


def is_poc_ready(poc_workspace: str, service_config, project_config):
    # check server and admin directories exist
    pass


def validate_poc_workspace(poc_workspace: str, service_config, project_config=None):
    pass


def validate_gpu_ids(gpu_ids: list, host_gpu_ids: list):
    pass


def get_gpu_ids(user_input_gpu_ids, host_gpu_ids) -> List[int]:
    pass


def start_poc(cmd_args):
    pass


def get_gpis(cmd_args):
    pass


def get_excluded(cmd_args):
    pass


def get_service_list(cmd_args):
    pass


def _get_server_url(project_config, service_config) -> str:
    pass


def _start_poc(poc_workspace: str, gpu_ids: List[int], excluded=None, services_list=None, study: Optional[str] = None):
    pass


def validate_services(project_config, services_list: List, excluded: List):
    pass


def validate_participants(participant_names, list_participants):
    pass


def setup_service_config(poc_workspace) -> Tuple:
    pass


def stop_poc(cmd_args):
    pass


def _stop_poc(poc_workspace: str, excluded=None, services_list=None, project_config=None, service_config=None):
    pass


def _get_clients(service_commands: list, service_config) -> List[str]:
    pass


def _build_commands(
    cmd_type: str,
    poc_workspace: str,
    service_config,
    project_config,
    excluded: list,
    services_list=None,
    study: Optional[str] = None,
) -> list:
    """Builds commands.

    Args:
        cmd_type (str): start/stop
        poc_workspace (str): poc workspace directory path
        service_config (_type_): service_config
        excluded (list): excluded service/participants name
        services_list (_type_, optional): Service names. If empty, include every service/participants

    Returns:
        list: built commands
    """
    def is_fl_service_dir(p_dir_name: str):
        pass
    pass


def prepare_env(service_name, gpu_ids: Optional[List[int]], service_config: Dict):
    pass


def async_process(service_name, cmd_path, gpu_ids: Optional[List[int]], service_config: Dict):
    pass


def sync_process(service_name, cmd_path):
    pass


def _run_poc(
    cmd_type: str,
    poc_workspace: str,
    gpu_ids: List[int],
    service_config: Dict,
    project_config: Dict,
    excluded: list,
    services_list=None,
    study: Optional[str] = None,
):
    pass


def clean_poc(cmd_args):
    pass


def is_poc_running(poc_workspace, service_config, project_config):
    pass


def _is_live_pid_file(pid_file: str) -> bool:
    pass


def _clean_poc(poc_workspace: str):
    pass


poc_sub_cmd_handlers = {
    CMD_PREPARE_POC: prepare_poc,
    CMD_PREPARE_JOBS_DIR: prepare_jobs_dir,
    CMD_START_POC: start_poc,
    CMD_STOP_POC: stop_poc,
    CMD_CLEAN_POC: clean_poc,
}

# Populated by define_*_parser functions; used by handlers for --schema support
_poc_sub_cmd_parsers = {}
_poc_root_parser = None


def def_poc_parser(sub_cmd):
    pass


def define_prepare_parser(poc_parser, cmd: Optional[str] = None, help_str: Optional[str] = None):
    pass


def define_prepare_jobs_parser(poc_parser):
    pass


def define_clean_parser(poc_parser):
    pass


def define_start_parser(poc_parser):
    pass


def define_stop_parser(poc_parser):
    pass


def get_local_host_gpu_ids():
    pass


def handle_poc_cmd(cmd_args):
    pass


def get_poc_workspace():
    pass
