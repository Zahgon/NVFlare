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
from typing import Optional

import msgpack

from nvflare.fuel.f3.connection import BytesAlike, Connection
from nvflare.fuel.f3.endpoint import Endpoint
from nvflare.fuel.f3.sfm.constants import HandshakeKeys, Types
from nvflare.fuel.f3.sfm.prefix import PREFIX_LEN, Prefix

log = logging.getLogger(__name__)


class SfmConnection:
    """A wrapper of driver connection.

    Driver connection deals with frame. This connection handles messages.

    The frame format:

    .. code-block::

        +--------------------------------------------------------+
        |                    length (4 bytes)                    |
        +----------------------------+---------------------------+
        |        header_len (2)      |   type (1)  |  reserved   |
        +----------------------------+---------------------------+
        |          flags (2)         |        app_id (2)         |
        +----------------------------+---------------------------+
        |        stream_id (2)       |       sequence (2)        |
        +--------------------------------------------------------+
        |                        Headers                         |
        |                    header_len bytes                    |
        +--------------------------------------------------------+
        |                                                        |
        |                        Payload                         |
        |              (length-header_len-16) bytes              |
        |                                                        |
        +--------------------------------------------------------+

    """

    def __init__(self, conn: Connection, local_endpoint: Endpoint):
        self.conn = conn
        self.local_endpoint = local_endpoint
        self.sfm_endpoint = None
        self.last_activity = 0
        self.sequence = 0
        self.lock = threading.Lock()
        self.send_state_lock = threading.Lock()
        self.send_started_at = 0.0

    def get_name(self) -> str:
        pass

    def next_sequence(self) -> int:
        """Get next sequence number for the connection.

        Sequence is used to detect lost frames.
        """
        pass

    def send_handshake(self, frame_type: int):
        """Send HELLO/READY frame"""
        pass

    def send_heartbeat(self, frame_type: int, data: Optional[dict] = None):
        """Send Ping or Pong"""
        pass

    def send_data(self, app_id: int, stream_id: int, headers: Optional[dict], payload: BytesAlike):
        """Send user data"""
        pass

    def send_dict(self, frame_type: int, stream_id: int, data: dict):
        """Send a dict as payload"""
        pass

    def send_frame(self, prefix: Prefix, headers: Optional[dict], payload: Optional[BytesAlike]):

        pass

    def get_send_stall_seconds(self) -> float:
        pass

    @staticmethod
    def headers_to_bytes(headers: Optional[dict]) -> Optional[bytes]:
        pass
