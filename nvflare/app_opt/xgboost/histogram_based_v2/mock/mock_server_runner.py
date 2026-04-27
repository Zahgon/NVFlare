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
from nvflare.app_opt.xgboost.histogram_based_v2.defs import Constant
from nvflare.app_opt.xgboost.histogram_based_v2.grpc_server import GrpcServer
from nvflare.app_opt.xgboost.histogram_based_v2.mock.aggr_servicer import AggrServicer
from nvflare.app_opt.xgboost.histogram_based_v2.runners.xgb_runner import AppRunner


class MockServerRunner(AppRunner):
    def __init__(self, server_max_workers=10, aggr_timeout=10.0):
        self.server_max_workers = server_max_workers
        self.aggr_timeout = aggr_timeout
        self._stopped = False
        self._server = None

    def run(self, ctx: dict):
        pass

    def stop(self):
        pass

    def is_stopped(self) -> (bool, int):
        pass
