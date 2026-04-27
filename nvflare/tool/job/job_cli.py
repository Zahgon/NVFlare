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

import argparse
import datetime
import os
import shutil
import sys
import time
import traceback
from contextlib import contextmanager
from functools import partial
from tempfile import mkdtemp
from typing import List, Optional, Tuple

from pyhocon import ConfigFactory as CF
from pyhocon import ConfigTree

from nvflare.cli_unknown_cmd_exception import CLIUnknownCmdException
from nvflare.fuel.utils.config import ConfigFormat
from nvflare.fuel.utils.config_factory import ConfigFactory
from nvflare.tool.cli_session import new_cli_session
from nvflare.tool.job.config.configer import (
    build_config_file_indices,
    filter_indices,
    get_root_index,
    merge_configs_from_cli,
)
from nvflare.tool.job.job_client_const import (
    CONFIG_FED_CLIENT_CONF,
    CONFIG_FED_SERVER_CONF,
    CONFIG_FILE_BASE_NAME_WO_EXTS,
    DEFAULT_APP_NAME,
    JOB_CONFIG_COMP_NAME,
    JOB_CONFIG_FILE_NAME,
    JOB_CONFIG_VAR_NAME,
    JOB_CONFIG_VAR_VALUE,
    JOB_INFO_CONF,
    JOB_INFO_CONTROLLER_TYPE,
    JOB_INFO_CONTROLLER_TYPE_KEY,
    JOB_INFO_DESC,
    JOB_INFO_DESC_KEY,
    JOB_INFO_EXECUTION_API_TYPE,
    JOB_INFO_EXECUTION_API_TYPE_KEY,
    JOB_INFO_KEYS,
    JOB_INFO_MD,
    JOB_META_BASE_NAME,
    META_APP_NAME,
    TEMPLATES_KEY,
)
from nvflare.utils.cli_utils import (
    TARGET_POC,
    backup_hidden_config_file,
    create_job_template_config,
    find_job_templates_location,
    get_curr_dir,
    get_startup_kit_dir_for_target,
    load_hidden_config_state,
    print_hidden_config_migration_notice,
    save_config,
)

CMD_LIST_TEMPLATES = "list-templates"
CMD_SHOW_VARIABLES = "show-variables"
CMD_CREATE_JOB = "create"
CMD_SUBMIT_JOB = "submit"
CMD_JOB_LIST = "list"
CMD_JOB_META = "meta"
CMD_JOB_ABORT = "abort"
CMD_JOB_CLONE = "clone"
CMD_JOB_DOWNLOAD = "download"
CMD_JOB_DELETE = "delete"

# Job observability commands
CMD_JOB_STATS = "stats"
CMD_JOB_LOGS = "logs"

# Job lifecycle helpers
CMD_JOB_MONITOR = "monitor"
CMD_JOB_LOG_CONFIG = "log-config"
CMD_JOB_LOG_ALIAS = "log"

_JOB_HELP_FORMATTER = partial(argparse.HelpFormatter, max_help_position=24, width=120)


def find_filename_basename(f: str):
    pass


def build_job_template_indices(job_templates_dir: str) -> ConfigTree:
    pass


def get_template_info_config(template_dir):
    pass


def get_app_dirs_from_template(template_dir):
    pass


def get_app_dirs_from_job_folder(job_folder):
    pass


def create_job(cmd_args):
    pass


def get_src_template_by_name(cmd_args):
    pass


def get_src_template(cmd_args) -> Optional[str]:
    pass


def remove_pycache_files(custom_dir):
    pass


def remove_extra_files(config_dir):
    pass


def show_variables(cmd_args):
    pass


def check_template_exists(target_template_name, template_index_conf):
    pass


def display_template_variables(job_folder, app_variable_values):
    pass


def list_templates(cmd_args):
    pass


def update_job_templates_dir(job_templates_dir: str):
    pass


def display_available_templates(template_index_conf):
    pass


def fix_length_format(name: str, name_fix_length: int):
    pass


def submit_job(cmd_args):
    def _has_job_meta(path: str):
        pass
    def _has_server_config(path: str):
        pass
    def _resolve_job_folder(path: str):
        pass
    pass


def _resolve_admin_user_and_dir_from_startup_kit(startup_kit_dir: str) -> Tuple[str, str]:
    pass


def find_admin_user_and_dir(startup_kit_dir: Optional[str] = None, target: Optional[str] = None) -> Tuple[str, str]:
    pass


def internal_submit_job(admin_user_dir, username, temp_job_dir, cmd_args=None):
    pass


job_sub_cmd_handlers = {
    CMD_CREATE_JOB: create_job,
    CMD_SUBMIT_JOB: submit_job,
    CMD_LIST_TEMPLATES: list_templates,
    CMD_SHOW_VARIABLES: show_variables,
    CMD_JOB_LIST: None,
    CMD_JOB_META: None,
    CMD_JOB_ABORT: None,
    CMD_JOB_CLONE: None,
    CMD_JOB_DOWNLOAD: None,
    CMD_JOB_DELETE: None,
    CMD_JOB_STATS: None,
    CMD_JOB_LOGS: None,
    CMD_JOB_MONITOR: None,
    CMD_JOB_LOG_CONFIG: None,
}

