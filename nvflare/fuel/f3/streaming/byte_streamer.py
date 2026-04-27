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
import logging
import threading
import time
from typing import Callable, Optional

from nvflare.fuel.f3.cellnet.core_cell import CoreCell
from nvflare.fuel.f3.cellnet.defs import MessageHeaderKey
from nvflare.fuel.f3.comm_config import CommConfigurator
from nvflare.fuel.f3.message import Message
from nvflare.fuel.f3.stats_pool import StatsPoolManager
from nvflare.fuel.f3.streaming.stream_const import (
    STREAM_ACK_TOPIC,
    STREAM_CHANNEL,
    STREAM_DATA_TOPIC,
    StreamDataType,
    StreamHeaderKey,
)
from nvflare.fuel.f3.streaming.stream_types import Stream, StreamError, StreamFuture, StreamTaskSpec
from nvflare.fuel.f3.streaming.stream_utils import (
    ONE_MB,
    gen_stream_id,
    stream_stats_category,
    stream_thread_pool,
    wrap_view,
)

STREAM_CHUNK_SIZE = 1024 * 1024
STREAM_WINDOW_SIZE = 16 * STREAM_CHUNK_SIZE
STREAM_ACK_WAIT = 300

STREAM_TYPE_BYTE = "byte"
STREAM_TYPE_BLOB = "blob"
STREAM_TYPE_FILE = "file"

COUNTER_NAME_SENT = "sent"

log = logging.getLogger(__name__)


class TxTask(StreamTaskSpec):
    def __init__(
        self,
        cell: CoreCell,
        chunk_size: int,
        channel: str,
        topic: str,
        target: str,
        headers: dict,
        stream: Stream,
        secure: bool,
        optional: bool,
    ):
        self.cell = cell
        self.chunk_size = chunk_size
        self.sid = gen_stream_id()
        self.buffer = wrap_view(bytearray(chunk_size))
        # Optimization to send the original buffer without copying
        self.direct_buf: Optional[bytes] = None
        self.buffer_size = 0
        self.channel = channel
        self.topic = topic
        self.target = target
        self.headers = headers
        self.stream = stream
        self.stream_future = None
        self.task_future = None
        self.ack_waiter = threading.Event()
        self.seq = 0
        self.offset = 0
        self.offset_ack = 0
        self.secure = secure
        self.optional = optional
        self.stopped = False

        self.stream_future = StreamFuture(self.sid, task_handle=self)
        self.stream_future.set_size(stream.get_size())

        config = CommConfigurator()
        self.window_size = config.get_streaming_window_size(STREAM_WINDOW_SIZE)
        self.ack_wait = config.get_streaming_ack_wait(STREAM_ACK_WAIT)
        self.ack_progress_timeout = config.get_streaming_ack_progress_timeout(60.0)
        # Guard against zero/negative config to avoid wait(0) busy-spin loops.
        self.ack_progress_check_interval = max(0.01, config.get_streaming_ack_progress_check_interval(5.0))
        self.last_ack_progress_ts = time.monotonic()

    def __str__(self):
        return f"Tx[SID:{self.sid} to {self.target} for {self.channel}/{self.topic}]"

    def send_loop(self):
        """Read/send loop to transmit the whole stream with flow control"""
        pass

    def send_pending_buffer(self, final=False):

        pass

    def stop(self, error: Optional[StreamError] = None, notify=True):

        pass

    def handle_ack(self, message: Message):

        pass

    def start_task_thread(self, task_handler: Callable):
        pass

    def cancel(self):
        pass


class ByteStreamer:

    tx_task_map = {}
    map_lock = threading.Lock()

    sent_stream_counter_pool = StatsPoolManager.add_counter_pool(
        name="Sent_Stream_Counters",
        description="Counters of sent streams",
        counter_names=[COUNTER_NAME_SENT],
    )

    sent_stream_size_pool = StatsPoolManager.add_msg_size_pool("Sent_Stream_Sizes", "Sizes of streams sent (MBs)")

    def __init__(self, cell: CoreCell):
        self.cell = cell
        self.cell.register_request_cb(channel=STREAM_CHANNEL, topic=STREAM_ACK_TOPIC, cb=self._ack_handler)
        self.chunk_size = CommConfigurator().get_streaming_chunk_size(STREAM_CHUNK_SIZE)

    def get_chunk_size(self):
        pass

    def send(
        self,
        channel: str,
        topic: str,
        target: str,
        headers: dict,
        stream: Stream,
        stream_type=STREAM_TYPE_BYTE,
        secure=False,
        optional=False,
    ) -> StreamFuture:
        pass

    @staticmethod
    def _transmit_task(task: TxTask):

        pass

    @staticmethod
    def _ack_handler(message: Message):

        pass
