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

from typing import Tuple

import nvflare.app_opt.xgboost.histogram_based_v2.proto.federated_pb2 as pb2
from nvflare.apis.fl_context import FLContext
from nvflare.app_opt.xgboost.histogram_based_v2.adaptors.xgb_adaptor import XGBServerAdaptor
from nvflare.app_opt.xgboost.histogram_based_v2.defs import Constant
from nvflare.app_opt.xgboost.histogram_based_v2.grpc_client import GrpcClient
from nvflare.fuel.f3.drivers.net_utils import get_open_tcp_port


class GrpcServerAdaptor(XGBServerAdaptor):
    """Implementation of XGBServerAdaptor that uses an internal `GrpcClient`.

    The `GrpcServerAdaptor` class serves as an interface between the XGBoost
    federated client and federated server components.
    It employs its `XGBRunner` to initiate an XGBoost federated gRPC server
    and utilizes an internal `GrpcClient` to forward client requests/responses.

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

    def __init__(
        self,
        int_client_grpc_options=None,
        xgb_server_ready_timeout=Constant.XGB_SERVER_READY_TIMEOUT,
        in_process=True,
    ):
        """Constructor method to initialize the object.

        Args:
            int_client_grpc_options: An optional list of key-value pairs (`channel_arguments`
                in gRPC Core runtime) to configure the gRPC channel of internal `GrpcClient`.
            in_process (bool): Specifies whether to call the `AppRunner.run()` in the same process or not.
            xgb_server_ready_timeout (float): Duration for which the internal `GrpcClient`
                should wait for the XGBoost gRPC server before timing out.
        """
        XGBServerAdaptor.__init__(self, in_process)
        self.int_client_grpc_options = int_client_grpc_options
        self.xgb_server_ready_timeout = xgb_server_ready_timeout
        self.in_process = in_process
        self.internal_xgb_client = None
        self._server_stopped = False
        self._exit_code = 0
        self._stopping = False

    def _start_server(self, addr: str, port: int, world_size: int, fl_ctx: FLContext):
        pass

    def _stop_server(self):
        pass

    def _is_stopped(self) -> Tuple[bool, int]:
        pass

    def start(self, fl_ctx: FLContext):
        # we dynamically create server address on localhost
        pass

    def stop(self, fl_ctx: FLContext):
        pass

    def all_gather(self, rank: int, seq: int, send_buf: bytes, fl_ctx: FLContext) -> bytes:
        pass

    def all_gather_v(self, rank: int, seq: int, send_buf: bytes, fl_ctx: FLContext) -> bytes:
        pass

    def all_reduce(
        self,
        rank: int,
        seq: int,
        data_type: int,
        reduce_op: int,
        send_buf: bytes,
        fl_ctx: FLContext,
    ) -> bytes:
        pass

    def broadcast(self, rank: int, seq: int, root: int, send_buf: bytes, fl_ctx: FLContext) -> bytes:
        pass

    def _handle_error(self, ex: Exception, op: str, rank: int, seq: int, send_buf: bytes) -> bytes:
        pass
