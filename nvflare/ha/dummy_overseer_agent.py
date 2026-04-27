# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
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
import threading
import time

from requests import Response

from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.overseer_spec import SP, OverseerAgent


class DummyOverseerAgent(OverseerAgent):
    SSID = "ebc6125d-0a56-4688-9b08-355fe9e4d61a"

    def __init__(self, sp_end_point, heartbeat_interval=0.5):
        super().__init__()
        self._base_init(sp_end_point)

        self._report_and_query = threading.Thread(target=self._rnq_worker, args=())
        self._report_and_query.daemon = True
        self._flag = threading.Event()
        self._asked_to_exit = False
        self._update_callback = None
        self._conditional_cb = False
        self._heartbeat_interval = heartbeat_interval

    def _base_init(self, sp_end_point):
        pass

    def initialize(self, fl_ctx: FLContext):
        pass

    def is_shutdown(self) -> bool:
        """Return whether the agent receives a shutdown request."""
        pass

    def get_primary_sp(self) -> SP:
        """Return current primary service provider. The PSP is static in the dummy agent."""
        pass

    def promote_sp(self, sp_end_point, headers=None) -> Response:
        # a hack to create dummy response
        pass

    def start(self, update_callback=None, conditional_cb=False):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def set_state(self, state) -> Response:
        # a hack to create dummy response
        pass

    def end(self):
        pass
        # self._report_and_query.join()

    def set_secure_context(self, ca_path: str, cert_path: str = "", prv_key_path: str = ""):
        pass

    def _do_callback(self):
        pass

    def _rnq_worker(self):
        pass
