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

import re
import shlex
from typing import List

from nvflare.apis.fl_constant import SiteType
from nvflare.fuel.hci.cmd_arg_utils import join_args, validate_text_file_name
from nvflare.fuel.hci.conn import Connection
from nvflare.fuel.hci.proto import MetaStatusValue, make_meta
from nvflare.fuel.hci.reg import CommandModule, CommandModuleSpec, CommandSpec
from nvflare.fuel.hci.server.authz import PreAuthzReturnCode
from nvflare.fuel.hci.server.constants import ConnProps
from nvflare.fuel.hci.shell_cmd_val import (
    CatValidator,
    GrepValidator,
    HeadValidator,
    LsValidator,
    ShellCommandValidator,
    TailValidator,
)
from nvflare.private.admin_defs import Message
from nvflare.private.defs import SysCommandTopic
from nvflare.private.fed.server.admin import new_message
from nvflare.private.fed.server.message_send import ClientReply
from nvflare.private.fed.server.server_engine_internal_spec import ServerEngineInternalSpec
from nvflare.private.fed.utils.fed_utils import execute_command_directly


class _CommandExecutor(object):
    def __init__(self, cmd_name: str, validator: ShellCommandValidator):
        self.cmd_name = cmd_name
        self.validator = validator

    def authorize_command(self, conn: Connection, args: List[str]):
        pass

    def validate_shell_command(self, args: List[str], parse_result) -> str:
        pass

    def execute_command(self, conn: Connection, args: List[str]):
        pass

    def get_usage(self):
        pass


class _NoArgCmdExecutor(_CommandExecutor):
    def __init__(self, cmd_name: str):
        _CommandExecutor.__init__(self, cmd_name, None)

    def validate_shell_command(self, args: List[str], parse_result):
        pass


class _FileCmdExecutor(_CommandExecutor):
    def __init__(
        self,
        cmd_name: str,
        validator: ShellCommandValidator,
        text_file_only: bool = True,
        single_file_only: bool = True,
        file_required: bool = True,
    ):
        _CommandExecutor.__init__(self, cmd_name, validator)
        self.text_file_only = text_file_only
        self.single_file_only = single_file_only
        self.file_required = file_required

    def validate_shell_command(self, args: List[str], parse_result):
        pass


class ShellCommandModule(CommandModule):
    def get_spec(self):
        pass
