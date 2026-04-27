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

"""FL Admin commands."""

from nvflare.apis.fl_constant import AdminCommandNames, FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.fuel.utils.log_utils import dynamic_log_config
from nvflare.private.fed.client.client_status import get_status_message
from nvflare.security.logging import secure_format_exception
from nvflare.widgets.info_collector import InfoCollector
from nvflare.widgets.widget import WidgetID


class CommandProcessor(object):
    """The CommandProcessor is responsible for processing a command from parent process."""

    def get_command_name(self) -> str:
        """Get command name that this processor will handle.

        Returns: name of the command

        """
        pass

    def process(self, data: Shareable, fl_ctx: FLContext):
        """Called to process the specified command.

        Args:
            data: process data
            fl_ctx: FLContext

        Return: reply message

        """
        pass


class CheckStatusCommand(CommandProcessor):
    """To implement the check_status command."""

    def get_command_name(self) -> str:
        """To get thee command name.

        Returns: AdminCommandNames.CHECK_STATUSv

        """
        pass

    def process(self, data: Shareable, fl_ctx: FLContext):
        """Called to process the check_status command.

        Args:
            data: process data
            fl_ctx: FLContext

        Returns: status message

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


class AbortTaskCommand(CommandProcessor):
    """To implement the abort_task command."""

    def get_command_name(self) -> str:
        """To get the command name.

        Returns: AdminCommandNames.ABORT_TASK

        """
        pass

    def process(self, data: Shareable, fl_ctx: FLContext):
        """Called to process the abort_task command.

        Args:
            data: process data
            fl_ctx: FLContext

        Returns: abort_task command message

        """
        pass


class ShowStatsCommand(CommandProcessor):
    """To implement the show_stats command."""

    def get_command_name(self) -> str:
        """To get the command name.

        Returns: AdminCommandNames.SHOW_STATS

        """
        pass

    def process(self, data: Shareable, fl_ctx: FLContext):
        """Called to process the abort_task command.

        Args:
            data: process data
            fl_ctx: FLContext

        Returns: show_stats command message

        """
        pass


class ShowErrorsCommand(CommandProcessor):
    """To implement the show_errors command."""

    def get_command_name(self) -> str:
        """To get the command name.

        Returns: AdminCommandNames.SHOW_ERRORS

        """
        pass

    def process(self, data: Shareable, fl_ctx: FLContext):
        """Called to process the show_errors command.

        Args:
            data: process data
            fl_ctx: FLContext

        Returns: show_errors command message

        """
        pass


class ResetErrorsCommand(CommandProcessor):
    """To implement the reset_errors command."""

    def get_command_name(self) -> str:
        """To get the command name.

        Returns: AdminCommandNames.RESET_ERRORS

        """
        pass

    def process(self, data: Shareable, fl_ctx: FLContext):
        """Called to process the reset_errors command.

        Args:
            data: process data
            fl_ctx: FLContext

        Returns: reset_errors command message

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

        Returns: configure_job_log command message

        """
        pass


class AdminCommands(object):
    """AdminCommands contains all the commands for processing the commands from the parent process."""

    commands = [
        CheckStatusCommand(),
        AbortCommand(),
        AbortTaskCommand(),
        ByeCommand(),
        ShowStatsCommand(),
        ShowErrorsCommand(),
        ResetErrorsCommand(),
        ConfigureJobLogCommand(),
    ]

    @staticmethod
    def get_command(command_name):
        """Call to return the AdminCommand object.

        Args:
            command_name: AdminCommand name

        Returns: AdminCommand object

        """
        pass

    @staticmethod
    def register_command(command_processor: CommandProcessor):
        """Call to register the AdminCommand processor.

        Args:
            command_processor: AdminCommand processor

        """
        pass
