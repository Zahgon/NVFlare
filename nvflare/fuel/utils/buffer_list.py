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


class BufferList:
    """A buffer list that can be treated as a single buffer"""

    def __init__(self, buf_list: list):
        self.buf_list = buf_list

    def get_size(self):

        pass

    def get_list(self):
        pass

    def append(self, buf: bytes):
        pass

    def read(self, start: int, end: int):

        pass

    def flatten(self):

        pass
