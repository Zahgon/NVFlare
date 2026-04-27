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
import logging

from nvflare.fuel.f3.connection import BytesAlike
from nvflare.fuel.f3.streaming.stream_utils import wrap_view

BUF_SIZE = 64 * 1024 * 1024 + 1
TEST_CHANNEL = "stream"
TEST_TOPIC = "test"
TX_CELL = "sender"
RX_CELL = "server"  # Passive cell's fqcn must be "server"
TIMESTAMP = "timestamp"


def make_buffer(size: int) -> BytesAlike:
    """
    Make a buffer of size bytes with fixed data pattern for easy debugging.

    :param size:
    :return:
    """
    pass


def setup_log(level):
    pass
