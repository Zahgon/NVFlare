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
import importlib
import inspect
import logging
import os
import sys
from enum import Enum
from os.path import dirname, join
from typing import Any, BinaryIO, Dict, Type, TypeVar, Union

import msgpack

from nvflare.fuel.utils.class_loader import get_class_name, load_class
from nvflare.fuel.utils.fobs.builtin_decomposers import BUILTIN_DECOMPOSERS, BUILTIN_TYPES
from nvflare.fuel.utils.fobs.datum import DatumManager
from nvflare.fuel.utils.fobs.decomposer import (
    DataClassDecomposer,
    Decomposer,
    EnumTypeDecomposer,
    Externalizer,
    Internalizer,
)

__all__ = [
    "register",
    "register_data_classes",
    "register_enum_types",
    "auto_register_enum_types",
    "register_folder",
    "num_decomposers",
    "serialize",
    "serialize_stream",
    "deserialize",
    "deserialize_stream",
    "reset",
    "get_dot_handler",
    "add_type_name_whitelist",
]

from nvflare.security.logging import secure_format_exception

FOBS_TYPE = "__fobs_type__"
FOBS_DATA = "__fobs_data__"
FOBS_DECOMPOSER = "__fobs_dc__"

MAX_CONTENT_LEN = 128
MSGPACK_TYPES = (type(None), bool, int, float, str, bytes, bytearray, memoryview, list, dict)
T = TypeVar("T")

log = logging.getLogger(__name__)
_decomposers: Dict[str, Decomposer] = {}
_dot_handlers: Dict[int, Decomposer] = {}  # decomposers that handle Datum Object Types (DOT)
_decomposers_registered = False
# If this is enabled, FOBS will try to register generic decomposers automatically
_enum_auto_registration = True
_data_auto_registration = True
# Whitelist of type names allowed for deserialization when not already in _decomposers.
# Pre-populated from BUILTIN_TYPES.
_type_name_whitelist: set[str] = set(BUILTIN_TYPES)


def register(decomposer: Union[Decomposer, Type[Decomposer]]) -> None:
    """Register a decomposer. It does nothing if decomposer is already registered for the type

    Args:
        decomposer: The decomposer type or instance
    """
    pass


class Packer:
    def __init__(self, manager: DatumManager):
        self.manager = manager
        self.enum_decomposer_name = get_class_name(EnumTypeDecomposer)
        self.data_decomposer_name = get_class_name(DataClassDecomposer)

    def pack(self, obj: Any) -> dict:

        pass

    def unpack(self, obj: Any) -> Any:

        pass


def add_type_name_whitelist(*type_names: str) -> None:
    """Add type names to the whitelist for deserialization.

    Type names added here are allowed to be auto-loaded during deserialization
    when they have not been explicitly pre-registered. This prevents arbitrary
    class loading (RCE) while still supporting lazy registration use cases.

    Args:
        type_names: Fully qualified class names (e.g. "mypackage.MyClass")
    """
    pass


def register_data_classes(*data_classes: Type[T]) -> None:
    """Register generic decomposers for data classes.

    Also adds each class to the type-name whitelist so that it can be lazily
    re-loaded during deserialization. The whitelist entry is cleared when
    fobs.reset() is called.

    Args:
        data_classes: The classes to be registered
    """
    pass


def register_enum_types(*enum_types: Type[Enum]) -> None:
    """Register generic decomposers for enum classes.

    Also adds each class to the type-name whitelist so that it can be lazily
    re-loaded during deserialization. The whitelist entry is cleared when
    fobs.reset() is called.

    Args:
        enum_types: The enum classes to be registered
    """
    pass


def auto_register_enum_types(enabled=True) -> None:
    """Enable or disable the auto-registration of enum types.

    Args:
        enabled: Auto-registration of enum classes is enabled if True.
    """
    pass


def auto_register_data_classes(enabled=True) -> None:
    """Enable or disable the auto-registration of data classes.

    Args:
        enabled: Auto-registration of data classes is enabled if True.
    """
    pass


def register_folder(folder: str, package: str):
    """Scan the folder and register all decomposers found.

    Args:
        folder: The folder to scan
        package: The package to import the decomposers from
    """
    pass


def register_custom_folder(folder: str):
    pass


def _register_decomposers():
    pass


def num_decomposers() -> int:
    """Returns the number of decomposers registered.

    Returns:
        The number of decomposers
    """
    pass


def serialize(obj: Any, manager: DatumManager = None, **kwargs) -> bytes:
    """Serialize object into bytes.

    Args:
        obj: Object to be serialized
        manager: Datum manager used to externalize datum
        kwargs: Arguments passed to msgpack.packb
    Returns:
        Serialized data
    """
    pass


def serialize_stream(obj: Any, stream: BinaryIO, manager: DatumManager = None, **kwargs):
    """Serialize object and write the data to a stream.

    Args:
        obj: Object to be serialized
        stream: Stream to write the result to
        manager: Datum manager to externalize datum
        kwargs: Arguments passed to msgpack.packb
    """
    pass


def deserialize(data: bytes, manager: DatumManager = None, **kwargs) -> Any:
    """Deserialize bytes into an object.

    Args:
        data: Serialized data
        manager: Datum manager to internalize datum
        kwargs: Arguments passed to msgpack.unpackb
    Returns:
        Deserialized object
    """
    pass


def deserialize_stream(stream: BinaryIO, manager: DatumManager = None, **kwargs) -> Any:
    """Deserialize bytes from stream into an object.

    Args:
        stream: Stream to write serialized data to
        manager: Datum manager to internalize datum
        kwargs: Arguments passed to msgpack.unpackb
    Returns:
        Deserialized object
    """
    pass


def get_dot_handler(dot: int):
    pass


def reset():
    """Reset FOBS to initial state. Used for unit test"""
    pass
