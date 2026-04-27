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
import json
import os
import threading

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import FLContextKey, JobConstants, ProcessType, StreamCtxKey, WorkspaceConstants
from nvflare.apis.fl_context import FLContext
from nvflare.apis.job_def import JobMetaKey
from nvflare.apis.workspace import Workspace
from nvflare.app_common.logging.constants import LIVE_LOG_TOPIC, Channels
from nvflare.app_common.streamers.log_streamer import LogStreamer
from nvflare.security.logging import secure_format_exception
from nvflare.widgets.widget import Widget

_LOG_STREAMER_PATH = "nvflare.app_common.logging.job_log_streamer.JobLogStreamer"


class SystemLogStreamer(Widget):
    """System-level widget that injects a :class:`JobLogStreamer` into every job
    that does not already declare one.

    Place this in the client's ``resources.json`` so that live log streaming is
    provided automatically for every job — without requiring each job to include
    a ``JobLogStreamer`` in its own configuration.

    On ``BEFORE_JOB_LAUNCH`` (after the job config is deployed to disk but
    before the job subprocess starts) ``SystemLogStreamer`` reads the deployed
    ``config_fed_client.json``.  If no ``JobLogStreamer`` component is found, it
    appends one with the configured parameters and writes the file back.  The
    job subprocess then picks up the modified config and ``JobLogStreamer`` runs
    inside the job as if the user had declared it explicitly.

    When configured for ``error_log.txt``, ``SystemLogStreamer`` also uploads a
    post-run snapshot from ``CLIENT_PARENT`` on ``JOB_COMPLETED``. This preserves
    error-log delivery for launch/config/bootstrap failures where the job
    subprocess never reaches ``START_RUN`` and therefore never loads the
    injected ``JobLogStreamer``.

    The server side must have a
    :class:`~nvflare.app_common.logging.job_log_receiver.JobLogReceiver`
    in its ``resources.json`` (or job config) to receive and store the stream.

    Args:
        log_file_name: base name of the log file to stream.  Defaults to
            ``WorkspaceConstants.LOG_FILE_NAME`` (``"log.txt"``).
        liveness_interval: seconds between heartbeat messages when no new log
            bytes have been written (default 10.0).  Must be strictly less than
            the receiver's ``idle_timeout``.
        poll_interval: seconds between polls when no new data has been written
            to the log (default 0.5).
    """

    def __init__(
        self,
        log_file_name: str = WorkspaceConstants.LOG_FILE_NAME,
        liveness_interval: float = 10.0,
        poll_interval: float = 0.5,
    ):
        super().__init__()
        self._log_file_name = log_file_name
        self._liveness_interval = liveness_interval
        self._poll_interval = poll_interval
        self.register_event_handler(EventType.BEFORE_JOB_LAUNCH, self._on_before_job_launch)
        self.register_event_handler(EventType.JOB_COMPLETED, self._on_job_completed)

    def _on_before_job_launch(self, event_type: str, fl_ctx: FLContext):
        pass

    def _stream_completed_log(self, fl_ctx: FLContext, log_path: str, client_name: str, job_id: str):
        pass

    def _on_job_completed(self, event_type: str, fl_ctx: FLContext):
        pass
