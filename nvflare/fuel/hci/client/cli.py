# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
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

import cmd
import json
import os
import signal
import threading
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from nvflare.apis.job_def import DEFAULT_STUDY

try:
    import readline
except ImportError:
    readline = None

from nvflare.fuel.hci.cmd_arg_utils import join_args, parse_command_line
from nvflare.fuel.hci.proto import ProtoKey
from nvflare.fuel.hci.reg import CommandModule, CommandModuleSpec, CommandRegister, CommandSpec
from nvflare.fuel.hci.table import Table
from nvflare.security.logging import secure_format_exception, secure_log_traceback

from .api import AdminAPI, CommandInfo
from .api_spec import AdminConfigKey, UidSource
from .api_status import APIStatus
from .event import EventContext, EventHandler, EventPropKey, EventType


class _SessionClosed(Exception):
    pass


class _BuiltInCmdModule(CommandModule):
    def get_spec(self):
        pass


class AdminClient(cmd.Cmd, EventHandler):
    """Admin command prompt for submitting admin commands to the server through the CLI.

    Args:
        cmd_modules: command modules to load and register
        debug: whether to print debug messages. False by default.
        cli_history_size: the maximum number of commands to save in the cli history file. Defaults to 1000.
    """

    def __init__(
        self,
        admin_config: dict,
        cmd_modules: Optional[List] = None,
        debug: bool = False,
        username: str = "",
        handlers=None,
        cli_history_dir: str = str(Path.home() / ".nvflare"),
        cli_history_size: int = 1000,
        study: str = DEFAULT_STUDY,
    ):
        super().__init__()
        self.intro = "Type help or ? to list commands.\n"
        self.prompt = admin_config.get(AdminConfigKey.PROMPT, "> ")
        self.user_name = username
        self._study = study
        self.debug = debug
        self.out_file = None
        self.no_stdout = False
        self.stopped = False  # use this flag to prevent unnecessary signal exception
        self.login_timeout = admin_config.get(AdminConfigKey.LOGIN_TIMEOUT)
        self.idle_timeout = admin_config.get(AdminConfigKey.IDLE_TIMEOUT, 900.0)
        self.last_active_time = time.time()

        if not cli_history_dir:
            raise Exception("missing cli_history_dir")

        modules = [_BuiltInCmdModule()]
        if cmd_modules:
            if not isinstance(cmd_modules, list):
                raise TypeError("cmd_modules must be a list.")
            for m in cmd_modules:
                if not isinstance(m, CommandModule):
                    raise TypeError("cmd_modules must be a list of CommandModule")
                modules.append(m)

        uid_source = admin_config.get(AdminConfigKey.UID_SOURCE, UidSource.USER_INPUT)
        if uid_source != UidSource.CERT:
            self.user_name = self._user_input("User Name: ")

        event_handlers = [self]
        if handlers:
            event_handlers.extend(handlers)

        self.api = AdminAPI(
            admin_config=admin_config,
            cmd_modules=modules,
            user_name=self.user_name,
            debug=self.debug,
            event_handlers=event_handlers,
            study=study,
        )

        if not os.path.isdir(cli_history_dir):
            os.mkdir(cli_history_dir)
        self.cli_history_file = os.path.join(cli_history_dir, ".admin_cli_history")

        if readline:
            readline.set_history_length(cli_history_size)

        # signal.signal(signal.SIGUSR1, partial(self.session_signal_handler))
        signal.signal(signal.SIGUSR1, self.session_signal_handler)

    def _monitor_user(self):
        pass

    def handle_event(self, event_type: str, ctx: EventContext):
        pass

    def session_signal_handler(self, signum, frame):
        pass

    def _set_output_file(self, file, no_stdout):
        pass

    def _close_output_file(self):
        pass

    def do_bye(self, arg):
        pass

    def do_lpwd(self, arg):
        """print local current work dir"""
        pass

    def do_timeout(self, arg):
        pass

    def emptyline(self):
        pass

    def _show_one_command(self, cmd_name, reg, show_invisible=False):
        pass

    def _show_commands(self, reg: CommandRegister):
        pass

    def do_help(self, arg):
        pass

    def complete(self, text, state):
        pass

    def default(self, line):
        pass

    def _user_input(self, prompt: str) -> str:
        pass

    def _do_default(self, line):
        pass

    def preloop(self):
        pass

    def postcmd(self, stop, line):
        pass

    def cmdloop(self, intro=None):
        """Repeatedly issue a prompt, accept input, parse an initial prefix
        off the received input, and dispatch to action methods, passing them
        the remainder of the line as argument.
        Overriding what is in cmd.Cmd to handle exiting client on Ctrl+D (EOF).
        """
        pass

    def run(self):
        pass

    def print_resp(self, resp: dict):
        """Prints the server response

        Args:
            resp (dict): The server response.
        """
        pass

    def write_stdout(self, data: str):
        pass

    def _write(self, content: str):
        pass

    def write_string(self, data: str):
        pass

    def write_table(self, table: Table):
        pass

    def write_dict(self, data: dict):
        pass

    def write_error(self, err: str):
        pass

    def flush(self):
        pass
