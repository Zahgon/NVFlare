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
import time
from typing import Tuple

import grpc

import nvflare.app_opt.xgboost.histogram_based_v2.proto.federated_pb2 as pb2
from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.app_opt.xgboost.histogram_based_v2.adaptors.xgb_adaptor import XGBClientAdaptor
from nvflare.app_opt.xgboost.histogram_based_v2.defs import Constant
from nvflare.app_opt.xgboost.histogram_based_v2.grpc_server import GrpcServer
from nvflare.app_opt.xgboost.histogram_based_v2.proto.federated_pb2_grpc import FederatedServicer
from nvflare.fuel.f3.drivers.net_utils import get_open_tcp_port
from nvflare.security.logging import secure_format_exception

DUPLICATE_REQ_MAX_HOLD_TIME = 3600.0


class GrpcClientAdaptor(XGBClientAdaptor, FederatedServicer):
    """Implementation of XGBClientAdaptor that uses an internal `GrpcServer`.

    The `GrpcClientAdaptor` class serves as an interface between the XGBoost
    federated client and federated server components.
    It employs its `XGBRunner` to initiate an XGBoost federated gRPC client
    and utilizes an internal `GrpcServer` to forward client requests/responses.

    The communication flow is as follows:
        1. XGBoost federated gRPC client talks to `GrpcClientAdaptor`, which
           encapsulates a `GrpcServer`.
           Requests are then forwarded to `GrpcServerAdaptor`, which internally
           manages a `GrpcClient` responsible for interacting with the XGBoost
           federated gRPC server.
        2. XGBoost federated gRPC server talks to `GrpcServerAdaptor`, which
           encapsulates a `GrpcClient`.
           Responses are then forwarded to `GrpcClientAdaptor`, which internally
           manages a `GrpcServer` responsible for interacting with the XGBoost
           federated gRPC client.
    """

    def __init__(self, int_server_grpc_options=None, in_process=True, per_msg_timeout=10.0, tx_timeout=100.0):
        """Constructor method to initialize the object.

        Args:
            int_server_grpc_options: An optional list of key-value pairs (`channel_arguments`
                in gRPC Core runtime) to configure the gRPC channel of internal `GrpcServer`.
            in_process (bool): Specifies whether to start the `XGBRunner` in the same process or not.
        """
        XGBClientAdaptor.__init__(self, in_process, per_msg_timeout, tx_timeout)
        self.int_server_grpc_options = int_server_grpc_options
        self.in_process = in_process
        self.internal_xgb_server = None
        self.stopped = False
        self.internal_server_addr = None
        self._training_stopped = False
        self._client_name = None
        self._workspace = None
        self._run_dir = None
        self._lock = threading.Lock()
        self._pending_req = {}

    def initialize(self, fl_ctx: FLContext):
        pass

    def _start_client(self, server_addr: str, fl_ctx: FLContext):
        """Start the XGB client runner in a separate thread or separate process based on config.
        Note that when starting runner in a separate process, we must not call a method defined in this
        class since the self object contains a sender that contains a Core Cell which cannot be sent to
        the new process. Instead, we use a small _ClientStarter object to run the process.

        Args:
            server_addr: the internal gRPC server address that the XGB client will connect to

        Returns: None

        """
        pass

    def _stop_client(self):
        pass

    def _is_stopped(self) -> Tuple[bool, int]:
        pass

    def start(self, fl_ctx: FLContext):
        pass

    def stop(self, fl_ctx: FLContext):
        pass

    def _abort(self, reason: str):
        # stop the gRPC XGB client (the target)
        pass

    def Allgather(self, request: pb2.AllgatherRequest, context):
        pass

    def AllgatherV(self, request: pb2.AllgatherVRequest, context):
        pass

    def Allreduce(self, request: pb2.AllreduceRequest, context):
        pass

    def Broadcast(self, request: pb2.BroadcastRequest, context):
        pass

    def _check_duplicate_seq(self, op: str, rank: int, seq: int):
        pass

    def _finish_pending_req(self, op: str, rank: int, seq: int):
        pass
