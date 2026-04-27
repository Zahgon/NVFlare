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
import os
import shutil
import tempfile

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import ReturnCode, SystemComponents, WorkspaceConstants
from nvflare.apis.fl_context import FLContext
from nvflare.apis.storage import DataTypes
from nvflare.apis.streaming import StreamContext
from nvflare.app_common.logging.constants import LIVE_LOG_TOPIC, Channels
from nvflare.app_common.streamers.log_streamer import LogStreamer
from nvflare.widgets.widget import Widget

# Keys for per-stream state stored in StreamContext
_KEY_RECV_FILE = "JobLogReceiver.recv_file"
_KEY_RECV_PATH = "JobLogReceiver.recv_path"


class JobLogReceiver(Widget):
    """Receives live log data streamed by :class:`JobLogStreamer`.

    ``JobLogReceiver`` accepts a live stream: each chunk is written directly to
    its final file as it arrives so that the log can be followed with
    ``tail -f`` on the server while the job runs. When the stream closes
    (normal EOF, job abort, or idle timeout) the file is handed to the job
    manager for storage.

    The destination file is written to ``{dest_dir}/{job_id}/{client_name}/{log_file_name}``,
    making it easy to locate and tail during a run.

    This widget can be placed in either of two locations:

    **Job-level configuration** (``config_fed_server.json``)
        Add it via ``job.to_server(JobLogReceiver())`` in the Job API, or
        declare it in the job's server config.  In this mode the handler is
        registered on ``START_RUN``, which fires when the job begins.  The
        widget is only active for that specific job.

    **System-level resources** (``resources.json`` on the server)
        Declare it as a system component so it is instantiated when the server
        process starts.  In this mode the handler is registered on
        ``SYSTEM_START`` and remains active for every job that runs on that
        server for the lifetime of the process.

    Regardless of placement, the stream handler is registered exactly once.

    Args:
        dest_dir: directory where incoming log files are written.
            Defaults to the system temporary directory.
        idle_timeout: seconds without any message (data or heartbeat) before
            the receiver declares the sender dead and closes the stream
            (default 30.0).  Set to 0 to disable.
    """

    def __init__(self, dest_dir: str = None, idle_timeout: float = 30.0):
        super().__init__()
        self._dest_dir = dest_dir
        self._idle_timeout = idle_timeout
        self._registered = False
        self.register_event_handler([EventType.SYSTEM_START, EventType.START_RUN], self._register)

    def _effective_dest_dir(self) -> str:
        pass

    @staticmethod
    def _sanitize_path_component(name: str) -> str:
        """Strip path separators and traversal sequences from a single path component."""
        pass

    @classmethod
    def _storage_data_type(cls, log_file_name: str) -> str:
        pass

    def _get_trusted_stream_identity(self, fl_ctx: FLContext):
        pass

    def _on_chunk_received(self, data: bytes, stream_ctx: StreamContext, fl_ctx: FLContext):
        pass

    def _on_stream_done(self, stream_ctx: StreamContext, fl_ctx: FLContext):
        pass

    def _register(self, event_type: str, fl_ctx: FLContext):
        pass
