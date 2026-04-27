# Copyright (c) 2026, NVIDIA CORPORATION.  All rights reserved.
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
import os
import sys
from contextlib import contextmanager

from nvflare.cli_unknown_cmd_exception import CLIUnknownCmdException
from nvflare.fuel.flare_api.api_spec import (
    AuthenticationError,
    AuthorizationError,
    CommandError,
    InternalError,
    InvalidArgumentError,
    NoConnection,
)
from nvflare.tool.cli_output import output_error, output_error_message, output_ok, output_usage_error
from nvflare.tool.job.job_cli import _resolve_admin_user_and_dir_from_startup_kit
from nvflare.utils.cli_utils import get_startup_kit_dir_for_target

CMD_STUDY_REGISTER = "register"
CMD_STUDY_ADD_SITE = "add-site"
CMD_STUDY_REMOVE_SITE = "remove-site"
CMD_STUDY_REMOVE = "remove"
CMD_STUDY_LIST = "list"
CMD_STUDY_SHOW = "show"
CMD_STUDY_ADD_USER = "add-user"
CMD_STUDY_REMOVE_USER = "remove-user"
POC_DEFAULT_ORG = "nvidia"

_study_sub_cmd_parsers = {}
_study_handlers = {}
_study_root_parser = None


class _WideSubcmdFormatter(argparse.HelpFormatter):
    """Ensures subcommand help text starts on the same line as the longest name."""

    def add_arguments(self, actions):
        pass


def _ensure_study_parsers():
    pass


def _add_connection_args(parser):
    pass


def _resolve_session_inputs(args):
    pass


@contextmanager
def _study_session(args):
    pass


def _handle_command_error(e: Exception):
    pass


def _get_caller_role_from_startup_kit(admin_user_dir: str) -> str:
    pass


def _try_get_caller_role(args) -> str:
    pass


def _parse_sites_arg(sites_arg: str):
    pass


def _parse_site_org_args(site_org_args):
    pass


def _output_invalid_lifecycle_args(detail: str, hint: str = "Run with -h for usage."):
    pass


def _project_admin_site_org_hint(command_label: str, study_name: str) -> str:
    pass


def _resolve_lifecycle_inputs(args, command_label: str):
    pass


def _run_with_payload(args, func, *func_args, parser=None):
    pass


def cmd_register(args):
    pass


def cmd_add_site(args):
    pass


def cmd_remove_site(args):
    pass


def cmd_remove(args):
    pass


def cmd_list(args):
    pass


def cmd_show(args):
    pass


def cmd_add_user(args):
    pass


def cmd_remove_user(args):
    pass


def _define_study_subcommands(parser):
    pass


def def_study_cli_parser(sub_cmd):
    pass


def handle_study_cmd(args):
    pass
