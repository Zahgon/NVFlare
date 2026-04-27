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

import flwr.proto.grpcadapter_pb2 as pb2
from flwr.proto.grpcadapter_pb2_grpc import GrpcAdapterServicer

from nvflare.fuel.utils.log_utils import get_obj_logger


class EchoServicer(GrpcAdapterServicer):
    def __init__(self, num_rounds):
        self.logger = get_obj_logger(self)
        self.num_rounds = num_rounds
        self.server = None
        self.stopped = False

    def set_server(self, s):
        pass

    def SendReceive(self, request: pb2.MessageContainer, context):
        pass
