# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
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

import logging
import os
import signal
import subprocess
from typing import List, Optional

log = logging.getLogger(__name__)

_POSIX_SPAWN_SUPPORTED = hasattr(os, "posix_spawn") and os.name == "posix"


class ProcessAdapter:
    def __init__(self, process: Optional[subprocess.Popen] = None, pid: Optional[int] = None):
        """Adapter to manage a process, whether created via subprocess.Popen or os.posix_spawn.

        Args:
            process: The subprocess.Popen object (if created via subprocess)
            pid: The process ID (if created via posix_spawn, or fallback for process.pid)
        """
        self.process = process
        self.pid = pid if pid is not None else (process.pid if process else None)
        self.logger = logging.getLogger(self.__class__.__name__)
        self._return_code: Optional[int] = None

        if self.pid is None:
            raise ValueError("ProcessAdapter requires either a process object or a pid.")

    def terminate(self) -> None:
        """Terminate the process group.

        Sends SIGKILL to the entire process group. No need to call process.terminate()
        separately since SIGKILL already terminates all processes in the group.
        """
        pass

    def poll(self) -> Optional[int]:
        """Check if the process has terminated.

        Returns:
            None if process is still running, otherwise the exit code.
        """
        pass

    def wait(self) -> None:
        """Wait for the process to terminate."""
        pass

    def _poll_pid(self) -> Optional[int]:
        pass

    def _decode_status(self, status: int) -> int:
        pass

    def _kill_process_group(self):
        pass


def spawn_process(cmd_args: List[str], env: dict) -> ProcessAdapter:
    """Launch a process using posix_spawn if available, falling back to subprocess.Popen.

    This method attempts to use os.posix_spawn with setsid=True to avoid fork() related issues
    (such as gRPC deadlocks). If posix_spawn is unavailable or fails, it falls back to
    subprocess.Popen with preexec_fn=os.setsid.

    Args:
        cmd_args: The command arguments as a list of strings.
        env: The environment variables dictionary.

    Returns:
        ProcessAdapter: An adapter wrapping the launched process.
    """
    pass
