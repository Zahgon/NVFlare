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

"""FL Admin commands."""

import time
from abc import ABC, abstractmethod
from typing import List

from nvflare.apis.fl_constant import (
    AdminCommandNames,
    FLContextKey,
    MachineStatus,
    ReturnCode,
    ServerCommandKey,
    ServerCommandNames,
)
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.apis.utils.fl_context_utils import gen_new_peer_ctx
from nvflare.fuel.utils.log_utils import dynamic_log_config, get_obj_logger
from nvflare.private.defs import SpecialTaskName, TaskConstant
from nvflare.security.logging import secure_format_exception, secure_format_traceback
from nvflare.widgets.widget import WidgetID

NO_OP_REPLY = "__no_op_reply"


class CommandProcessor(ABC):
    """The CommandProcessor is responsible for processing a command from parent process."""

    def __init__(self) -> None:
        self.logger = get_obj_logger(self)

    @abstractmethod
    def get_command_name(self) -> str:
        """Gets the command name that this processor will handle.

        Returns:
            name of the command
        """
        pass

    @abstractmethod
    def process(self, data: Shareable, fl_ctx: FLContext):
        """Processes the data.

        Args:
            data: process data
            fl_ctx: FLContext

        Return:
            A reply message
        """
        pass


class ServerStateCheck(ABC):
    """Server command requires the server state check"""

    @abstractmethod
    def get_state_check(self, fl_ctx: FLContext) -> dict:
        """Get the state check data for the server command.

        Args:
            fl_ctx: FLContext

        Returns: server state check dict data

        """
        pass


class AbortCommand(CommandProcessor):
    """To implement the abort command."""

    def get_command_name(self) -> str:
        """To get the command name.

        Returns: AdminCommandNames.ABORT

        """
        pass

    def process(self, data: Shareable, fl_ctx: FLContext):
        """Called to process the abort command.

        Args:
            data: process data
            fl_ctx: FLContext

        Returns: abort command message

        """
        pass


class GetRunInfoCommand(CommandProcessor):
    """Implements the GET_RUN_INFO command."""

    def get_command_name(self) -> str:
        pass

    def process(self, data: Shareable, fl_ctx: FLContext):
        pass


class GetTaskCommand(CommandProcessor, ServerStateCheck):
    """To implement the server GetTask command."""

    def get_command_name(self) -> str:
        """To get the command name.

        Returns: ServerCommandNames.GET_TASK

        """
        pass

    def process(self, data: Shareable, fl_ctx: FLContext):
        """Called to process the GetTask command.

        Args:
            data: process data
            fl_ctx: FLContext

        Returns: task data

        """
        pass

    def get_state_check(self, fl_ctx: FLContext) -> dict:
        pass


class SubmitUpdateCommand(CommandProcessor, ServerStateCheck):
    """To implement the server GetTask command."""

    def get_command_name(self) -> str:
        """To get the command name.

        Returns: ServerCommandNames.SUBMIT_UPDATE

        """
        pass

    def process(self, data: Shareable, fl_ctx: FLContext):
        """Called to process the abort command.

        Args:
            data: process data
            fl_ctx: FLContext

        Returns:

        """
        pass

    def get_state_check(self, fl_ctx: FLContext) -> dict:
        pass


class HandleDeadJobCommand(CommandProcessor):
    """To implement the server HandleDeadJob command."""

    def get_command_name(self) -> str:
        """To get the command name.

        Returns: ServerCommandNames.SUBMIT_UPDATE

        """
        pass

    def process(self, data: Shareable, fl_ctx: FLContext):
        """Called to process the HandleDeadJob command.

        Args:
            data: process data
            fl_ctx: FLContext

        Returns:

        """
        pass


class ShowStatsCommand(CommandProcessor):
    """To implement the show_stats command."""

    def get_command_name(self) -> str:
        """To get the command name.

        Returns: ServerCommandNames.SHOW_STATS

        """
        pass

    def process(self, data: Shareable, fl_ctx: FLContext):
        """Called to process the abort command.

        Args:
            data: process data
            fl_ctx: FLContext

        Returns: Engine run_info

        """
        pass


