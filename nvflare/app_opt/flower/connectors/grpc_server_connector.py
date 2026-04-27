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

from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReturnCode, Shareable, make_reply
from nvflare.app_opt.flower.connectors.flower_connector import FlowerServerConnector
from nvflare.app_opt.flower.defs import Constant
from nvflare.app_opt.flower.grpc_client import GrpcClient
from nvflare.app_opt.flower.utils import msg_container_to_shareable, shareable_to_msg_container
from nvflare.fuel.utils.network_utils import get_local_addresses
from nvflare.security.logging import secure_format_exception


class GrpcServerConnector(FlowerServerConnector):
    def __init__(
        self,
        int_client_grpc_options=None,
        flower_server_ready_timeout=Constant.FLOWER_SERVER_READY_TIMEOUT,
        monitor_interval: float = 1.0,
    ):
        FlowerServerConnector.__init__(self, monitor_interval)
        self.int_client_grpc_options = int_client_grpc_options
        self.flower_server_ready_timeout = flower_server_ready_timeout
        self.internal_grpc_client = None
        self._server_stopped = False
        self._exit_code = 0

    def _start_server(self, serverapp_api_addr: str, fleet_api_addr: str, exec_api_addr: str, fl_ctx: FLContext):
        pass

    def _stop_server(self):
        pass

    def _is_stopped(self) -> (bool, int):
        pass

    def start(self, fl_ctx: FLContext):
        # we dynamically create server address on localhost
        # we need 3 free local addresses for flwr's superlink:
        # - address for client to connect to (fleet-api-address)
        # - address for serverapp to connect to (serverapp-api-address)
        # - address for "flwr run" to connect to (control-api-address)
        pass

    def stop(self, fl_ctx: FLContext):
        pass

    def send_request_to_flower(self, request: Shareable, fl_ctx: FLContext) -> Shareable:
        """Send the request received from FL client to Flower server.

        This is done by:
        1. convert the request to Flower-defined MessageContainer object
        2. Send the MessageContainer object to Flower server via the internal GRPC client (LGC)
        3. Convert the reply MessageContainer object received from the Flower server to Shareable
        4. Return the reply Shareable object

        Args:
            request: the request received from FL client
            fl_ctx: FL context

        Returns: response from Flower server converted to Shareable

        """
        pass
