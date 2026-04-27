# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
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
import threading

from nvflare.apis.fl_constant import FLContextKey, SecureTrainConst
from nvflare.apis.fl_context import FLContext
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.private.fed.utils.identity_utils import IdentityAsserter, IdentityVerifier


class CredKeeper:

    def __init__(self):
        self.id_verifier = None
        self.id_asserter = None
        self.logger = get_obj_logger(self)
        self._lock = threading.Lock()

    def _get_server_config(self, fl_ctx: FLContext):
        pass

    def get_id_verifier(self, fl_ctx: FLContext):
        pass

    def get_id_asserter(self, fl_ctx: FLContext):
        pass
