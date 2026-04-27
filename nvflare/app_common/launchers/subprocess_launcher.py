# Copyright (c) 2023, NVIDIA CORPORATION.  All rights reserved.
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

import os
import re
import shlex
import subprocess
from threading import Lock, Thread
from typing import Optional

from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.apis.signal import Signal
from nvflare.app_common.abstract.launcher import Launcher, LauncherRunStatus
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.utils.job_launcher_utils import add_custom_dir_to_path


def get_line(buffer: bytearray):
    """Read a line from the binary buffer. It treats all combinations of \n and \r as line breaks.

    Args:
        buffer: A binary buffer

    Returns:
        (line, remaining): Return the first line as str and the remaining buffer.
        line is None if no newline found

    """
    pass


# Matches the start of a formatted NVFlare log line after stripping ANSI color
# codes: "YYYY-MM-DD HH:MM:SS" produced by BaseFormatter / ColorFormatter.
# Lines from the subprocess consoleHandler match this; raw print() lines do not.
_ANSI_ESC_RE = re.compile(r"\x1b\[[0-9;]*m")
_LOG_LINE_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")


def _route_subprocess_line(line: str, logger) -> None:
    """Route one stdout line from the subprocess to the right destination.

    Formatted log lines (from the subprocess consoleHandler) are already written
    to the shared log files by the subprocess file handler, so we just print them
    to the terminal for interactive visibility.  Raw print() lines from user
    training scripts have no timestamp, so we wrap them with logger.info() to
    ensure they reach both the terminal and log.txt.
    """
    pass


def log_subprocess_output(process, logger):

    pass


class SubprocessLauncher(Launcher):
    def __init__(
        self,
        script: str,
        launch_once: Optional[bool] = True,
        clean_up_script: Optional[str] = None,
        shutdown_timeout: Optional[float] = 0.0,
    ):
        """Initializes the SubprocessLauncher.

        Args:
            script (str): Script to be launched using subprocess.
            launch_once (bool): Whether the external process will be launched only once at the beginning or on each task.
            clean_up_script (Optional[str]): Optional clean up script to be run after the main script execution.
            shutdown_timeout (float): If provided, will wait for this number of seconds before shutdown.
        """
        super().__init__()

        self._app_dir = None
        self._process = None
        self._script = script
        self._launch_once = launch_once
        self._clean_up_script = clean_up_script
        self._shutdown_timeout = shutdown_timeout
        self._lock = Lock()
        self.logger = get_obj_logger(self)

    def initialize(self, fl_ctx: FLContext):
        pass

    def finalize(self, fl_ctx: FLContext) -> None:
        pass

    def needs_deferred_stop(self) -> bool:
        pass

    def launch_task(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> bool:
        pass

    def stop_task(self, task_name: str, fl_ctx: FLContext, abort_signal: Signal) -> None:
        pass

    def _start_external_process(self, fl_ctx: FLContext):
        pass

    def _stop_external_process(self):
        pass

    def check_run_status(self, task_name: str, fl_ctx: FLContext) -> str:
        pass
