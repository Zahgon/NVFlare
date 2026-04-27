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
import uuid
from enum import Enum
from typing import Any, Callable, Dict, Union

TEN_MEGA = 10 * 1024 * 1024
MIN_THRESHOLD = 1024


class DatumType(Enum):
    TEXT = 1  # for text string
    BLOB = 2  # for binary bytes
    FILE = 3  # for file name


class Datum:
    """Datum is a class that holds information for externalized data"""

    def __init__(self, datum_type: DatumType, value: Any, dot=0):
        """Constructor of Datum object

        Args:
            datum_type: type of the datum.
            value: value of the datum
            dot: the Object Type of the datum

        """
        self.datum_id = str(uuid.uuid4())
        self.datum_type = datum_type
        self.dot = dot
        self.value = value
        self.restore_func = None  # func to restore original object.
        self.restore_func_data = None  # arg to the restore func

    def set_restore_func(self, func, func_data):
        """Set the restore function and func data.
        Restore func is set during the serialization process. If set, the func will be called after the serialization
        to restore the serialized object back to its original state.

         Args:
             func: the restore function
             func_data: arg passed to the restore func when called

         Returns: None

        """
        pass

    @staticmethod
    def blob_datum(blob: Union[bytes, bytearray, memoryview], dot=0):
        """Factory method to create a BLOB datum"""
        pass

    @staticmethod
    def text_datum(text: str, dot=0):
        """Factory method to create a TEXT datum"""
        pass

    @staticmethod
    def file_datum(path: str, dot=0):
        """Factory method to crate a file datum"""
        pass


class DatumRef:
    """A reference to externalized datum. If unwrap is true, the reference will be removed and replaced with the
    content of the datum"""

    def __init__(self, datum_id: str, unwrap=False):
        self.datum_id = datum_id
        self.unwrap = unwrap


class DatumManager:
    def __init__(self, threshold=None, fobs_ctx: dict = None):
        if not threshold:
            threshold = TEN_MEGA

        if not isinstance(threshold, int):
            raise TypeError(f"threshold must be int but got {type(threshold)}")

        if threshold < MIN_THRESHOLD:
            raise ValueError(f"threshold must be at least {MIN_THRESHOLD} but got {threshold}")

        if not fobs_ctx:
            fobs_ctx = {}

        self.threshold = threshold
        self.datums: Dict[str, Datum] = {}
        self.fobs_ctx = fobs_ctx

        # some decomposers (e.g. Shareable, Learnable, etc.) make a shallow copy of the original object before
        # serialization. After serialization, only the values in the copy are restored. We need to keep a ref
        # from the copy to the original object so that values in the original are also restored.
        self.obj_copies = {}  # copy id => original object

        # Post CBs are called after the serialize process is done
        # Post CBs could be used, for example, to prepare files to be downloaded by the message receiver
        self.post_cbs = []
        self.error = None  # save error text

    def add_datum(self, d: Datum):
        pass

    def get_fobs_context(self):
        """Get the FOBS Context associated with the manager.
        The context is available during the whole process of serialization/deserialization of a single message.
        Since Decomposers are singleton objects that could be used by multiple decomposition processes concurrently,
        processing state data must not be stored in the decomposer! Instead, such data should be stored in the
        FOBS context.

        Returns:

        """
        pass

    def register_post_cb(self, cb: Callable[["DatumManager"], None], **cb_kwargs):
        """Register a callback that will be called after the decomposition is done during serialization process.
        The callback is typically registered during decomposition by decomposers.

        Note that the callback itself could also call this method to register additional callbacks. These callbacks
        will be appended to the callback list.

        The manager's post CB processing continues until all registered callbacks are invoked.

        Args:
            cb: the callback to be registered
            **cb_kwargs: kwargs to be passed to the callback when invoked

        Returns:

        """
        pass

    def set_error(self, error: str):
        """Set an error with the manager.
        The manager will eventually raise RuntimeError at the end of serialization if any error is set.

        Args:
            error: the error to be set

        Returns: None

        """
        pass

    def get_error(self):
        """Get the error set with the manager

        Returns: the error set with the manager

        """
        pass

    def post_process(self):
        """Invoke all post serialization callbacks.
        Called during serialization after all objects are decomposed.

        Returns: None

        """
        pass

    def register_copy(self, obj_copy, original_obj):
        """Register the object_copy => original object

        Args:
            obj_copy: a copy of the original object
            original_obj: the original object

        Returns: None

        """
        pass

    def get_original(self, obj_copy) -> Any:
        """Get the registered original object from the object copy.

        Args:
            obj_copy: a copy of the original object

        Returns: the original object if found; None otherwise.

        """
        pass

    def get_datums(self):
        pass

    def get_datum(self, datum_id: str):
        pass

    def externalize(self, data: Any):
        pass

    def internalize(self, data: Any) -> Any:
        pass
