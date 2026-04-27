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
import threading
import time

import flwr.proto.grpcadapter_pb2 as pb2
from flwr.proto.grpcadapter_pb2_grpc import GrpcAdapterServicer

from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReturnCode
from nvflare.app_opt.flower.connectors.flower_connector import FlowerClientConnector
from nvflare.app_opt.flower.defs import Constant
from nvflare.app_opt.flower.grpc_server import GrpcServer
from nvflare.app_opt.flower.utils import msg_container_to_shareable, reply_should_exit, shareable_to_msg_container
from nvflare.fuel.utils.network_utils import get_local_addresses
from nvflare.security.logging import secure_format_exception


class GrpcClientConnector(FlowerClientConnector, GrpcAdapterServicer):
    def __init__(
        self,
        int_server_grpc_options=None,
        per_msg_timeout=2.0,
        tx_timeout=10.0,
        client_shutdown_timeout=0.5,
    ):
        """Constructor of GrpcClientConnector.
        GrpcClientConnector is used to connect Flare Client with the Flower Client App.

        Args:
            int_server_grpc_options: internal grpc server options
            per_msg_timeout: per-message timeout for using ReliableMessage
            tx_timeout: transaction timeout for using ReliableMessage
            client_shutdown_timeout: max time for shutting down Flare client
        """
        FlowerClientConnector.__init__(self, per_msg_timeout, tx_timeout)
        self.client_shutdown_timeout = client_shutdown_timeout
        self.int_server_grpc_options = int_server_grpc_options
        self.internal_grpc_server = None
        self.stopped = False
        self.internal_server_addr = None
        self._training_stopped = False
        self._client_name = None
        self._stopping = False
        self._exit_waiter = threading.Event()

    def initialize(self, fl_ctx: FLContext):
        pass

    def _start_client(self, superlink_addr: str, clientapp_api_addr: str, fl_ctx: FLContext):
        pass

    def _stop_client(self):
        pass

    def _is_stopped(self) -> (bool, int):
        pass

    def start(self, fl_ctx: FLContext):
        pass

    def stop(self, fl_ctx: FLContext):
        pass

    def _abort(self, reason: str):
        # stop the gRPC client (the target)
        pass

    def SendReceive(self, request: pb2.MessageContainer, context):
        """Process request received from a Flower client.

        This implements the SendReceive method required by Flower gRPC server (LGS on FLARE Client).
        1. convert the request to a Shareable object.
        2. send the Shareable request to FLARE server.
        3. convert received Shareable result to MessageContainer and return to the Flower client

        Args:
            request: the request received from the Flower client
            context: gRPC context

        Returns: the reply MessageContainer object

        """
        pass
