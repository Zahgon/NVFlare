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
from typing import Callable, Optional

from nvflare.fuel.f3.comm_config import CommConfigurator
from nvflare.fuel.f3.connection import BytesAlike
from nvflare.fuel.f3.message import Message
from nvflare.fuel.f3.streaming.byte_receiver import ByteReceiver
from nvflare.fuel.f3.streaming.byte_streamer import STREAM_CHUNK_SIZE, STREAM_TYPE_BLOB, ByteStreamer
from nvflare.fuel.f3.streaming.stream_const import EOS
from nvflare.fuel.f3.streaming.stream_types import Stream, StreamError, StreamFuture
from nvflare.fuel.f3.streaming.stream_utils import FastBuffer, callback_thread_pool, stream_thread_pool, wrap_view
from nvflare.fuel.utils.buffer_list import BufferList
from nvflare.security.logging import secure_format_traceback

log = logging.getLogger(__name__)


class BlobStream(Stream):
    def __init__(self, blob: BytesAlike, headers: Optional[dict]):
        size = self.buffer_len(blob)
        super().__init__(size, headers)

        if not isinstance(blob, list):
            self.blob_view = wrap_view(blob)
            self.buffer_list = None
        else:
            self.blob_view = [wrap_view(b) for b in blob]
            self.buffer_list = BufferList(self.blob_view)

    def read(self, chunk_size: int) -> BytesAlike:

        pass

    @staticmethod
    def buffer_len(buffer: BytesAlike):
        pass


class BlobTask:
    def __init__(self, future: StreamFuture, stream: Stream):
        self.future = future
        self.stream = stream
        self.size = stream.get_size()
        self.pre_allocated = self.size > 0

        if self.pre_allocated:
            self.buffer = wrap_view(bytearray(self.size))
        else:
            self.buffer = FastBuffer()

    def __str__(self):
        return f"Blob[SID:{self.future.get_stream_id()} Size：{self.size}]"


class BlobHandler:
    def __init__(self, blob_cb: Callable):
        self.blob_cb = blob_cb
        self.chunk_size = CommConfigurator().get_streaming_chunk_size(STREAM_CHUNK_SIZE)

    def handle_blob_cb(self, future: StreamFuture, stream: Stream, resume: bool, *args, **kwargs) -> int:

        pass

    def _run_blob_cb(self, future: StreamFuture, stream: Stream, args: tuple, kwargs: dict):
        """Run blob_cb on the callback pool; preserve exception handling (log + task.stop) as in ByteReceiver."""
        pass

    def _read_stream(self, blob_task: BlobTask):

        pass


class BlobStreamer:
    def __init__(self, byte_streamer: ByteStreamer, byte_receiver: ByteReceiver):
        self.byte_streamer = byte_streamer
        self.byte_receiver = byte_receiver

    def send(
        self, channel: str, topic: str, target: str, message: Message, secure: bool, optional: bool
    ) -> StreamFuture:
        pass

    def register_blob_callback(self, channel, topic, blob_cb: Callable, *args, **kwargs):
        pass
