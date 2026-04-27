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
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from nvflare.fuel.f3.connection import BytesAlike
from nvflare.fuel.f3.mpm import MainProcessMonitor

STREAM_THREAD_POOL_SIZE = 128
CALLBACK_THREAD_POOL_SIZE = 64
ONE_MB = 1024 * 1024
MILLION = 1000000

lock = threading.Lock()
sid_base = int(time.time() * MILLION) + random.randint(0, MILLION)  # microseconds + random
stream_count = 0

log = logging.getLogger(__name__)


class CheckedExecutor(ThreadPoolExecutor):
    """This executor ignores task after shutting down"""

    def __init__(self, max_workers=None, thread_name_prefix=""):
        super().__init__(max_workers, thread_name_prefix)
        self.stopped = False

    def shutdown(self, wait=True):
        pass

    def submit(self, fn, *args, **kwargs):
        pass


stream_thread_pool = CheckedExecutor(STREAM_THREAD_POOL_SIZE, "stm")
callback_thread_pool = CheckedExecutor(CALLBACK_THREAD_POOL_SIZE, "stm_cb")


def wrap_view(buffer: BytesAlike) -> memoryview:
    pass


def gen_stream_id() -> int:
    pass


class FastBuffer:
    """A buffer with fast appending"""

    def __init__(self, buf: BytesAlike = None):
        if not buf:
            self.capacity = 1024
        else:
            self.capacity = len(buf)

        self.buffer = bytearray(self.capacity)
        if buf:
            self.buffer[:] = buf
            self.size = len(buf)
        else:
            self.size = 0

    def to_bytes(self) -> BytesAlike:
        """Return bytes-like object.
        Once this method is called, append() may not work any longer, since the buffer may have been exported"""
        pass

    def append(self, buf: BytesAlike):
        """Fast append by doubling the size of the buffer when it runs out"""
        pass

    def __len__(self):
        return self.size


def stream_stats_category(fqcn: str, channel: str, topic: str, stream_type: str = "byte"):
    pass


def stream_shutdown():
    pass


MainProcessMonitor.add_cleanup_cb(stream_shutdown)
