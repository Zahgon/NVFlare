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
import threading
import time
import uuid
from abc import ABC, abstractmethod
from typing import Any

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReturnCode, Shareable, make_reply
from nvflare.apis.streaming import StreamContext
from nvflare.security.logging import secure_format_exception

RETRIEVER_TX_ID = "_rtr_tx_id_"

_SHORT_WAIT = 0.1


class _Waiter(threading.Event):
    def __init__(self):
        super().__init__()
        self.result = None

    def set_result(self, rc: str, data: Any):
        pass


class ObjectRetriever(FLComponent, ABC):
    """This is the base class for object retrieval with streaming. The retrieval works as follows:
    - The requesting site initiates the process by sending a data request to the site that has the data;
    - The requesting site then waits for the data to be completely received;
    - Once the data request is received, the data owner site streams the data to the requesting site;
    - During the streaming process, the requesting site keeps checking for the completion of the streaming until
    either the data is completely received, or timed out, or aborted.
    """

    def __init__(
        self,
        topic: str = None,
    ):
        FLComponent.__init__(self)
        class_name = self.__class__.__name__
        if not topic:
            topic = class_name
        self.topic = topic
        self.stream_channel = class_name
        self.tx_table = {}

    @abstractmethod
    def register_stream_processing(
        self,
        channel: str,
        topic: str,
        fl_ctx: FLContext,
        stream_done_cb,
        **cb_kwargs,
    ):
        """Object requester side, which will receive data stream.
        This is called to register the status_cb for received stream.

        Args:
            channel: stream channel
            topic: stream topic
            fl_ctx: FLContext object
            stream_done_cb: the stream_done callback to be registered
            **cb_kwargs: kwargs to be passed to the CB

        Returns:

        """
        pass

    @abstractmethod
    def validate_request(self, request: Shareable, fl_ctx: FLContext) -> (str, Any):
        """Object sending side. Called to validate the received retrieval request.

        Args:
            request: the request to be validated
            fl_ctx: FLContext object

        Returns: tuple of (ReturnCode, Validation Data)
        This method should do as much as possible so that the do_stream method won't be called if any error
        is detected (the do_stream method is called in a separate thread).
        The validation data produced by this method will be passed to the do_stream method.

        """
        pass

    @abstractmethod
    def do_stream(
        self,
        target: str,
        request: Shareable,
        fl_ctx: FLContext,
        stream_ctx: StreamContext,
        validation_data: Any,
    ) -> Any:
        """Object sending side. Called to stream data to the requesting side.

        Args:
            target: the requesting site to stream to
            request: the object retrieval request
            fl_ctx: a FLContext object
            stream_ctx: stream context data
            validation_data: the validation data produced by the validate_request method.

        Returns: Any object

        """
        pass

    @abstractmethod
    def get_result(self, stream_ctx: StreamContext) -> (str, Any):
        """Object requesting side, which is also the stream receiving side.
        Called to get the result of the streaming.

        Args:
            stream_ctx: StreamContext object

        Returns: tuple of (ReturnCode, Result Object)

        """
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def retrieve(self, from_site: str, fl_ctx: FLContext, timeout: float, **obj_attrs) -> (str, Any):
        """Retrieve an object from a specified site.

        Args:
            from_site: the site to retrieve the object from
            fl_ctx: a FLContext object
            timeout: max number of seconds to wait for the data
            **obj_attrs: attributes of the object to be retrieved

        Returns: tuple of (ReturnCode, Retrieved Data)

        """
        pass

    def _handle_stream_done(self, stream_ctx: StreamContext, fl_ctx: FLContext):
        # On stream receiving side, which is also the requesting side
        pass

    def _handle_request(self, topic, request: Shareable, fl_ctx: FLContext) -> Shareable:
        # On request receiving side, which is also stream sending side.
        pass

    def _do_stream(self, request: Shareable, fl_ctx: FLContext, validated_data: Any):
        # On request receiving side, which is also stream sending side.
        pass
