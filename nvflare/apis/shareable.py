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
from typing import Optional

from ..fuel.utils import fobs
from .fl_constant import ReservedKey, ReturnCode, ServerCommandKey


class ReservedHeaderKey(object):

    HEADERS = "__headers__"
    TOPIC = "__topic__"
    RC = ReservedKey.RC
    COOKIE_JAR = ReservedKey.COOKIE_JAR
    PEER_PROPS = "__peer_props__"
    REPLY_IS_LATE = "__reply_is_late__"
    TASK_NAME = ReservedKey.TASK_NAME
    TASK_ID = ReservedKey.TASK_ID
    WORKFLOW = ReservedKey.WORKFLOW
    AUDIT_EVENT_ID = ReservedKey.AUDIT_EVENT_ID
    CONTENT_TYPE = "__content_type__"
    TASK_OPERATOR = "__task_operator__"
    ERROR = "__error__"
    PEER_CTX = ServerCommandKey.PEER_FL_CONTEXT
    MSG_ROOT_ID = "__msg_root_id__"
    MSG_ROOT_TTL = "__msg_root_ttl__"  # TTL = time to live
    PASS_THROUGH = "__pass_through__"  # request PASS_THROUGH decode at receiving CJ


class Shareable(dict):
    """The information communicated between server and client.

    Shareable is just a dict that can have any keys and values, defined by developers and users.
    It is recommended that keys are strings. Values must be serializable.
    """

    def __init__(self, data: Optional[dict] = None):
        """Init the Shareable."""
        super().__init__()
        if data:
            self.update(data)
        self[ReservedHeaderKey.HEADERS] = {}

    def set_header(self, key: str, value):
        pass

    def get_header(self, key: str, default=None):
        pass

    # some convenience methods
    def get_return_code(self, default=ReturnCode.OK):
        pass

    def set_return_code(self, rc):
        pass

    def add_cookie(self, name: str, data):
        """Add a cookie that is to be sent to the client and echoed back in response.

        This method is intended to be called by the Server side.

        Args:
            name: the name of the cookie
            data: the data of the cookie, which must be serializable

        """
        pass

    def get_cookie_jar(self):
        pass

    def set_cookie_jar(self, jar):
        pass

    def get_cookie(self, name: str, default=None):
        pass

    def set_peer_props(self, props: dict):
        pass

    def get_peer_props(self):
        pass

    def get_peer_prop(self, key: str, default):
        pass

    def set_peer_context(self, peer_ctx):
        pass

    def get_peer_context(self):
        pass

    def to_bytes(self) -> bytes:
        """Serialize the Model object into bytes.

        Returns:
            object serialized in bytes.

        """
        pass

    @classmethod
    def from_bytes(cls, data: bytes):
        """Convert the data bytes into Model object.

        Args:
            data: a bytes object

        Returns:
            an object loaded by FOBS from data

        """
        pass


# some convenience functions
def make_reply(rc, headers=None) -> Shareable:
    pass


def make_copy(source: Shareable, exclude_headers: list = None) -> Shareable:
    """
    Make a copy from the source.
    The content (non-headers) will be kept intact. Headers will be deep-copied into the new instance.
    """
    pass