job_sub_cmd_parser = {
    CMD_CREATE_JOB: None,
    CMD_SUBMIT_JOB: None,
    CMD_LIST_TEMPLATES: None,
    CMD_SHOW_VARIABLES: None,
    CMD_JOB_LIST: None,
    CMD_JOB_META: None,
    CMD_JOB_ABORT: None,
    CMD_JOB_CLONE: None,
    CMD_JOB_DOWNLOAD: None,
    CMD_JOB_DELETE: None,
    CMD_JOB_STATS: None,
    CMD_JOB_LOGS: None,
    CMD_JOB_MONITOR: None,
    CMD_JOB_LOG_CONFIG: None,
}


def handle_job_cli_cmd(cmd_args):
    pass


def def_job_cli_parser(sub_cmd):
    pass


def _add_job_connection_args(parser):
    pass


def define_submit_job_parser(job_subparser):
    pass


def define_list_templates_parser(job_subparser):
    pass


def define_variables_parser(job_subparser):
    pass


def define_create_job_parser(job_subparser):
    pass


def prepare_job_config(cmd_args, app_names: List[str], tmp_job_dir: Optional[str] = None):
    pass


def has_client_config_file(app_config_dir):
    pass


def save_merged_configs(app_merged_conf, job_folder, tmp_job_dir):
    pass


def prepare_meta_config(cmd_args, target_template_dir, app_names):
    pass


def load_default_config_template(config_file_name: str):
    pass


def dst_app_path(job_folder: str, app_name="app"):
    pass


def dst_config_path(job_folder, config_filename, app_name: str = "app"):
    pass


def get_config_dirs(job_folder: str, app_names: List[str]) -> List[str]:
    pass


def get_config_dir(job_folder: str, app_name: str) -> str:
    pass


def convert_args_list_to_dict(kvs: Optional[List[str]] = None) -> dict:
    """
    Convert a list of key-value strings to a dictionary.

    Args:
        kvs (Optional[List[str]]): A list of key-value strings in the format "key=value".

    Returns:
        dict: A dictionary containing the key-value pairs from the input list.
    """
    pass


def prepare_job_folder(cmd_args):
    pass


def is_subdir(path, directory):
    # Normalize the paths to avoid issues with different OS formats
    pass


def prepare_app_scripts(job_folder, app_custom_dirs, cmd_args):
    pass


def prepare_app_dirs(job_folder: str, app_names: List[str]) -> List[str]:
    pass


def create_app_dir(job_folder, app_name: str = "app"):
    pass


# ---------------------------------------------------------------------------
# Section 3: New Job Lifecycle Commands
# ---------------------------------------------------------------------------


def _get_session(args=None, admin_user_dir=None, username=None, study="default"):
    """Create a secure session using the startup kit."""
    pass


@contextmanager
def _session(args=None, admin_user_dir=None, username=None, study="default"):
    pass


def _get_arg_value(args, name, default=None):
    pass


def _job_session_for_args(cmd_args=None, study="default"):
    pass


def cmd_job_list(cmd_args):
    pass


def cmd_job_meta(cmd_args):
    pass


def cmd_job_abort(cmd_args):
    pass


def cmd_job_clone(cmd_args):
    pass


def cmd_job_download(cmd_args):
    pass


def cmd_job_delete(cmd_args):
    pass


# ---------------------------------------------------------------------------
# Parser definitions for new commands
# ---------------------------------------------------------------------------


def define_list_jobs_parser(job_subparser):
    pass


def define_job_meta_parser(job_subparser):
    pass


def define_abort_job_parser(job_subparser):
    pass


def define_clone_job_parser(job_subparser):
    pass


def define_download_job_parser(job_subparser):
    pass


def define_delete_job_parser(job_subparser):
    pass


_TERMINAL_JOB_STATES = {"FINISHED_OK", "FINISHED_EXCEPTION", "ABORTED", "ABANDONED", "FAILED"}


def cmd_job_stats(cmd_args):
    pass


def cmd_job_logs(cmd_args):
    pass


def define_job_stats_parser(job_subparser):
    pass


def define_job_logs_parser(job_subparser):
    pass


def _summarize_monitor_meta(meta: dict, job_meta_key_cls) -> dict:
    pass


def _parse_monitor_start_ts(meta: dict, start_time_key: str, submit_time_iso_key: str) -> float:
    pass


def _parse_monitor_duration_seconds(value) -> float:
    pass


def _build_monitor_key_aliases(extra_metrics: list) -> dict:
    pass


def _extract_monitor_metrics(stats: dict, key_aliases: dict) -> dict:
    def _find_key(d: dict, keys: list):
        pass
    def _search(d: dict, keys: list):
        pass
    pass


def _make_monitor_state() -> dict:
    pass


def _refresh_monitor_stats(sess, job_id: str, state: dict, stats_target: str, key_aliases: dict):
    pass


def _emit_monitor_progress(job_id: str, job_meta: dict, state: dict, now: float, start: float, start_ts):
    pass


def _build_monitor_status_callback(
    start: float, start_ts_holder: dict, emit_interval: int, stats_interval: int, stats_target: str, key_aliases: dict
):
    def _status_cb(sess, job_id, job_meta, state):
        pass
    pass


def _build_monitor_output_data(
    job_id: str, meta: dict, start: float, start_ts, cb_state: dict, json_mode: bool
) -> dict:
    pass


def cmd_job_monitor(cmd_args):
    pass


def cmd_job_log(cmd_args):
    pass


def define_job_monitor_parser(job_subparser):
    pass


def define_job_log_parser(job_subparser):
    pass
