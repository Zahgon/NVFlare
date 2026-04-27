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

import sys
import time
from contextlib import contextmanager

import nvflare
from nvflare.tool.cli_output import output_error, output_error_message, output_ok, output_usage_error

CMD_SYSTEM_STATUS = "status"
CMD_SYSTEM_RESOURCES = "resources"
CMD_SYSTEM_SHUTDOWN = "shutdown"
CMD_SYSTEM_RESTART = "restart"
CMD_SYSTEM_REMOVE_CLIENT = "remove-client"
CMD_SYSTEM_VERSION = "version"
CMD_SYSTEM_LOG_CONFIG = "log-config"

_system_sub_cmd_parsers = {}


def _add_system_connection_args(parser):
    pass


def def_system_cli_parser(system_parser):
    """system_parser is already created in cli.py — add subcommands here."""
    pass


def _confirm_or_force(prompt, args):
    """Prompt for confirmation unless --force is set."""
    pass


def _get_system_session(args=None):
    """Create a secure session using the startup kit."""
    pass


@contextmanager
def _system_session(args=None):
    pass


def _fmt_ts(ts):
    pass


def _render_status_human(result, target_type):
    pass


def _output_system_status(result, target_type):
    pass


def _render_version_human(result):
    pass


def _output_system_version(result):
    pass


def cmd_system_status(args):
    pass


def cmd_system_resources(args):
    pass


def cmd_system_shutdown(args):
    pass


def cmd_system_restart(args):
    pass


def cmd_system_version(args):
    pass


def cmd_system_log(args):
    pass


def cmd_system_remove_client(args):
    pass


_system_handlers = {
    CMD_SYSTEM_STATUS: cmd_system_status,
    CMD_SYSTEM_RESOURCES: cmd_system_resources,
    CMD_SYSTEM_SHUTDOWN: cmd_system_shutdown,
    CMD_SYSTEM_RESTART: cmd_system_restart,
    CMD_SYSTEM_REMOVE_CLIENT: cmd_system_remove_client,
    CMD_SYSTEM_VERSION: cmd_system_version,
    CMD_SYSTEM_LOG_CONFIG: cmd_system_log,
}


def handle_system_cmd(args):
    pass
