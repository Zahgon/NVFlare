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
import copy
import threading
from typing import Any, Dict, List

from nvflare.fuel.utils.log_utils import get_obj_logger

from .fl_constant import ReservedKey

# Lock-ordering rule: always acquire _update_lock (module-level FLContext lock)
# before FLContextManager._update_lock. Never invert this order (e.g. set_prop
# holds _update_lock and then calls ctx_manager.update_sticker).
_update_lock = threading.Lock()

MASK_STICKY = 1 << 0
MASK_PRIVATE = 1 << 1

V = "value"
M = "mask"


def is_sticky(mask) -> bool:
    pass


def is_private(mask) -> bool:
    pass


def make_mask(private, sticky):
    pass


def to_string(mask) -> str:
    pass


class FLContext(object):
    def __init__(self):
        """Init the FLContext.

        The FLContext is used to passed data between FL Components.
        It can be thought of as a dictionary that stores key/value pairs called props (properties).

        Visibility: private props are only visible to local components,
                    public props are also visible to remote components

        Stickiness: sticky props become available in all future FL Contexts,
                    non-sticky props will only be available in the current FL Context

        """
        self.model = None
        self.props = {}
        self.logger = get_obj_logger(self)

    def get_prop_keys(self) -> List[str]:
        pass

    def public_key_exists(self, key) -> bool:
        pass

    def get_all_public_props(self) -> Dict[str, Any]:
        pass

    def _get_ctx_manager(self):
        pass

    def _get_prop(self, key: str) -> (bool, Any):
        """
        Get the prop with the specified key.
        If the property is sticky, its value will be retrieved from the base (the ctx manager)

        Args:
            key: key of the property

        Returns: tuple: whether the property exists, and the value of the prop if exists.

        """
        pass

    def set_prop(self, key: str, value, private=True, sticky=True):
        pass

    def get_prop(self, key, default=None):
        pass

    def get_custom_prop(self, key: str, default=None):
        pass

    def set_custom_prop(self, key: str, value):
        pass

    def get_prop_detail(self, key):
        pass

    def remove_prop(self, key: str, force_removal=False):
        pass

    def __str__(self):
        raw_list = [f"{k}: {type(v[V])}" for k, v in self.props.items()]
        return " ".join(raw_list)

    # some convenience methods
    def _simple_get(self, key: str, default=None):
        pass

    def get_engine(self, default=None):
        pass

    def get_workspace(self):
        pass

    def get_process_type(self, default=None):
        pass

    def get_job_id(self, default=None):
        pass

    def get_identity_name(self, default=""):
        pass

    def set_job_is_unsafe(self, value: bool = True):
        pass

    def is_job_unsafe(self):
        pass

    def get_run_abort_signal(self):
        pass

    def set_peer_context(self, ctx):
        pass

    def get_peer_context(self):
        pass

    def set_public_props(self, metadata: dict):
        # remove all public props
        pass

    def sync_sticky(self):
        # no longer needed since sticky props are always synced
        pass

    def put(self, key: str, value, private, sticky):
        """
        Simply put the prop into the fl context without doing sticky property processing
        Args:
            key:
            value:
            private:
            sticky:

        Returns:

        """
        pass

    def clone(self):
        """Make a copy from self.

        Returns: a new FLContext object

        """
        pass

    # implement Context Manager protocol
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # no longer needed since sticky props are always synced
        pass


class FLContextManager(object):
    """FLContextManager manages the creation and updates of FLContext objects for a run.

    NOTE: The engine may create a new FLContextManager object for each RUN!

    """

    def __init__(
        self, engine=None, identity_name: str = "", job_id: str = "", public_stickers=None, private_stickers=None
    ):
        """Init the FLContextManager.

        Args:
            engine: the engine that created this FLContextManager object
            identity_name (str): identity name
            job_id: the job id
            public_stickers: public sticky properties that are copied into or copied from
            private_stickers: private sticky properties that are copied into or copied from
        """
        self.engine = engine
        self.identity_name = identity_name
        self.job_id = job_id
        self._update_lock = threading.Lock()

        self.public_stickers = {}
        self.private_stickers = {}

        if public_stickers and isinstance(public_stickers, dict):
            self.public_stickers.update(public_stickers)

        if private_stickers and isinstance(private_stickers, dict):
            self.private_stickers.update(private_stickers)

    def new_context(self) -> FLContext:
        """Create a new FLContext object.

        Sticky properties are copied from the stickers into the new context.

        Returns: a FLContext object

        """
        pass

    @staticmethod
    def _get_sticker(stickers, key) -> (bool, Any):
        """
        Get sticker with specified key

        Args:
            stickers:
            key:

        Returns: tuple: whether the sticker exists, value of the sticker if exists

        """
        pass

    def check_sticker(self, key: str) -> (bool, Any, int):
        """
        Check whether a sticky prop exists in either the public or private group.

        Args:
            key: the key of the sticker to be checked

        Returns: tuple: whether the sticker exists, its value and mask if it exists

        """
        pass

    def update_sticker(self, key: str, value, mask):
        """
        Update the value of a specified sticker.

        Args:
            key: key of the sticker to be updated
            value: value of the sticker
            mask: mask to determine whether the sticker is public or private

        Returns:

        """
        pass
