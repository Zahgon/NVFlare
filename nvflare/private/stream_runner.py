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
import time
import uuid
from concurrent.futures import Future, ThreadPoolExecutor
from threading import Lock
from typing import Any, List, Tuple

from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.apis.streaming import ConsumerFactory, ObjectConsumer, ObjectProducer, StreamContext, StreamContextKey
from nvflare.fuel.f3.cellnet.registry import Registry
from nvflare.fuel.utils.config_service import ConfigService
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.fuel.utils.validation_utils import check_callable, check_object_type, check_str
from nvflare.private.aux_runner import AuxMsgTarget, AuxRunner
from nvflare.security.logging import secure_format_exception

# Topics for streaming messages
PREFIX = "ObjectStreamer."
TOPIC_STREAM_REQUEST = PREFIX + "Request"
TOPIC_STREAM_ABORT = PREFIX + "Abort"


class HeaderKey:
    TX_ID = PREFIX + "TX_ID"
    SEQ = PREFIX + "SEQ"
    TOPIC = PREFIX + "TOPIC"
    CHANNEL = PREFIX + "CHANNEL"
    CTX = PREFIX + "CTX"
    END_RESULT = PREFIX + "END_RESULT"


class _ConsumerInfo:
    def __init__(
        self,
        logger,
        stream_ctx: StreamContext,
        factory: ConsumerFactory,
        consumer: ObjectConsumer,
        stream_done_cb,
        consumed_cb,
        cb_kwargs,
    ):
        self.logger = logger
        self.factory = factory
        self.stream_ctx = stream_ctx
        self.consumer = consumer
        self.consumed_cb = consumed_cb
        self.stream_done_cb = stream_done_cb
        self.cb_kwargs = cb_kwargs
        self.stream_start_time = time.time()
        self.last_msg_start_time = None
        self.last_msg_end_time = None

    def process(
        self,
        msg: Shareable,
        fl_ctx: FLContext,
    ):
        pass

    def stream_done(self, rc: str, fl_ctx: FLContext):
        pass


class ObjectStreamer(FLComponent):
    def __init__(self, aux_runner: AuxRunner):
        FLComponent.__init__(self)
        self.aux_runner = aux_runner
        self.registry = Registry()
        self.tx_lock = Lock()
        self.tx_table = {}  # tx_id => _ProcessorInfo
        self.logger = get_obj_logger(self)

        # Note: the ConfigService has been initialized
        max_concurrent_streaming_sessions = ConfigService.get_int_var("max_concurrent_streaming_sessions", default=20)
        self.streaming_executor = ThreadPoolExecutor(max_workers=max_concurrent_streaming_sessions)

        aux_runner.register_aux_message_handler(
            topic=TOPIC_STREAM_REQUEST,
            message_handle_func=self._handle_request,
        )
        aux_runner.register_aux_message_handler(
            topic=TOPIC_STREAM_ABORT,
            message_handle_func=self._handle_abort,
        )

    def shutdown(self):
        pass

    def register_stream_processing(
        self,
        channel: str,
        topic: str,
        factory: ConsumerFactory,
        stream_done_cb=None,
        consumed_cb=None,
        **cb_kwargs,
    ):
        """Register a ConsumerFactory for specified app channel and topic.
        Once a new streaming request is received for the channel/topic, the registered factory will be used
        to create a new ObjectConsumer object to handle the stream.

        Note: the factory should generate a new ObjectConsumer every time get_consumer() is called. This is because
        multiple streaming sessions could be going on at the same time. Each streaming session should have its
        own ObjectConsumer.

        Args:
            channel: app channel
            topic: app topic
            factory: the factory to be registered
            consumed_cb: the CB is called after a chunk is consumed
            stream_done_cb: the CB to be called when a stream is done

        Returns: None

        """
        pass

    @staticmethod
    def _log_msg(req: Shareable, msg: str):
        pass

    def error(self, req: Shareable, msg: str):
        pass

    def info(self, req: Shareable, msg: str):
        pass

    def debug(self, req: Shareable, msg: str):
        pass

    def _end_tx(self, tx_id: str, rc: str, fl_ctx: FLContext):
        pass

    def _handle_abort(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def _handle_request(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def _notify_abort_streaming(
        self,
        targets: List[AuxMsgTarget],
        tx_id: str,
        secure: bool,
        fl_ctx: FLContext,
    ):
        """Notify all targets to stop streaming processing in case they are still waiting.

        Args:
            targets:
            tx_id:
            fl_ctx:
            secure:

        Returns:

        """
        pass

    def stream(
        self,
        channel: str,
        topic: str,
        stream_ctx: StreamContext,
        targets: List[AuxMsgTarget],
        producer: ObjectProducer,
        fl_ctx: FLContext,
        secure=False,
        optional=False,
    ) -> Tuple[str, Any]:
        pass

    def stream_no_wait(
        self,
        channel: str,
        topic: str,
        stream_ctx: StreamContext,
        targets: List[AuxMsgTarget],
        producer: ObjectProducer,
        fl_ctx: FLContext,
        secure=False,
        optional=False,
    ) -> Future:
        pass
