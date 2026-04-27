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

import threading

import nvflare.app_opt.xgboost.histogram_based_v2.proto.federated_pb2 as pb2
from nvflare.app_opt.xgboost.histogram_based_v2.proto.federated_pb2_grpc import FederatedServicer
from nvflare.fuel.utils.log_utils import get_obj_logger


class ReqWaiter:
    def __init__(self, exp_num_clients: int, exp_seq: int, exp_op):
        self.exp_num_clients = exp_num_clients
        self.exp_seq = exp_seq
        self.exp_op = exp_op
        self.reqs = {}
        self.result = {}
        self.waiter = threading.Event()

    def add_request(self, op: str, rank, seq, req):
        pass

    def wait(self, timeout):
        pass


class AggrServicer(FederatedServicer):
    def __init__(self, num_clients, aggr_timeout=10.0):
        self.logger = get_obj_logger(self)
        self.num_clients = num_clients
        self.aggr_timeout = aggr_timeout
        self.req_lock = threading.Lock()
        self.req_waiter = None

    def _wait_for_result(self, op, rank, seq, request):
        pass

    def Allgather(self, request: pb2.AllgatherRequest, context):
        pass

    def AllgatherV(self, request: pb2.AllgatherVRequest, context):
        pass

    def Allreduce(self, request: pb2.AllreduceRequest, context):
        pass

    def Broadcast(self, request: pb2.BroadcastRequest, context):
        pass
