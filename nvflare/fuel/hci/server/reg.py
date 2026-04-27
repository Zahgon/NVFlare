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

from typing import List

from nvflare.fuel.hci.cmd_arg_utils import split_to_args
from nvflare.fuel.hci.conn import Connection
from nvflare.fuel.hci.reg import CommandRegister
from nvflare.security.logging import secure_format_exception, secure_log_traceback

from .constants import ConnProps


class CommandFilter(object):
    """Base class for filters to run before or after commands."""

    def pre_command(self, conn: Connection, args: List[str]) -> bool:
        """Code to execute before executing a command.

        Returns: True to continue filter chain or False to not
        """
        pass

    def post_command(self, conn: Connection, args: List[str]) -> bool:
        """Code to execute after executing a command."""
        pass

    def close(self):
        pass


class ServerCommandRegister(CommandRegister):
    def __init__(self, app_ctx):
        """Runs filters and executes commands by calling their handler function.

        This is the main command register used by AdminServer.

        Args:
            app_ctx: app context
        """
        CommandRegister.__init__(self, app_ctx)
        self.filters = []
        self.closed = False

    def add_filter(self, cmd_filter: CommandFilter):
        pass

    def _do_command(self, conn: Connection, command: str):
        """Executes command.

        Getting the command from the command registry, invoke filters and call the handler function, passing along conn
        and the args split from the command.
        """
        pass

    def process_command(self, conn: Connection, command: str):
        pass

    def close(self):
        pass
