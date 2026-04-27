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
"""
LogStreamer — live-tailing streamer for growing log files
=========================================================

LogStreamer differs from FileStreamer in three fundamental ways:

1. **Growing file (live tail)**
   FileStreamer treats a file as a static snapshot: it opens the file, reads
   it to the end, and sends EOF.  LogStreamer instead *tails* the file — it
   keeps reading as new bytes are appended, blocking between polls until the
   caller sets ``stop_event`` and all buffered bytes have been flushed.  It
   also survives log rotation: when the inode changes (or the file shrinks
   below the current read position) it closes the stale handle and reopens
   the file at the new path from the beginning.

2. **Dead-sender detection via liveness heartbeats**
   Because the stream may be idle for extended periods (no new log lines),
   the receiver cannot distinguish "nothing to send yet" from "sender has
   crashed".  LogStreamer solves this with periodic *heartbeat* messages: if
   no data chunk has been sent for ``liveness_interval`` seconds the producer
   emits a zero-payload heartbeat.  The consumer resets its idle clock on
   every message — data or heartbeat — so the idle timer only counts genuine
   silence on the network.

3. **Automatic stream closure on idle timeout**
   The receiver runs a background watchdog thread.  If no message of any
   kind (data or heartbeat) arrives for ``idle_timeout`` seconds the watchdog
   concludes the sender is unreachable, closes the stream via the engine's
   ``END_STREAM`` hook, and fires ``stream_done_cb`` with
   ``StreamContextKey.RC = ReturnCode.TIMEOUT``.  To avoid spurious timeouts,
   ``liveness_interval`` must be strictly less than ``idle_timeout``.  This
   can be validated only when the caller knows both values; otherwise ensure
   they are consistent at deployment.

Relationship between the two parameters
----------------------------------------
- ``liveness_interval``: how often the *sender* emits a heartbeat when idle
- ``idle_timeout``: how long the *receiver* waits before declaring the sender dead

Rule: ``liveness_interval < idle_timeout``.  With the defaults (10 s and
30 s) a healthy sender heartbeats every 10 s, so the receiver's 30 s timer
is always reset well before it fires.
"""
import os
import threading
import time
from typing import List, Tuple

from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReturnCode, Shareable, make_reply
from nvflare.apis.streaming import ConsumerFactory, ObjectConsumer, StreamableEngine, StreamContext, StreamContextKey
from nvflare.fuel.utils.validation_utils import check_non_negative_number, check_positive_int, check_positive_number

from .streamer_base import (  # noqa: F401
    KEY_DATA,
    KEY_DATA_SIZE,
    KEY_EOF,
    KEY_FILE_NAME,
    KEY_HEARTBEAT,
    KEY_STREAM_DONE_CB,
    BaseChunkConsumer,
    BaseChunkProducer,
    StreamerBase,
)


def _make_once(fn):
    """Return a thread-safe wrapper that calls *fn* at most once across all callers.

    Used so that ``stream_done_cb`` is executed exactly once regardless of whether
    the idle-timeout watchdog or the normal engine completion path fires first.
    """
    def wrapper(*args, **kwargs):
        pass
    pass


class _LogChunkConsumer(BaseChunkConsumer):
    def __init__(
        self,
        stream_ctx: StreamContext,
        chunk_received_cb,
        idle_timeout: float,
        cb_kwargs: dict,
        fl_ctx: FLContext = None,
    ):
        super().__init__()
        self._chunk_received_cb = chunk_received_cb
        self._idle_timeout = idle_timeout
        self._cb_kwargs = cb_kwargs
        self._stream_ctx = stream_ctx
        self._fl_ctx = fl_ctx  # updated on each consume(); seeded from get_consumer()
        self._last_received_time = time.time()
        self._done = threading.Event()

        if idle_timeout > 0:
            t = threading.Thread(target=self._watchdog, daemon=True)
            t.start()

    def _watchdog(self):
        """Background thread: end this stream when it goes idle."""
        pass

    def consume(
        self,
        shareable: Shareable,
        stream_ctx: StreamContext,
        fl_ctx: FLContext,
    ) -> Tuple[bool, Shareable]:
        pass

    def finalize(self, stream_ctx: StreamContext, fl_ctx: FLContext):
        # Stop the watchdog — the stream ended normally via EOF or engine abort.
        pass


class LogChunkConsumerFactory(ConsumerFactory):
    def __init__(self, chunk_received_cb, idle_timeout: float, stream_done_cb, cb_kwargs: dict):
        self._chunk_received_cb = chunk_received_cb
        self._idle_timeout = idle_timeout
        self._stream_done_cb = stream_done_cb
        self._cb_kwargs = cb_kwargs

    def get_consumer(self, stream_ctx: StreamContext, fl_ctx: FLContext) -> ObjectConsumer:
        pass


def dispatch_stream_done(stream_ctx: StreamContext, fl_ctx: FLContext, **kwargs):
    pass


