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
import json
import time

import nvflare.app_opt.xgboost.histogram_based_v2.proto.federated_pb2 as pb2
from nvflare.apis.fl_component import FLComponent
from nvflare.app_opt.xgboost.histogram_based_v2.defs import Constant
from nvflare.app_opt.xgboost.histogram_based_v2.grpc_client import GrpcClient
from nvflare.app_opt.xgboost.histogram_based_v2.runners.xgb_runner import AppRunner


def encode_msg(msg: dict):
    pass


class MockSecureClientRunner(AppRunner, FLComponent):
    def __init__(self, sample_size=1000):
        FLComponent.__init__(self)
        self.training_stopped = False
        self.asked_to_stop = False
        self.sample_size = sample_size

    def run(self, ctx: dict):
        pass

    def stop(self):
        pass

    def is_stopped(self) -> (bool, int):
        pass
