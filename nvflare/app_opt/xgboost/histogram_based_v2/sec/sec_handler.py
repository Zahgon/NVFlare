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
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.app_opt.xgboost.histogram_based_v2.defs import Constant


class SecurityHandler(FLComponent):
    def _process_before_broadcast(self, fl_ctx: FLContext):
        pass

    def _process_after_broadcast(self, fl_ctx: FLContext):
        pass

    def _process_before_all_gather_v(self, fl_ctx: FLContext):
        pass

    def _process_after_all_gather_v(self, fl_ctx: FLContext):
        pass

    def _format_msg(self, fl_ctx: FLContext, msg: str):
        pass

    def info(self, fl_ctx: FLContext, msg: str):
        pass

    def debug(self, fl_ctx: FLContext, msg: str):
        pass

    def error(self, fl_ctx: FLContext, msg: str):
        pass

    def _abort(self, error: str, fl_ctx: FLContext):
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass
