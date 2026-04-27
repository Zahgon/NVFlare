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
import copy
import logging
import time
from typing import Any

import nvflare.fuel.utils.fobs as fobs
from nvflare.fuel.f3.cellnet.defs import Encoding, MessageHeaderKey
from nvflare.fuel.f3.message import Message
from nvflare.fuel.f3.streaming.stream_const import StreamHeaderKey
from nvflare.fuel.utils.buffer_list import BufferList

cell_mapping = {
    "O": MessageHeaderKey.ORIGIN,
    "D": MessageHeaderKey.DESTINATION,
    "F": MessageHeaderKey.FROM_CELL,
    "T": MessageHeaderKey.TO_CELL,
}

msg_mapping = {
    "CH": MessageHeaderKey.CHANNEL,
    "TP": MessageHeaderKey.TOPIC,
    "SCH": StreamHeaderKey.CHANNEL,
    "STP": StreamHeaderKey.TOPIC,
    "SEQ": StreamHeaderKey.SEQUENCE,
}


_MSG_SIZE_HW_THRESHOLD = 1024 * 1024 * 10

log = logging.getLogger(__name__)


class MsgHighWaterInfo:

    def __init__(self, hw_type: str):
        self.hw_type = hw_type
        self.size = 0
        self.timestamp = None
        self.topic = None
        self.origin = None
        self.destination = None
        self.headers = None

    def update(self, size, msg: Message):
        pass


# Some stats of msg size high water
_sent_hw_info = MsgHighWaterInfo("Sent")
_received_hw_info = MsgHighWaterInfo("Received")


def new_cell_message(headers: dict, payload=None):
    pass


def make_reply(rc: str, error: str = "", body=None) -> Message:
    pass


def shorten_string(string):
    pass


def buffer_len(buffer: Any):

    pass


def shorten_fqcn(fqcn):
    pass


def get_msg_header_value(m, k):
    pass


def format_log_message(fqcn: str, message: Message, log: str) -> str:
    pass


def encode_payload(message: Message, encoding_key=MessageHeaderKey.PAYLOAD_ENCODING, fobs_ctx: dict = None) -> int:
    """Encode the payload of the specified message.

    Args:
        message: the message to be encoded
        encoding_key: the key name of the encoding property in the message header. If the encoding property is not
        set in the message header, then it means that the message payload has not been encoded. If the property is
        already set, then the message payload is already encoded, and no processing is done.
        If encoding is needed, we will determine the encoding scheme based on the data type of the payload:
        - If the payload is None, encoding scheme is NONE
        - If the payload data type is like bytes, encoding scheme is BYTES
        - Otherwise, encoding scheme is FOBS, and the payload is serialized with FOBS.
        fobs_ctx: contextual info for decomposers

    Returns: the encoded payload size.

    """
    pass


def decode_payload(message: Message, encoding_key=MessageHeaderKey.PAYLOAD_ENCODING, fobs_ctx: dict = None):
    pass


def format_size(size, binary=False):
    """Format size in human-readable formats like  KB, MB, KiB, MiB

    Args:
        size: Size in bytes
        binary: If binary, one K is 1024 bytes, otherwise 1000 bytes.

    Returns: Size in human-readable format (like 10MB, 100.2GiB etc)

    """
    pass
