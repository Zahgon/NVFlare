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

from typing import List

from nvflare.fuel.common.ctx import BaseContext

from .proto import Buffer, ProtoKey
from .table import Table


class Connection(BaseContext):
    def __init__(self, app_ctx=None, props=None):
        """Object containing connection information and buffer to build and send a line with socket passed in at init."""
        BaseContext.__init__(self)
        self.app_ctx = app_ctx
        self.ended = False
        self.request = None
        self.command = None
        self.args = None
        self.buffer = Buffer()
        if props:
            self.set_props(props)

    def append_table(self, headers: List[str], name=None) -> Table:
        pass

    def append_string(self, data: str, meta: dict = None):
        pass

    def append_success(self, data: str, meta: dict = None):
        pass

    def append_dict(self, data: dict, meta: dict = None):
        pass

    def append_error(self, data: str, meta: dict = None):
        pass

    def append_command(self, cmd: str):
        pass

    def append_token(self, token: str):
        pass

    def append_shutdown(self, msg: str):
        pass

    def append_any(self, data, meta: dict = None):
        pass

    def update_meta(self, meta: dict):
        pass

    def close(self):
        pass

    def get_token(self):
        pass
