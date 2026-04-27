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
from collections import deque
from typing import Callable, Deque, Dict, Optional, Tuple

from nvflare.fuel.f3.cellnet.core_cell import CoreCell
from nvflare.fuel.f3.cellnet.defs import MessageHeaderKey
from nvflare.fuel.f3.cellnet.registry import Callback, Registry
from nvflare.fuel.f3.comm_config import CommConfigurator
from nvflare.fuel.f3.connection import BytesAlike
from nvflare.fuel.f3.message import Message
from nvflare.fuel.f3.stats_pool import StatsPoolManager
from nvflare.fuel.f3.streaming.stream_const import (
    EOS,
    STREAM_ACK_TOPIC,
    STREAM_CHANNEL,
    STREAM_DATA_TOPIC,
    StreamDataType,
    StreamHeaderKey,
)
from nvflare.fuel.f3.streaming.stream_types import Stream, StreamError, StreamFuture
from nvflare.fuel.f3.streaming.stream_utils import ONE_MB, stream_stats_category, stream_thread_pool

log = logging.getLogger(__name__)

MAX_OUT_SEQ_CHUNKS = 16
# 1/4 of the window size
ACK_INTERVAL = 1024 * 1024 * 4
READ_TIMEOUT = 300
COUNTER_NAME_RECEIVED = "received"

# Read result status
RESULT_DATA = 0
RESULT_NO_DATA = 1
RESULT_EOS = 2


class RxTask:
    """Receiving task for ByteStream"""

    rx_task_map: Dict[Tuple[str, int], "RxTask"] = {}
    map_lock = threading.Lock()

    def __init__(self, sid: int, origin: str, cell: CoreCell):
        self.sid = sid
        self.origin = origin
        self.cell = cell

        self.channel = None
        self.topic = None
        self.headers = None
        self.size = 0

        # The reassembled chunks in a double-ended queue
        self.chunks: Deque[Tuple[bool, BytesAlike]] = deque()
        self.chunk_offset = 0  # Start of the remaining data for partially read left-most chunk

        # Out-of-sequence chunks to be assembled
        self.out_seq_chunks: Dict[int, Tuple[bool, BytesAlike]] = {}
        self.stream_future = None
        self.next_seq = 0
        self.offset = 0
        self.offset_ack = 0
        self.waiter = threading.Event()
        self.lock = threading.Lock()
        self.eos = False
        self.last_chunk_received = False

        self.timeout = CommConfigurator().get_streaming_read_timeout(READ_TIMEOUT)
        self.ack_interval = CommConfigurator().get_streaming_ack_interval(ACK_INTERVAL)
        self.max_out_seq = CommConfigurator().get_streaming_max_out_seq_chunks(MAX_OUT_SEQ_CHUNKS)

    def __str__(self):
        return f"Rx[SID:{self.sid} from {self.origin} for {self.channel}/{self.topic} Size: {self.size}]"

    @classmethod
    def find_or_create_task(cls, message: Message, cell: CoreCell) -> Optional["RxTask"]:

        pass

    def read(self, size: int) -> BytesAlike:

        pass

    def process_chunk(self, message: Message) -> bool:
        """Returns True if a new stream is created"""
        pass

    def _handle_new_stream(self, message: Message):
        pass

    def _handle_incoming_data(self, seq: int, message: Message):

        pass

    def stop(self, error: StreamError = None, notify=True):

        pass

    def _try_to_read(self, size: int) -> Tuple[int, Optional[BytesAlike]]:

        pass

    def _append(self, buf: Tuple[bool, BytesAlike]):
        pass


class RxStream(Stream):
    """A stream that's used to read streams from the streaming task"""

    def __init__(self, task: RxTask):
        super().__init__(task.size, task.headers)
        self.task = task

    def read(self, size: int) -> bytes:
        pass

    def close(self):
        pass


class ByteReceiver:

    received_stream_counter_pool = StatsPoolManager.add_counter_pool(
        name="Received_Stream_Counters",
        description="Counters of received streams",
        counter_names=[COUNTER_NAME_RECEIVED],
    )

    received_stream_size_pool = StatsPoolManager.add_msg_size_pool(
        "Received_Stream_Sizes", "Sizes of streams received (MBs)"
    )

    def __init__(self, cell: CoreCell):
        self.cell = cell
        self.cell.register_request_cb(channel=STREAM_CHANNEL, topic=STREAM_DATA_TOPIC, cb=self._data_handler)
        self.registry = Registry()

    def register_callback(self, channel: str, topic: str, stream_cb: Callable, *args, **kwargs):
        pass

    def _data_handler(self, message: Message):

        pass

    @staticmethod
    def _callback_wrapper(task: RxTask, callback: Callback):
        """A wrapper to catch all exceptions in the callback"""
        pass
