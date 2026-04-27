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
import struct

from .checksum import Checksum

HEADER_STRUCT = struct.Struct(">BII")  # marker(1), seq_num(4), size(4)
HEADER_LEN = HEADER_STRUCT.size

MARKER_DATA = 101
MARKER_END = 102

MAX_CHUNK_SIZE = 1024 * 1024


def get_slice(buf, start: int, length: int):
    pass


class Header:
    def __init__(self, marker, num1, num2):
        self.marker = marker
        self.checksum = 0
        self.seq = 0
        self.size = 0
        if marker == MARKER_DATA:
            self.seq = num1
            self.size = num2
        elif marker == MARKER_END:
            if num1 != 0:
                raise ValueError(f"num1 must be 0 for checksum but got {num1}")
            self.checksum = num2
        else:
            raise ValueError(f"invalid chunk marker {marker}")

    def __str__(self):
        d = {
            "marker": self.marker,
            "seq": self.seq,
            "size": self.size,
            "checksum": self.checksum,
        }
        return f"{d}"

    @classmethod
    def from_bytes(cls, buffer: bytes):
        pass

    def to_bytes(self):
        pass


class ChunkState:
    def __init__(self, expect_seq=1):
        self.header_bytes = bytearray()
        self.header = None
        self.received = 0
        self.expect_seq = expect_seq

    def __str__(self):
        d = {
            "header": f"{self.header}",
            "header_bytes": f"{self.header_bytes}",
            "received": self.received,
            "expect_seq": self.expect_seq,
        }
        return f"{d}"

    def unpack_header(self):
        pass

    def is_last(self):
        pass


class Receiver:
    def __init__(self, receive_data_func):
        self.receive_data_func = receive_data_func
        self.checksum = Checksum()
        self.current_state = ChunkState()
        self.done = False

    def receive(self, data) -> bool:
        pass

    def _process_chunk(self, c: ChunkState, data, start: int, length: int):
        pass


class Sender:
    def __init__(self, send_data_func):
        self.send_data_func = send_data_func
        self.checksum = Checksum()
        self.next_seq = 1
        self.closed = False

    def send(self, data):
        pass

    def close(self):
        pass


def chunk_it(c: ChunkState, data, cursor: int, process_chunk_func) -> ChunkState:
    pass
