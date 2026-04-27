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

from typing import Any, Dict, List, Tuple

from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReturnCode, Shareable, make_reply
from nvflare.apis.streaming import ConsumerFactory, ObjectConsumer, ObjectProducer, StreamableEngine, StreamContext
from nvflare.app_common.streamers.streamer_base import StreamerBase
from nvflare.fuel.utils.class_loader import get_class_name, load_class
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.fuel.utils.validation_utils import check_positive_number

_PREFIX = "ContainerStreamer."

# Keys for StreamCtx
_CTX_TYPE = _PREFIX + "type"
_CTX_SIZE = _PREFIX + "size"
_CTX_RESULT = _PREFIX + "result"

# Keys for Shareable
_KEY_ENTRY = _PREFIX + "entry"
_KEY_LAST = _PREFIX + "last"


class _EntryConsumer(ObjectConsumer):
    def __init__(self, stream_ctx: StreamContext):
        self.logger = get_obj_logger(self)
        container_type = stream_ctx.get(_CTX_TYPE)
        container_class = load_class(container_type)
        self.container = container_class()
        self.size = stream_ctx.get(_CTX_SIZE)

    def consume(
        self,
        shareable: Shareable,
        stream_ctx: StreamContext,
        fl_ctx: FLContext,
    ) -> Tuple[bool, Shareable]:

        pass

    def finalize(self, stream_ctx: StreamContext, fl_ctx: FLContext):
        pass


class _EntryConsumerFactory(ConsumerFactory):
    def get_consumer(self, stream_ctx: StreamContext, fl_ctx: FLContext) -> ObjectConsumer:
        pass


class _EntryProducer(ObjectProducer):
    def __init__(self, container, entry_timeout):
        self.logger = get_obj_logger(self)
        if not container:
            error = "Can't stream empty container"
            self.logger.error(error)
            raise ValueError(error)

        self.container = container
        if isinstance(container, dict):
            self.iterator = iter(container.items())
        else:
            self.iterator = iter(container)
        self.size = len(container)
        self.count = 0
        self.last = False
        self.entry_timeout = entry_timeout

    def produce(
        self,
        stream_ctx: StreamContext,
        fl_ctx: FLContext,
    ) -> Tuple[Shareable, float]:

        pass

    def process_replies(
        self,
        replies: Dict[str, Shareable],
        stream_ctx: StreamContext,
        fl_ctx: FLContext,
    ) -> Any:
        pass


class ContainerStreamer(StreamerBase):
    @staticmethod
    def register_stream_processing(
        fl_ctx: FLContext,
        channel: str,
        topic: str,
        stream_done_cb=None,
        **cb_kwargs,
    ):
        """Register for stream processing on the receiving side.

        Args:
            fl_ctx: the FLContext object
            channel: the app channel
            topic: the app topic
            stream_done_cb: if specified, the callback to be called when the file is completely received
            **cb_kwargs: the kwargs for the stream_done_cb

        Returns: None

        Notes: the stream_done_cb must follow stream_done_cb_signature as defined in apis.streaming.

        """
        pass

    @staticmethod
    def stream_container(
        channel: str,
        topic: str,
        stream_ctx: StreamContext,
        targets: List[str],
        container: Any,
        fl_ctx: FLContext,
        entry_timeout=None,
        optional=False,
        secure=False,
    ) -> bool:
        """Stream a file to one or more targets.

        Args:
            channel: the app channel
            topic: the app topic
            stream_ctx: context data of the stream
            targets: targets that the file will be sent to
            container: container to be streamed
            fl_ctx: a FLContext object
            entry_timeout: timeout for each entry sent to targets.
            optional: whether the file is optional
            secure: whether P2P security is required

        Returns: whether the streaming completed successfully

        Notes: this is a blocking call - only returns after the streaming is done.
        """
        pass

    @staticmethod
    def get_result(stream_ctx: StreamContext) -> Any:
        """Get the received container
        This method is intended to be used by the stream_done_cb() function of the receiving side.

        Args:
            stream_ctx: the stream context

        Returns: The received container

        """
        pass
