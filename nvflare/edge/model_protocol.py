# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
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

"""Model exchange protocol specification and utilities.

This module defines the complete protocol for exchanging models between components,
including message format specification, supported types, and validation utilities.

Example:
    >>> from nvflare.edge.utils.model_protocol import ModelBufferType, ModelExchangeFormat
    >>> task_dxo = {
    ...     "data": encoded_data,
    ...     "meta": {
    ...         ModelExchangeFormat.MODEL_BUFFER_TYPE: ModelBufferType.EXECUTORCH,
    ...         ModelExchangeFormat.MODEL_BUFFER_NATIVE_FORMAT: ModelNativeFormat.BINARY,
    ...         ModelExchangeFormat.MODEL_BUFFER_ENCODING: ModelEncoding.BASE64
    ...     }
    ... }
    >>> verify_payload(
    ...     payload,
    ...     expected_type=ModelBufferType.EXECUTORCH
    ... )
"""

import logging
from typing import Dict, Optional

from nvflare.apis.dxo import DXO

log = logging.getLogger(__name__)


class ModelBufferType:
    """Supported model buffer types for data exchange.

    These constants define the supported types of data that can be exchanged,
    helping ensure consistency across different components.
    """

    # Model formats
    EXECUTORCH = "executorch"
    PYTORCH = "pytorch"


class ModelNativeFormat:
    """Native format of the data before any transmission encoding."""

    BINARY = "binary"  # Raw bytes, binary data
    STRING = "string"  # Text-based data


class ModelEncoding:
    """Supported encodings for data transmission.

    For binary native format:
        - BASE64 or HEX encoding required for safe transmission

    For string native format:
        - UTF8 or ASCII for character encoding
        - NONE for plain string data
    """

    BASE64 = "base64"
    HEX = "hex"
    UTF8 = "utf8"
    ASCII = "ascii"
    NONE = "none"


class ModelExchangeFormat:
    """Constants for model exchange protocol between components.

    The protocol uses three main attributes:
    1. TYPE: What the data represents (e.g., executorch, pytorch)
    2. NATIVE_FORMAT: Original format before any transmission encoding
    3. ENCODING: How the data is encoded for transmission

    Format and Encoding combinations:
        - For binary FORMAT:
            - base64 encoding (safe for text transmission)
            - hex encoding (alternative text encoding)
        - For string FORMAT:
            - utf8 encoding (for unicode text)
            - ascii encoding (for restricted character set)
            - null/empty (for plain string)

    Examples:
        Binary data (ExecutorTorch model):
            {
                "data": <encoded_data>,
                "meta": {
                  MODEL_BUFFER_TYPE: ModelBufferType.EXECUTORCH,
                  MODEL_BUFFER_NATIVE_FORMAT: ModelNativeFormat.BINARY,
                  MODEL_BUFFER_ENCODING: ModelEncoding.BASE64
                }
            }

        String data (JSON config):
            {
                "data": <json_string>,
                "meta": {
                  MODEL_BUFFER_TYPE: ModelBufferType.JSON,
                  MODEL_BUFFER_NATIVE_FORMAT: ModelNativeFormat.STRING,
                  MODEL_BUFFER_ENCODING: ModelEncoding.UTF8
                }
            }
    """

    MODEL_BUFFER_TYPE = "model_buffer_type"
    MODEL_BUFFER_NATIVE_FORMAT = "model_buffer_native_format"
    MODEL_BUFFER_ENCODING = "model_buffer_encoding"
    MODEL_VERSION = "model_version"


def verify_payload(
    task_dxo: DXO,
    expected_type: Optional[str] = None,
    expected_format: Optional[str] = None,
    expected_encoding: Optional[str] = None,
) -> Dict:
    """Verify that the task data payload follows the model exchange protocol.

    Args:
        task_dxo: The task data dxo to verify
        expected_type: Expected model buffer type (from ModelBufferType)
        expected_format: Expected native format (from ModelNativeFormat)
        expected_encoding: Expected encoding (from ModelEncoding)

    Raises:
        ValueError: If the payload structure is invalid or values don't match expected
    """
    pass
