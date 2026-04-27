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

"""
This package implements a binary protocol for data exchange between the Admin client and server. This is mainly
used for large data exchanges such as job submission and download.

The format of a binary exchange has 4 sections (header, meta, body, and footer), as follows:

    [Header] [Meta] [Body] [Footer]

Header section: {binary_marker:1} {meta_size:4} {body_size:8}
Meta section: {meta:meta_size}
Body section: {body:body_size}
Footer section: {end_marker:4} {checksum:4}

The 1-byte binary_marker in Header signifies that the exchange is binary. If this marker is missing,
the exchange is text.

A binary exchange can optionally include text-encoded meta information (e.g. a JSON string).

At the end of the exchange is the footer that contains end-of-data marker (four bytes of 0) and the checksum computed
over the body bytes.

Note that the binary protocol does not replace the text protocol, which is still used for regular admin commands.

"""

import os
import struct
import tempfile
import uuid
from abc import ABC, abstractmethod

from .checksum import Checksum
from .proto import ALL_END, LINE_END, MAX_BLOCK_SIZE

CT_TEXT = 0
CT_BINARY = 1
BINARY_MARKER = 1

HEADER_STRUCT = struct.Struct(">IQ")  # meta_size(4), body_size(8)
HEADER_LEN = HEADER_STRUCT.size

FOOTER_STRUCT = struct.Struct(">II")  # end_marker(four 0s), checksum(4)
FOOTER_LEN = FOOTER_STRUCT.size


class Receiver(ABC):
    """
    A Receiver must be able to receive bytes from the peer.
    """

    @abstractmethod
    def recv(self, size: int) -> bytes:
        """Receive bytes of up to the specified size.
        Note that this method is named "recv" to make TCP socket automatically a Receiver (duck typing).

        Args:
            size: the max number of bytes to receive.

        Returns: bytes of no more than size; or None if recv is not possible (e.g. peer reset connection)

        """
        pass


class DataProcessor(ABC):
    """
    A DataProcessor is used to process data received from the peer.
    """

    @abstractmethod
    def process(self, data: bytes, content_type: int) -> bool:
        """Process the data received from peer.

        Args:
            data: the data to be processed
            content_type: the content type: CT_TEXT or CT_BINARY

        Returns: whether this is the end of process

        """
        pass

    @abstractmethod
    def finalize(self):
        """Finalize the processor. This is called when the exchange processing is finished.

        Returns: None

        """
        pass


class ExchangeHandler:
    """
    The ExchangeHandler is used to receive and parse exchange from the peer.
    It uses the provided Receiver to receive data from the peer, parses the data according to the echange protocl,
    and calls the provided DataProcessor to process the data.
    """

    def __init__(self, receiver: Receiver, processor: DataProcessor):
        """Constructor of ExchangeHandler

        Args:
            receiver: the data receiver object to be used to receive data from the peer
            processor: the data processor for data processing
        """
        self.receiver = receiver
        self.processor = processor
        self.meta = None
        self.content_type = None

    def _must_recv(self, num_bytes: int):
        """Must receive specified number of bytes.

        Note that the receiver's recv method can return any number of bytes. We keep calling it until the
        specified number of bytes are received.

        Args:
            num_bytes: number of bytes to receive

        Returns: received bytes

        """
        pass

    def _parse_text(self):
        pass

    def _parse_binary(self, body_size):
        pass

    def receive_and_parse(self):
        """Receive data of the exchange from the peer and parse it according to the protocol definition.

        Returns: None

        """
        pass


class MsgDataProcessor(DataProcessor):
    """The MsgDataProcessor is a special DataProcessor that can handle both TEXT and BINARY content type.
    For TEXT, it collects all received text segments and assemble them into one text string;
    For BINARY, it saves received data into a temporary file so that no memory is used to collect the data. This
    is necessary to support extremely large data exchanges (e.g. large job submission and download).

    """

    def __init__(self):
        self.file = None
        self.file_name = None
        self.text_segs = []
        self.total_text = None

    def process(self, data, content_type: int):
        pass

    def finalize(self):
        pass


def receive_all(receiver: Receiver):
    """Receive all data from the peer via the specified communication socket.
    This function uses the MsgDataProcessor for memory saving during data exchange.

    Args:
        receiver: the object that is capable of receiving. Note that TCP socket is a Receiver (duck typing)

    Returns: a tuple of (content_type, request_text, additional_data)

    When content_type is CT_TEXT, the request_text is the request body, and additional_data is None;
    When content_type is CT_BINARY, the request_text is the meta info, and additional_data is the name of a
    temporary file that holds the received body data. However, if there is no data (size 0), the value of
    additional_data is None.
    """
    pass


def binary_header(meta_size: int, body_size: int):
    """Create bytes for the exchange header.

    Args:
        meta_size: size of the meta info
        body_size: size of the message body

    Returns: encoded bytes of the header

    """
    pass


def binary_footer(checksum: int):
    """Create bytes for the exchange footer.

    Args:
        checksum: the checksum value.

    Returns: encoded bytes of the footer

    """
    pass


class DataGenerator(ABC):
    @abstractmethod
    def data_size(self) -> int:
        """Return the size of the exchange body to be generated. This method is called before the generate method is called.
        Therefore, the DataGenerator must know the size of the exchange body in advance.

        Returns: the size of the exchange body to be generated

        """
        pass

    @abstractmethod
    def generate(self) -> bytes:
        """This method is called to generate next chunk of data to be sent.

        Returns: bytes to be sent; or None if no more data.

        """
        pass


class Sender(ABC):
    @abstractmethod
    def sendall(self, data: bytes):
        """Send specified data until done. This method must send all bytes, instead of a subset of it!
        Note that this method is named "sendall" to make TCP socket automatically a Sender (duck typing).

        Args:
            data: data to be sent.

        Returns:

        """
        pass


def send_binary_data(sender: Sender, generator: DataGenerator, meta: str) -> int:
    """Send data in binary exchange protocol.

    Args:
        sender: the sender that is capable of sending bytes
        generator: the generator that is capable of generating data to be sent
        meta: the meta info to be included in the exchange

    Returns: number of body bytes sent

    """
    pass


class GenerateDataFromFile(DataGenerator):
    """
    This is a special DataGenerator that generates bytes from a file.
    """

    def __init__(self, file_name: str):
        file_stats = os.stat(file_name)
        self.size = file_stats.st_size
        self.file = open(file_name, "rb")

    def data_size(self) -> int:
        pass

    def generate(self) -> bytes:
        pass


def send_binary_file(sender: Sender, file_name: str, meta: str) -> int:
    """Send a file using binary protocol.

    Args:
        sender: the object that is capable of sending. Note that TCP socket is a Sender (duck typing).
        file_name: the file to be sent
        meta: the meta info to be sent

    Returns: number of bytes sent (the same as size of the file)

    """
    pass
