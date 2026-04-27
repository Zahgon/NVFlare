# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
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
import time
from abc import ABC, abstractmethod

from nvflare.security.logging import secure_format_exception

from .applet import Applet
from .defs import Constant
from .process_mgr import CommandDescriptor, start_process


class CLIApplet(Applet, ABC):
    def __init__(self, stop_method="kill"):
        """Constructor of CLIApplet, which runs the applet as a subprocess started with CLI command."""
        Applet.__init__(self)
        self.stop_method = stop_method
        self._proc_mgr = None
        self._start_error = False

    @abstractmethod
    def get_command(self, app_ctx: dict) -> CommandDescriptor:
        """Subclass must implement this method to return the CLI command to be executed.

        Args:
            app_ctx: the applet context that contains execution env info

        Returns: a CommandDescriptor that describes the CLI command

        """
        pass

    def start(self, app_ctx: dict):
        """Start the execution of the applet.

        Args:
            app_ctx: the applet run context

        Returns:

        """
        pass

    def stop(self, timeout=0.0) -> int:
        """Stop the applet

        Args:
            timeout: amount of time to wait for the applet to stop by itself. If the applet does not stop on
                its own within this time, we'll forcefully stop it by kill.

        Returns: exit code

        """
        pass

    def is_stopped(self) -> (bool, int):
        pass
