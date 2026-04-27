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
import os
import signal
import threading
import time

from nvflare.apis.fl_constant import FLMetaKey
from nvflare.fuel.common.excepts import ComponentNotAuthorized, ConfigError
from nvflare.fuel.common.exit_codes import ProcessExitCode
from nvflare.fuel.f3.drivers.aio_context import AioContext
from nvflare.fuel.utils.log_utils import get_module_logger
from nvflare.security.logging import secure_format_exception, secure_format_traceback


class MainProcessMonitor:
    """MPM (Main Process Monitor). It's used to run main thread and to handle graceful shutdown"""

    name = "MPM"
    _cleanup_cbs = []
    _stopping = False
    _logger = None
    _aio_ctx = None

    @classmethod
    def set_name(cls, name: str):
        pass

    @classmethod
    def is_stopping(cls):
        pass

    @classmethod
    def get_aio_context(cls):
        pass

    @classmethod
    def logger(cls):
        pass

    @classmethod
    def add_cleanup_cb(cls, cb, *args, **kwargs):
        pass

    @classmethod
    def _call_cb(cls, t: tuple):
        pass

    @classmethod
    def _start_shutdown(cls, shutdown_grace_time, cleanup_grace_time):
        pass

    @classmethod
    def _cleanup_one_round(cls, cbs):
        pass

    @classmethod
    def _do_cleanup(cls, waiter: threading.Event):
        pass

    @classmethod
    def run(cls, main_func, run_dir=None, shutdown_grace_time=3, cleanup_grace_time=3, **kwargs):
        pass
