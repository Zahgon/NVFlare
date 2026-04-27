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
import tempfile
import uuid
from typing import List, Tuple

from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReturnCode, Shareable, make_reply
from nvflare.apis.streaming import ConsumerFactory, ObjectConsumer, StreamableEngine, StreamContext
from nvflare.fuel.utils.validation_utils import check_positive_int, check_positive_number

from .streamer_base import (  # noqa: F401
    KEY_DATA,
    KEY_DATA_SIZE,
    KEY_EOF,
    KEY_FILE_LOCATION,
    KEY_FILE_NAME,
    KEY_FILE_SIZE,
    BaseChunkConsumer,
    BaseChunkProducer,
    StreamerBase,
)


class _ChunkConsumer(BaseChunkConsumer):
    def __init__(self, stream_ctx: StreamContext, dest_dir):
        super().__init__()
        self.file_name = stream_ctx.get(KEY_FILE_NAME)
        self.dest_dir = dest_dir
        self.file_size = stream_ctx.get(KEY_FILE_SIZE)
        self.received_size = 0
        file_path = os.path.join(dest_dir, str(uuid.uuid4()))
        self.file = open(file_path, "wb")
        stream_ctx[KEY_FILE_LOCATION] = file_path

    def consume(
        self,
        shareable: Shareable,
        stream_ctx: StreamContext,
        fl_ctx: FLContext,
    ) -> Tuple[bool, Shareable]:
        pass

    def finalize(self, stream_ctx: StreamContext, fl_ctx: FLContext):
        pass


class _ChunkConsumerFactory(ConsumerFactory):
    def __init__(self, dest_dir: str):
        self.dest_dir = dest_dir

    def get_consumer(self, stream_ctx: StreamContext, fl_ctx: FLContext) -> ObjectConsumer:
        pass


class _ChunkProducer(BaseChunkProducer):
    def __init__(self, file, chunk_size, timeout):
        super().__init__()
        self.file = file
        self.chunk_size = chunk_size
        self.timeout = timeout

    def produce(
        self,
        stream_ctx: StreamContext,
        fl_ctx: FLContext,
    ) -> Tuple[Shareable, float]:
        pass


class FileStreamer(StreamerBase):
    @staticmethod
    def register_stream_processing(
        fl_ctx: FLContext,
        channel: str,
        topic: str,
        dest_dir: str = None,
        stream_done_cb=None,
        chunk_consumed_cb=None,
        **cb_kwargs,
    ):
        """Register for stream processing on the receiving side.

        Args:
            fl_ctx: the FLContext object
            channel: the app channel
            topic: the app topic
            dest_dir: the destination dir for received file. If not specified, system temp dir is used
            stream_done_cb: if specified, the callback to be called when the file is completely received
            chunk_consumed_cb: if specified, the callback to be called when a chunk is processed
            **cb_kwargs: the kwargs for the stream_done_cb

        Returns: None

        Notes: the stream_done_cb must follow stream_done_cb_signature as defined in apis.streaming.

        """
        pass

    @staticmethod
    def stream_file(
        channel: str,
        topic: str,
        stream_ctx: StreamContext,
        targets: List[str],
        file_name: str,
        fl_ctx: FLContext,
        chunk_size=None,
        chunk_timeout=None,
        optional=False,
        secure=False,
    ) -> (str, bool):
        """Stream a file to one or more targets.

        Args:
            channel: the app channel
            topic: the app topic
            stream_ctx: context data of the stream
            targets: targets that the file will be sent to
            file_name: full path to the file to be streamed
            fl_ctx: a FLContext object
            chunk_size: size of each chunk to be streamed. If not specified, default to 1M bytes.
            chunk_timeout: timeout for each chunk of data sent to targets.
            optional: whether the file is optional
            secure: whether P2P security is required

        Returns: a tuple of (RC, Result):
            - RC is ReturnCode.OK or ReturnCode.ERROR;
            - Result is whether the streaming completed successfully

        Notes: this is a blocking call - only returns after the streaming is done.
        """
        pass

    @staticmethod
    def get_file_name(stream_ctx: StreamContext):
        """Get the file base name property from stream context.
        This method is intended to be used by the stream_done_cb() function of the receiving side.

        Args:
            stream_ctx: the stream context

        Returns: file base name

        """
        pass

    @staticmethod
    def get_file_location(stream_ctx: StreamContext):
        """Get the file location property from stream context.
        This method is intended to be used by the stream_done_cb() function of the receiving side.

        Args:
            stream_ctx: the stream context

        Returns: location (full file path) of the received file

        """
        pass

    @staticmethod
    def get_file_size(stream_ctx: StreamContext):
        """Get the file size property from stream context.
        This method is intended to be used by the stream_done_cb() function of the receiving side.

        Args:
            stream_ctx: the stream context

        Returns: size (in bytes) of the received file

        """
        pass
