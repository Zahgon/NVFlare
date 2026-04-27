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

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, List, Optional, Type, TypeVar

# Generic type supported by the decomposer.
from nvflare.fuel.utils.fobs.datum import Datum, DatumManager, DatumRef, DatumType

T = TypeVar("T")

DICT_CONTENT = "dict"
DATA_CONTENT = "data"


class Decomposer(ABC):
    """Abstract base class for decomposers.

    Every class to be serialized by FOBS must register a decomposer which is
    a concrete subclass of this class.
    """

    @abstractmethod
    def supported_type(self) -> Type[T]:
        """Returns the type/class supported by this decomposer.

        Returns:
            The class (not instance) of supported type
        """
        pass

    def supported_dots(self) -> Optional[List[int]]:
        """Return the Datum Object Types supported by this decomposer.
        If a DOT is returned, this decomposer's process_datum method will be called for any datum whose DOT
        matches this DOT.

        Returns: None or list of DOTs

        """
        pass

    def process_datum(self, datum: Datum, manager: DatumManager):
        """This method will be called during message deserialization to process the specified datum.

        Args:
            datum: the datum to be processed
            manager: the datum manger

        Returns: None

        """
        pass

    @abstractmethod
    def decompose(self, target: T, manager: DatumManager = None) -> Any:
        """Decompose the target into types supported by msgpack or classes with decomposers registered.

        Msgpack supports primitives, bytes, memoryview, lists, dicts.

        Args:
            target: The instance to be serialized
            manager: Datum manager to store externalized datum

        Returns:
            The decomposed serializable objects
        """
        pass

    @abstractmethod
    def recompose(self, data: Any, manager: DatumManager = None) -> T:
        """Reconstruct the object from decomposed components.

        Args:
            data: The decomposed component
            manager: Datum manager to internalize datum

        Returns:
            The reconstructed object
        """
        pass


def restore_position(manager: DatumManager, datum: Datum, position):
    """
    This function is used for restoring object state at the specified position.

    Args:
        manager: the datum manager
        datum: the datum that contains the value of the original object at the position.
        position: the position to be restored

    Returns: None

    """
    pass


class Externalizer:
    """
    This class is used to help creating 'decompose' method of decomposers of arbitrary classes.

    """

    def __init__(self, manager: DatumManager):
        self.manager = manager

    def _set_position(self, ext_result: Any, target, key):
        pass

    def externalize(self, target: Any):
        """Recursively go through object tree (dict or list) and externalize leaf nodes."""
        pass


class Internalizer:
    """
    This class is used to help creating 'recompose' method of decomposers of arbitrary classes.

    """

    def __init__(self, manager: DatumManager):
        self.manager = manager

    def internalize(self, target) -> Any:
        """Recursively go through object tree (dict or list) and internalize leaf nodes."""
        pass


class DictDecomposer(Decomposer):
    """Generic decomposer for subclasses of dict like Shareable"""

    def __init__(self, dict_type: Type[dict]):
        self.dict_type = dict_type

    def supported_type(self):
        pass

    def decompose(self, target: dict, manager: DatumManager = None) -> Any:
        # need to create a new object; otherwise msgpack will try to decompose this object endlessly.
        pass

    def recompose(self, data: dict, manager: DatumManager = None) -> dict:
        pass


class DataClassDecomposer(Decomposer):
    """Generic decomposers for data classes, which must meet following requirements:

    1. All class members must be serializable. The type of member must be one of the
       types supported by MessagePack or a decomposer is registered for the type.
    2. The __new__ method only takes one argument which is the class type.
    3. The __init__ method has no side effects. It can only change the states of the
       object. The side effects include creating files, initializing loggers, modifying
       global variables.

    """

    def __init__(self, data_type: Type[T]):
        self.data_type = data_type

    def supported_type(self) -> Type[T]:
        pass

    def decompose(self, target: T, manager: DatumManager = None) -> Any:
        pass

    def recompose(self, data: dict, manager: DatumManager = None) -> T:
        pass


class EnumTypeDecomposer(Decomposer):
    """Generic decomposers for enum types."""

    def __init__(self, data_type: Type[Enum]):
        if not issubclass(data_type, Enum):
            raise TypeError(f"{data_type} is not an enum")

        self.data_type = data_type

    def supported_type(self) -> Type[Enum]:
        pass

    def decompose(self, target: Enum, manager: DatumManager = None) -> Any:
        pass

    def recompose(self, data: Any, manager: DatumManager = None) -> Enum:
        pass
