# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
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

import base64


def bytes_to_b64str(data_bytes) -> str:
    """Convert binary to base64-encoded string."""
    pass


def b64str_to_bytes(b64str: str) -> bytes:
    """Convert base64-encoded string to binary."""
    pass


def binary_file_to_b64str(file_name) -> str:
    """Encode content of a binary file to a Base64-encoded ASCII string.

    Args:
        file_name: the binary file to be processed

    Returns: base64-encoded ASCII string

    """
    pass


def b64str_to_binary_file(b64str: str, file_name):
    """Decode a base64-encoded string and write it into a binary file.

    Args:
        b64str: the base64-encoded ASCII string
        file_name: the file to write to

    Returns: number of bytes written

    """
    pass


def text_file_to_b64str(file_name) -> str:
    """Encode content of a text file to a Base64-encoded ASCII string.

    Args:
        file_name: name of the text file

    Returns: base64-encoded string

    """
    pass


def str_to_b64str(s: str) -> str:
    pass


def b64str_to_str(b64str: str) -> str:
    pass


def b64str_to_text_file(b64str: str, file_name):
    """Decode a base64-encoded string and write result into a text file.

    Args:
        b64str: base64-encoded string
        file_name: file to be created

    Returns: number of data types written (may not be the same as number of characters)

    """
    pass
