# Copyright (c) 2026, NVIDIA CORPORATION.  All rights reserved.
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
import itertools
import logging
import os
import threading
import time

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import ReservedKey, StreamCtxKey, WorkspaceConstants
from nvflare.apis.fl_context import FLContext
from nvflare.apis.signal import Signal
from nvflare.app_common.logging.constants import LIVE_LOG_TOPIC, Channels
from nvflare.app_common.streamers.log_streamer import LogStreamer
from nvflare.widgets.widget import Widget

_thread_counter = itertools.count()


class JobLogStreamer(Widget):
    """Streams a job log file to the server in real-time.

    ``JobLogStreamer`` tails the live log file from the moment the job starts
    and streams new bytes to the server as they are written. The stream is
    drained and closed cleanly when the job completes or is aborted.

    The log file path is discovered by inspecting the active Python logging
    handlers, so it works correctly in both the simulator and production
    without any workspace path arithmetic.

    This widget runs inside the job subprocess (``CLIENT_JOB`` or ``SERVER_JOB``)
    and must be placed in the job-level configuration (``config_fed_client.json``
    or ``config_fed_server.json``).  To stream multiple log files, add one
    ``JobLogStreamer`` per file.

    Args:
        log_file_name: base name of the log file to stream.  Defaults to
            ``WorkspaceConstants.LOG_FILE_NAME`` (``"log.txt"``).
        liveness_interval: seconds between heartbeat messages when no new log
            bytes have been written (default 10.0).  Must be less than the
            receiver's ``idle_timeout``.
        poll_interval: seconds between polls when the log file has no new data
            (default 0.5).
    """

    def __init__(
        self,
        log_file_name: str = WorkspaceConstants.LOG_FILE_NAME,
        liveness_interval: float = 10.0,
        poll_interval: float = 0.5,
    ):
        super().__init__()
        if os.path.isabs(log_file_name):
            raise ValueError(f"log_file_name must be a relative base name, not an absolute path: {log_file_name}")
        if ".." in log_file_name.split(os.sep):
            raise ValueError(f"log_file_name must not contain '..': {log_file_name}")
        self._log_file_name = log_file_name
        self._liveness_interval = liveness_interval
        self._poll_interval = poll_interval
        self._stop_event: threading.Event = None
        self._stream_thread: threading.Thread = None
        self.register_event_handler(EventType.START_RUN, self._on_job_started)
        self.register_event_handler(EventType.ABOUT_TO_END_RUN, self._on_about_to_end_run)
        self.register_event_handler(EventType.END_RUN, self._on_job_ended)

    def _find_log_path(self) -> str:
        """Return the path for log_file_name by locating the log directory from any active file handler.

        All log files (log.txt, log_fl.txt, error_log.txt, …) reside in the same directory.
        Some of them may not have an active handler in this process (e.g. written by another
        process), so we find the directory from whichever file handler is active and construct
        the target path from it.
        """
        pass

    def _do_stream(self, log_path: str, client_name: str, job_id: str, fl_ctx: FLContext):
        pass

    def _on_job_started(self, event_type: str, fl_ctx: FLContext):
        pass

    def _on_about_to_end_run(self, event_type: str, fl_ctx: FLContext):
        # Signal the streaming thread to stop but do NOT join here.  Returning quickly lets
        # the event dispatcher proceed immediately so that ABOUT_TO_END_RUN-era log lines
        # (written by ClientRunner after fire_event returns) land in the log file while the
        # streaming thread is still draining — they will be picked up by the drain retry.
        pass

    def _on_job_ended(self, event_type: str, fl_ctx: FLContext):
        # Join in END_RUN — keeps client_run() alive until the streaming thread has sent EOF
        # and the server has received it.  This prevents server.abort_run() (which fires after
        # executor.shutdown() returns) from racing with the in-flight stream.
        pass
