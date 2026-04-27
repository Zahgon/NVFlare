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
import asyncio
import os
import threading
import time

from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.security.logging import secure_format_exception


class AioContext:
    """Asyncio context. Used to share the asyncio event loop among multiple classes"""

    _ctx_lock = threading.Lock()
    _global_ctx = None

    def __init__(self, name):
        self.closed = False
        self.name = name
        self.loop = None
        self.ready = threading.Event()
        self.logger = get_obj_logger(self)
        self.logger.debug(f"{os.getpid()}: ******** Created AioContext {name}")

    def get_event_loop(self):
        pass

    def _handle_exception(self, loop, context):
        pass

    def run_aio_loop(self):
        pass

    def run_coro(self, coro):
        pass

    def stop_aio_loop(self, grace=1.0):
        pass

    @classmethod
    def get_global_context(cls):
        pass

    @classmethod
    def close_global_context(cls):
        pass
