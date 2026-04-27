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

import concurrent.futures
import copy
import threading
import uuid
from typing import Dict, List, Union

from nvflare.apis.signal import Signal
from nvflare.fuel.f3.cellnet.core_cell import CoreCell, TargetMessage
from nvflare.fuel.f3.cellnet.defs import CellChannel, MessageHeaderKey, MessagePropKey, MessageType, ReturnCode
from nvflare.fuel.f3.cellnet.utils import decode_payload, encode_payload, make_reply
from nvflare.fuel.f3.message import Message
from nvflare.fuel.f3.stream_cell import StreamCell
from nvflare.fuel.f3.streaming.stream_const import StreamHeaderKey
from nvflare.fuel.f3.streaming.stream_types import StreamFuture
from nvflare.fuel.utils.fobs import FOBSContextKey
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.fuel.utils.waiter_utils import WaiterRC, conditional_wait
from nvflare.security.logging import secure_format_exception

CHANNELS_TO_EXCLUDE = (
    CellChannel.CLIENT_MAIN,
    CellChannel.SERVER_MAIN,
    CellChannel.SERVER_PARENT_LISTENER,
    CellChannel.CLIENT_COMMAND,
    CellChannel.CLIENT_SUB_WORKER_COMMAND,
    CellChannel.MULTI_PROCESS_EXECUTOR,
    CellChannel.SIMULATOR_RUNNER,
    CellChannel.RETURN_ONLY,
)


def _is_stream_channel(channel: str) -> bool:
    pass


class SimpleWaiter:
    def __init__(self, req_id, result):
        super().__init__()
        self.req_id = req_id
        self.result = result
        self.receiving_future = None
        self.in_receiving = threading.Event()


class Adapter:
    def __init__(self, cb, my_info, cell):
        self.cb = cb
        self.my_info = my_info
        self.cell = cell
        self.logger = get_obj_logger(self)

    def call(self, future, *args, **kwargs):  # this will be called by StreamCell upon receiving the first byte of blob
        pass


class Cell(StreamCell):
    def __init__(self, *args, **kwargs):
        self.core_cell = CoreCell(*args, **kwargs)
        super().__init__(self.core_cell)
        self.requests_dict = dict()
        self.logger = get_obj_logger(self)
        self.register_blob_cb(CellChannel.RETURN_ONLY, "*", self._process_reply)  # this should be one-time registration
        self.core_cell.update_fobs_context({FOBSContextKey.CELL: self})
        self.decode_pass_through_channels: set = set()  # per-channel opt-in for receiver-side PASS_THROUGH

    def update_fobs_context(self, props: dict):
        pass

    def get_fobs_context(self, props: dict = None):
        """Return a new copy of the fobs context. If props is specified, they will be set into the context.

        Returns: a new copy of the fobs context

        """
        pass

    def __getattr__(self, func):
        """
        This method is called when Python cannot find an invoked method "x" of this class.
        Method "x" is one of the message sending methods (send_request, broadcast_request, etc.)
        In this method, we decide which method should be used instead, based on the "channel" of the message.
        - If the channel is stream channel, use the method "_x" of this class.
        - Otherwise, user the method "x" of the CoreCell.
        """

        def method(*args, **kwargs):
            pass

        return method

    def _broadcast_request(
        self,
        channel: str,
        topic: str,
        targets: Union[str, List[str]],
        request: Message,
        timeout=None,
        secure=False,
        optional=False,
        abort_signal: Signal = None,
    ) -> Dict[str, Message]:
        """
        Send a message over a channel to specified destination cell(s), and wait for reply

        Args:
            channel: channel for the message
            topic: topic of the message
            targets: FQCN of the destination cell(s)
            request: message to be sent
            timeout: how long to wait for replies
            secure: End-end encryption
            optional: whether the message is optional
            abort_signal: signal to abort the message

        Returns: a dict of: cell_id => reply message

        """
        pass

    def _fire_and_forget(
        self,
        channel: str,
        topic: str,
        targets: Union[str, List[str]],
        message: Message,
        secure=False,
        optional=False,
    ) -> Dict[str, str]:
        """
        Send a message over a channel to specified destination cell(s), and do not wait for replies.

        Args:
            channel: channel for the message
            topic: topic of the message
            targets: one or more destination cell IDs. None means all.
            message: message to be sent
            secure: End-end encryption if True
            optional: whether the message is optional

        Returns: None

        """
        pass

    def _get_result(self, req_id):
        pass

    def _check_error(self, future):
        pass

    def _future_wait(self, future, timeout, abort_signal: Signal):
        # future could have an error!
        pass

    def _encode_message(self, msg: Message, abort_signal, num_receivers=1) -> int:
        pass

    def _send_request(
        self,
        channel,
        target,
        topic,
        request,
        timeout=10.0,
        secure=False,
        optional=False,
        abort_signal: Signal = None,
    ):
        """Stream one request to the target

        Args:
            channel: message channel name
            target: FQCN of the target cell
            topic: topic of the message
            request: request message
            timeout: how long to wait
            secure: is P2P security to be applied
            optional: is the message optional
            abort_signal: signal to abort the message

        Returns: reply data

        """
        pass

    def _send_one_request(
        self,
        channel,
        target,
        topic,
        request,
        timeout=10.0,
        secure=False,
        optional=False,
        abort_signal=None,
    ):
        pass

    def _process_reply(self, future: StreamFuture):
        pass

    def _register_request_cb(self, channel: str, topic: str, cb, *args, **kwargs):
        """
        Register a callback for handling request. The CB must follow request_cb_signature.

        Args:
            channel: the channel of the request
            topic: topic of the request
            cb:
            *args:
            **kwargs:

        Returns:

        """
        pass
