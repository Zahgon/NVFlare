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

import json
import uuid
from typing import Optional


class MsgHeader(object):

    REF_MSG_ID = "_refMsgId"
    RETURN_CODE = "_rtnCode"
    META = "_meta"


class ReturnCode(object):

    OK = "_ok"
    ERROR = "_error"


class Message(object):
    def __init__(self, topic: str, body):
        """To init a Message.

        Args:
            topic: message topic
            body: message body.
        """
        self.id = str(uuid.uuid4())
        self.topic = topic
        self.body = body
        self.headers = {}

    def set_header(self, key, value):
        pass

    def set_meta(self, meta: dict):
        pass

    def get_meta(self):
        pass

    def set_headers(self, headers: dict):
        pass

    def get_header(self, key, default=None):
        pass

    def get_ref_id(self, default=None):
        pass

    def set_ref_id(self, msg_id):
        pass


def error_reply(err: str, meta: Optional[dict] = None) -> Message:
    pass


def ok_reply(topic=None, body=None, meta: Optional[dict] = None) -> Message:
    pass
