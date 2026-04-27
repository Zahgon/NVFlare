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
import os
import shlex
import subprocess
import sys
import threading

from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.workspace import Workspace
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.fuel.utils.validation_utils import check_object_type, check_str


class StopMethod:
    KILL = "kill"
    TERMINATE = "terminate"


class CommandDescriptor:
    def __init__(
        self,
        cmd: str,
        cwd=None,
        env=None,
        log_file_name: str = "",
        log_stdout: bool = True,
        stdout_msg_prefix: str = None,
        stop_method=StopMethod.KILL,
    ):
        """Constructor of CommandDescriptor.
        A CommandDescriptor describes the requirements of the new process to be started.

        Args:
            cmd: the command to be executed to start the new process
            cwd: current work dir for the new process
            env: system env for the new process
            log_file_name: base name of the log file.
            log_stdout: whether to output log messages to stdout.
            stdout_msg_prefix: prefix to be prepended to log message when writing to stdout.
                Since multiple processes could be running within the same terminal window, the prefix can help
                differentiate log messages from these processes.
            stop_method: how to stop the command (kill or terminate)
        """
        check_str("cmd", cmd)

        if cwd:
            check_str("cwd", cwd)

        if env:
            check_object_type("env", env, dict)

        if log_file_name:
            check_str("log_file_name", log_file_name)

        if stdout_msg_prefix:
            check_str("stdout_msg_prefix", stdout_msg_prefix)

        valid_stop_methods = [StopMethod.KILL, StopMethod.TERMINATE]
        if stop_method not in valid_stop_methods:
            raise ValueError(f"invalid stop_method '{stop_method}': must be one of {valid_stop_methods}")

        self.cmd = cmd
        self.cwd = cwd
        self.env = env
        self.log_file_name = log_file_name
        self.log_stdout = log_stdout
        self.stdout_msg_prefix = stdout_msg_prefix
        self.stop_method = stop_method


class ProcessManager:
    def __init__(self, cmd_desc: CommandDescriptor, stop_method="kill"):
        """Constructor of ProcessManager.
        ProcessManager provides methods for managing the lifecycle of a subprocess (start, stop, poll), as well
        as the handling of log file to be used by the subprocess.

        Args:
            cmd_desc: the CommandDescriptor that describes the command of the new process to be started

        NOTE: the methods of ProcessManager are not thread safe.

        """
        check_object_type("cmd_desc", cmd_desc, CommandDescriptor)
        self.process = None
        self.cmd_desc = cmd_desc
        self.stop_method = stop_method
        self.log_file = None
        self.msg_prefix = None
        self.file_lock = threading.Lock()
        self.logger = get_obj_logger(self)

    def start(
        self,
        fl_ctx: FLContext,
    ):
        """Start the new process.

        Args:
            fl_ctx: FLContext object.

        Returns: None

        """
        pass

    def _write_log(self):
        # write messages from the process's stdout pipe to log file and sys.stdout.
        # note that depending on how the process flushes out its output, the messages may be buffered/delayed.
        pass

    def poll(self):
        """Perform a poll request on the process.

        Returns: None if the process is still running; an exit code (int) if process is not running.

        """
        pass

    def stop(self) -> int:
        """Stop the process.
        If the process is still running, kill the process. If a log file is open, close the log file.

        Returns: the exit code of the process. If killed, returns -9.

        """
        pass


def start_process(cmd_desc: CommandDescriptor, fl_ctx: FLContext, stop_method="kill") -> ProcessManager:
    """Convenience function for starting a subprocess.

    Args:
        cmd_desc: the CommandDescriptor the describes the command to be executed
        fl_ctx: FLContext object
        stop_method: how to stop the process

    Returns: a ProcessManager object.

    """
    pass


def run_command(cmd_desc: CommandDescriptor) -> str:
    pass
