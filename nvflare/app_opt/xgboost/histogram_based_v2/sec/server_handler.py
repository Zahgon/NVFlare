# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
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
import threading

from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_opt.xgboost.histogram_based_v2.defs import Constant
from nvflare.app_opt.xgboost.histogram_based_v2.sec.sec_handler import SecurityHandler

try:
    from nvflare.app_opt.he import decomposers

    tenseal_imported = True
except Exception:
    tenseal_imported = False


class ServerSecurityHandler(SecurityHandler):
    def __init__(self):
        FLComponent.__init__(self)
        self.encrypted_gh = None
        self.gh_source_rank = 0
        self.gh_seq = 0
        self.gh_original_buf_size = 0
        self.aggr_seq = 0
        self.aggr_result_dict = None
        self.aggr_result_to_send = None
        self.aggr_result_lock = threading.Lock()
        self.world_size = 0
        self.size_dict = None

        if tenseal_imported:
            decomposers.register()

    def _process_before_broadcast(self, fl_ctx: FLContext):
        pass

    def _process_after_broadcast(self, fl_ctx: FLContext):
        # this is called after the Server already received broadcast calls from all clients of the same sequence
        pass

    def _process_before_all_gather_v(self, fl_ctx: FLContext):
        pass

    def _process_after_all_gather_v(self, fl_ctx: FLContext):
        # this is called after the Server has finished gathering
        # Note: this fl_ctx is the same as the one in _process_before_all_gather_v!
        pass

    def _histogram_sum(self, fl_ctx: FLContext):

        pass