class _LogTailProducer(BaseChunkProducer):
    def __init__(
        self,
        file_name: str,
        chunk_size: int,
        chunk_timeout: float,
        poll_interval: float,
        stop_event: threading.Event,
        liveness_interval: float,
    ):
        super().__init__()
        self.file_name = file_name
        self.chunk_size = chunk_size
        self.chunk_timeout = chunk_timeout
        self.poll_interval = poll_interval
        self.stop_event = stop_event
        self._liveness_interval = liveness_interval
        self._last_send_time = time.time()
        self.file = None
        self.inode = None
        self._draining = False  # True while doing the post-stop drain retry
        self._open_file()

    def _open_file(self):
        pass

    def _check_rotation(self) -> bool:
        """Return True if the log file has been rotated (inode change or truncation)."""
        pass

    def produce(
        self,
        stream_ctx: StreamContext,
        fl_ctx: FLContext,
    ) -> Tuple[Shareable, float]:
        pass

    def close(self):
        pass


class LogStreamer(StreamerBase):
    @staticmethod
    def register_stream_processing(
        fl_ctx: FLContext,
        channel: str,
        topic: str,
        chunk_received_cb=None,
        stream_done_cb=None,
        idle_timeout: float = 30.0,
        **cb_kwargs,
    ):
        """Register for live log stream processing on the receiving side.

        Args:
            fl_ctx: the FLContext object
            channel: the app channel
            topic: the app topic
            chunk_received_cb: called for each received data chunk (heartbeats are
                silently absorbed and never forwarded):
                ``chunk_received_cb(data: bytes, stream_ctx: StreamContext, fl_ctx: FLContext, **cb_kwargs)``
            stream_done_cb: called when the stream ends (normal EOF, engine abort, or
                idle timeout); follows ``stream_done_cb_signature`` in
                ``nvflare.apis.streaming``.  The ``stream_ctx`` passed to this callback
                will contain ``StreamContextKey.RC = ReturnCode.TIMEOUT`` when the call
                is triggered by the idle-timeout watchdog.
            idle_timeout: seconds without any message (data or heartbeat) before the
                receiver declares the sender dead and closes the stream (default 30.0).
                Set to 0 to disable.
            **cb_kwargs: kwargs forwarded to both callbacks

        Returns: None

        Notes:
            ``stream_done_cb`` is guaranteed to be called at most once per stream even
            when both the idle-timeout path and the normal engine completion path race.
        """
        pass

    @staticmethod
    def stream_log(
        channel: str,
        topic: str,
        stream_ctx: StreamContext,
        targets: List[str],
        file_name: str,
        fl_ctx: FLContext,
        stop_event: threading.Event = None,
        poll_interval: float = 0.5,
        liveness_interval: float = 10.0,
        idle_timeout: float = None,
        chunk_size: int = None,
        chunk_timeout: float = None,
        optional: bool = False,
        secure: bool = False,
    ):
        """Tail and stream a live log file to one or more targets.

        Continuously reads new data appended to *file_name* (including across log
        rotations) and streams it to *targets*.  Blocks until *stop_event* is set
        **and** all buffered data has been flushed, or until the run is aborted.

        **Log rotation** is detected by comparing the file's inode after each poll.
        When a rotation is found the old file handle is closed and the new file is
        opened from the beginning.  Truncation (size decreased below the current read
        position) is treated the same way.

        **Liveness heartbeats** — when no new data has been sent for *liveness_interval*
        seconds a lightweight heartbeat message (no payload) is sent to each target.
        This lets the receiver distinguish "log is quiet" from "sender process died".
        The receiver's idle-timeout clock is reset on every message, including
        heartbeats, so the timeout only fires when the sender is genuinely unreachable.

        If the file does not exist when ``stream_log`` is called the producer waits,
        polling every *poll_interval* seconds until it appears.

        Args:
            channel: the app channel
            topic: the app topic
            stream_ctx: context data for this stream
            targets: receiving site names
            file_name: full path of the log file to tail
            fl_ctx: a FLContext object
            stop_event: a :class:`threading.Event` used to signal the streamer to
                finish.  When set, the streamer drains any remaining unread bytes and
                then sends EOF.  If *None* a new Event is created; the only way to stop
                in that case is via the run abort signal.
            poll_interval: seconds to wait between polls when no new data is available
                (default 0.5)
            liveness_interval: seconds of log silence before sending a heartbeat to
                receivers (default 10.0)
            idle_timeout: optional receiver idle-timeout value used only for local
                validation. When provided and greater than zero,
                ``liveness_interval`` must be strictly less than ``idle_timeout``.
            chunk_size: bytes per chunk; defaults to 64 KB
            chunk_timeout: per-chunk send timeout in seconds; defaults to 5.0
            optional: whether the stream is optional
            secure: whether P2P security is required

        Returns: result from ``engine.stream_objects`` — same shape as
            :meth:`FileStreamer.stream_file`
        """
        pass

    @staticmethod
    def get_file_name(stream_ctx: StreamContext):
        """Get the source log file's base name from the stream context.

        Intended for use inside ``chunk_received_cb`` or ``stream_done_cb`` on the
        receiving side.

        Args:
            stream_ctx: the stream context

        Returns: file base name string, or None
        """
        pass
