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
from typing import Any

from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReturnCode, Shareable
from nvflare.apis.streaming import StreamContext

from .container_streamer import ContainerStreamer
from .object_retriever import ObjectRetriever


class ContainerRetriever(ObjectRetriever):
    def __init__(
        self,
        topic: str = None,
        stream_msg_optional=False,
        stream_msg_secure=False,
        entry_timeout=None,
    ):
        ObjectRetriever.__init__(self, topic)
        self.stream_msg_optional = stream_msg_optional
        self.stream_msg_secure = stream_msg_secure
        self.entry_timeout = entry_timeout
        self.containers = {}

    def add_container(self, name: str, container: Any):
        """Add a container to the retriever. This must be called on the sending side

        Args:
            name: name for the container.
            container: The container to be streamed
        """
        pass

    def register_stream_processing(
        self,
        channel: str,
        topic: str,
        fl_ctx: FLContext,
        stream_done_cb,
        **cb_kwargs,
    ):
        """Called on the stream sending side.

        Args:
            channel:
            topic:
            fl_ctx:
            stream_done_cb:
            **cb_kwargs:

        Returns:

        """
        pass

    def validate_request(self, request: Shareable, fl_ctx: FLContext) -> (str, Any):
        pass

    def retrieve_container(self, from_site: str, fl_ctx: FLContext, timeout: float, name: str) -> (str, Any):
        """Retrieve a container from the specified site.
        This method is to be called by the app.

        Args:
            from_site: the site that has the container to be retrieved
            fl_ctx: FLContext object
            timeout: how long to wait for the file
            name: name of the container

        Returns: a tuple of (ReturnCode, container)

        """
        pass

    def do_stream(
        self, target: str, request: Shareable, fl_ctx: FLContext, stream_ctx: StreamContext, validated_data: Any
    ):
        """Stream the container to the peer.
        Called on the stream sending side.

        Args:
            target: the receiving site
            request: data to be sent
            fl_ctx: FLContext object
            stream_ctx: the stream context
            validated_data: the file full path returned from the validate_request method

        Returns:

        """
        pass

    def get_result(self, stream_ctx: StreamContext) -> (str, Any):
        """Called on the stream receiving side.
        Get the final result of the streaming.
        The result is the location of the received file.

        Args:
            stream_ctx: the StreamContext

        Returns:

        """
        pass
