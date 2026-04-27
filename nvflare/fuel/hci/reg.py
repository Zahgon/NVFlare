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

from nvflare.fuel.hci.proto import ConfirmMethod


class CommandSpec(object):

    valid_confirms = ["none", ConfirmMethod.YESNO, ConfirmMethod.AUTH]

    def __init__(
        self,
        name: str,
        description: str,
        usage: str,
        handler_func,
        authz_func=None,
        visible=True,
        confirm=None,
        client_cmd=None,
        enabled=True,
        scope_name="",
    ):
        """Specification of a command within a CommandModuleSpec to register into CommandRegister as a CommandEntry.

        Args:
            name: command name
            description: command description text
            usage: string to show usage of the command
            handler_func: function to call for executing the command.
            authz_func: called to preprocess the command by AuthzFilter.
            visible: whether the command is visible or not
            confirm: whether the command needs confirmation to execute
        """
        self.name = name
        self.description = description
        self.usage = usage
        self.handler_func = handler_func
        self.authz_func = authz_func
        self.visible = visible
        self.confirm = confirm
        self.client_cmd = client_cmd
        self.enabled = enabled
        self.scope_name = scope_name

        if not confirm:
            self.confirm = "none"
        else:
            assert confirm in CommandSpec.valid_confirms


class CommandModuleSpec(object):
    def __init__(self, name: str, cmd_specs: List[CommandSpec], conn_props: dict = None):
        """Specification for a command module containing a list of commands in the form of CommandSpec.

        Args:
            name: becomes the scope name of the commands in cmd_specs when registered in CommandRegister
            cmd_specs: list of CommandSpec objects with
            conn_props: conn properties declared by the module
        """
        self.name = name
        self.cmd_specs = cmd_specs
        self.conn_props = conn_props


class CommandModule(object):
    """Base class containing CommandModuleSpec."""

    def get_spec(self) -> CommandModuleSpec:
        pass

    def generate_module_spec(self, server_cmd_spec: CommandSpec):
        pass

    def close(self):
        pass


class CommandEntry(object):
    def __init__(self, scope, name, desc, usage, handler, authz_func, visible, confirm, client_cmd):
        """Contains information about a command. This is registered in Scope within CommandRegister.

        Args:
            scope: scope for this command
            name: command name
            desc: command description text
            usage: string to show usage of the command
            handler: function to call for executing the command
            authz_func: authorization function to run to get a tuple of (valid, authz_ctx) in AuthzFilter
            visible: whether the command is visible or not
            confirm: whether the command needs confirmation to execute
        """
        self.scope = scope
        self.name = name
        self.desc = desc
        self.usage = usage
        self.handler = handler
        self.authz_func = authz_func
        self.visible = visible
        self.confirm = confirm
        self.client_cmd = client_cmd

    def full_command_name(self) -> str:
        pass


class _Scope(object):
    def __init__(self, name: str):
        """A container grouping CommandEntry objects inside CommandRegister.

        Args:
            name: name of scope grouping commands
        """
        self.name = name
        self.entries = {}

    def register_command(
        self, cmd_name: str, cmd_desc: str, cmd_usage: str, handler_func, authz_func, visible, confirm, client_cmd
    ):
        pass


class CommandRegister(object):
    def __init__(self, app_ctx):
        """Object containing the commands in scopes once they have been registered.

        ServerCommandRegister is derived from this class and calls the handler of the command through
        ``process_command`` and ``_do_command``. This is also used to register commands for the admin client.

        Args:
            app_ctx: app context
        """
        self.app_ctx = app_ctx
        self.scopes = {}
        self.cmd_map = {}
        self.modules = []
        self.conn_props = {}  # conn properties from modules
        self.mapped_cmds = []

    def _get_scope(self, name: str):
        pass

    def get_command_entries(self, cmd_name: str):
        pass

    def register_module_spec(self, module_spec: CommandModuleSpec, include_invisible=True):
        pass

    def register_module(self, module: CommandModule, include_invisible=True):
        pass

    def add_command(
        self,
        scope_name,
        cmd_name,
        desc,
        usage,
        handler,
        authz_func,
        visible,
        confirm,
        client_cmd=None,
        map_client_cmd=False,
    ):

        pass

    def _add_cmd_entry(self, cmd_name, entry):
        pass

    def finalize(self, add_cmd_func=None):
        pass