class GetErrorsCommand(CommandProcessor):
    """To implement the show_errors command."""

    def get_command_name(self) -> str:
        """To get the command name.

        Returns: ServerCommandNames.GET_ERRORS

        """
        pass

    def process(self, data: Shareable, fl_ctx: FLContext):
        """Called to process the abort command.

        Args:
            data: process data
            fl_ctx: FLContext

        Returns: Engine run_info

        """
        pass


class ResetErrorsCommand(CommandProcessor):
    """To implement the show_errors command."""

    def get_command_name(self) -> str:
        """To get the command name.

        Returns: ServerCommandNames.GET_ERRORS

        """
        pass

    def process(self, data: Shareable, fl_ctx: FLContext):
        """Called to process the abort command.

        Args:
            data: process data
            fl_ctx: FLContext

        """
        pass


class ByeCommand(CommandProcessor):
    """To implement the ShutdownCommand."""

    def get_command_name(self) -> str:
        """To get the command name.

        Returns: AdminCommandNames.SHUTDOWN

        """
        pass

    def process(self, data: Shareable, fl_ctx: FLContext):
        """Called to process the Shutdown command.

        Args:
            data: process data
            fl_ctx: FLContext

        Returns: Shutdown command message

        """
        pass


class HeartbeatCommand(CommandProcessor):
    """To implement the HEARTBEATCommand."""

    def get_command_name(self) -> str:
        """To get the command name.

        Returns: AdminCommandNames.HEARTBEAT

        """
        pass

    def process(self, data: Shareable, fl_ctx: FLContext):
        """Called to process the HEARTBEAT command.

        Args:
            data: process data
            fl_ctx: FLContext

        """
        pass


class ServerStateCommand(CommandProcessor):
    """To implement the ServerStateCommand."""

    def get_command_name(self) -> str:
        """To get the command name.

        Returns: AdminCommandNames.SERVER_STATE

        """
        pass

    def process(self, data: Shareable, fl_ctx: FLContext):
        """Called to process the SERVER_STATE command.

        Args:
            data: ServerState object
            fl_ctx: FLContext

        """
        pass


class ConfigureJobLogCommand(CommandProcessor):
    """To implement the configure_job_log command."""

    def get_command_name(self) -> str:
        """To get the command name.

        Returns: AdminCommandNames.CONFIGURE_JOB_LOG

        """
        pass

    def process(self, data: Shareable, fl_ctx: FLContext):
        """Called to process the configure_job_log command.

        Args:
            data: process data
            fl_ctx: FLContext

        """
        pass


class AppCommandProcessor(CommandProcessor):
    def get_command_name(self) -> str:
        """To get the command name.

        Returns: AdminCommandNames.SERVER_STATE

        """
        pass

    def process(self, data: Shareable, fl_ctx: FLContext):
        pass


class ServerCommands(object):
    """AdminCommands contains all the commands for processing the commands from the parent process."""

    commands: List[CommandProcessor] = [
        AbortCommand(),
        ByeCommand(),
        GetRunInfoCommand(),
        GetTaskCommand(),
        SubmitUpdateCommand(),
        HandleDeadJobCommand(),
        ShowStatsCommand(),
        GetErrorsCommand(),
        ResetErrorsCommand(),
        HeartbeatCommand(),
        ServerStateCommand(),
        ConfigureJobLogCommand(),
        AppCommandProcessor(),
    ]

    client_request_commands_names = [
        ServerCommandNames.GET_TASK,
        ServerCommandNames.SUBMIT_UPDATE,
    ]

    app_cmd_registry = {}

    @classmethod
    def get_command(cls, command_name):
        """Call to return the AdminCommand object.

        Args:
            command_name: AdminCommand name

        Returns: AdminCommand object

        """
        pass

    @classmethod
    def register_app_command(cls, topic: str, cmd_func, *args, **kwargs):
        """Called to register an app command.

        Args:
            topic: topic that the command will process
            cmd_func: the function to process the command
        """
        pass

    @classmethod
    def get_app_command(cls, topic: str):
        pass
