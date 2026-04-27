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

from nvflare.fuel.hci.conn import Connection
from nvflare.fuel.hci.reg import CommandEntry, CommandModule, CommandModuleSpec, CommandSpec

from .reg import ServerCommandRegister


class BuiltInCmdModule(CommandModule):
    def __init__(self, reg: ServerCommandRegister):
        """Built in CommandModule with the ability to list commands.

        Args:
            reg: ServerCommandRegister
        """
        self.reg = reg

    def get_spec(self):
        pass

    def _show_command(self, conn: Connection, cmd_name):
        pass

    def handle_list_commands(self, conn: Connection, args: List[str]):
        pass


def new_command_register_with_builtin_module(app_ctx):
    """Creates ServerCommandRegister and registers builtin command module.

    Args:
        app_ctx: engine

    Returns: ServerCommandRegister

    """
    pass
