# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
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
import io
import os.path
import struct
import uuid
from typing import Any, BinaryIO, Optional, Union

from nvflare.fuel.utils.config_service import ConfigService
from nvflare.fuel.utils.fobs import deserialize, get_dot_handler, serialize
from nvflare.fuel.utils.fobs.buf_list_stream import BufListStream
from nvflare.fuel.utils.fobs.datum import Datum, DatumManager, DatumType
from nvflare.fuel.utils.fobs.decomposer import Externalizer, Internalizer

# DAT: Datum App Type
HEADER_STRUCT = struct.Struct(">BBQ")  # marker(1), dot(1), size(8)
HEADER_LEN = HEADER_STRUCT.size

MARKER_MAIN = 100
MARKER_DATUM_TEXT = 101
MARKER_DATUM_BLOB = 102
MARKER_DATUM_FILE = 103

DATUM_ID_LEN = 16
MAX_BYTES_PER_READ = 1024 * 1024  # 1MB

DATUM_DIR_CONFIG_VAR = "datum_dir"

# this default should work for all systems. Can be overridden by NVFLARE_DATUM_DIR system environment variable.
DEFAULT_DATUM_DIR = os.path.join(os.path.abspath(os.sep), "tmp", "nvflare", "datums")


class _Header:
    def __init__(self, marker: int, dot: int, size: int):
        self.marker = marker
        self.dot = dot
        self.size = size

    @classmethod
    def from_bytes(cls, buffer: bytes):
        pass

    def to_bytes(self):
        pass


def _write_datum_header(stream: BinaryIO, marker, dot, datum_id: str, value_size: int):
    pass


def dump_to_stream(obj: Any, stream: BinaryIO, max_value_size=None, fobs_ctx: Optional[dict] = None):
    """
    Serialize the specified object to a stream of bytes. If the object contains any datums, they will be included
    into the result.

    The result may contain multiple sections:
    - the 1st section is the main body (serialized with fobs/msgpack) of the object
    - if the object contains large binary data, they will be converted to datums, and each datum has one section

    During serialization, the object may be altered (replace large value with datums). After serialization, the object
    is restored to its original state.

    Args:
        obj: the object to be serialized.
        stream: the stream that serialized data will be written to.
        max_value_size: max size of bytes/str value allowed. If a value exceeds this, it will be converted to datum.
        If not specified, default is 10MB.
        fobs_ctx: context info

    Returns: None

    """
    pass


def _get_datum_id(stream: BinaryIO, header: _Header):
    """Get datum ID from the stream:
    - Read 16 bytes from the stream
    - Convert the bytes to hex string - this gives a UUID string without hyphens
    - Make a UUID object from the hex string
    - Convert it to string - this gives a UUID string with hyphens. This version is what we need!

    Args:
        stream: the stream that contains bytes to be deserialized
        header: the header of the section

    Returns: datum ID string

    """
    pass


def _get_one_section(stream: BinaryIO, expect_datum: bool):
    """
    Get one data section from the stream. A section represents a complete item: the main body of the serialized object
    or a Datum.

    Args:
        stream: the stream that contains the data
        expect_datum: whether the section is expected to be a Datum.

    Returns: a tuple of (header, datum_id, data_bytes)

    """
    pass


def get_datum_dir():
    """When a file datum is received, the data will be stored in a temporary file under a predefined Datum Directory.
    This function returns this predefined Datum Directory. The function also tries to create the directory if
    it does not exist.

    The directory can be defined with a system environment variable: NVFLARE_DATUM_DIR.

    Returns: name of the datum directory

    Notes: temporary dir from tempfile must not be used! This is because the file must continue to exist after it is
    closed.

    """
    pass


def load_from_stream(stream: BinaryIO, fobs_ctx: Optional[dict] = None):
    """Load/deserialize data from the specified stream into an object.

    The data in the stream must be a well-formed serialized data. It has one or more sections:
    - The 1st section contains the main body of the object (serialized with fobs/msgpack)
    - Optionally, more datum sections follow, each representing a datum that is referenced in the main body.

    Args:
        stream: the stream that contains data to be deserialized.
        fobs_ctx: contextual info for decomposers

    Returns: an object

    """
    pass


def dump_to_bytes(obj: Any, buffer_list=False, max_value_size=None, fobs_ctx: Optional[dict] = None):
    """Serialize an object to bytes

    Args:
        obj: object to be serialized
        max_value_size: the max size allowed for bytes/str value in the object. If a value exceeds this, it will be
        converted to datum. If not specified, default is 10MB.
        buffer_list: If true, returns buffer list to save memory
        fobs_ctx: context info for decomposers

    Returns: a bytes object

    """
    pass


def load_from_bytes(data: Union[bytes, list], fobs_ctx: Optional[dict] = None) -> Any:
    """Deserialize the bytes into an object

    Args:
        data: the bytes to be deserialized
        fobs_ctx: context info for decomposers

    Returns: an object

    """
    pass


def dump_to_file(obj: Any, file_path: str, max_value_size=None, fobs_ctx: Optional[dict] = None):
    """Serialize the object and save result to the specified file.

    Args:
        obj: object to be serialized
        file_path: path of the file to store serialized data
        max_value_size: the max size allowed for bytes/str value in the object. If a value exceeds this, it will be
        converted to datum. If not specified, default is 10MB.
        fobs_ctx: context info for decomposers

    Returns: None

    """
    pass


def load_from_file(file_path: str, fobs_ctx: Optional[dict] = None) -> Any:
    """Deserialized data in the specified file into an object

    Args:
        file_path: the file that contains data to be deserialized.
        fobs_ctx: context info for decomposers

    Returns: an object

    """
    pass
