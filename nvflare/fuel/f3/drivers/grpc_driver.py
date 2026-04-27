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

import os
import threading
from concurrent import futures
from typing import Any, Dict, List, Union

import grpc

from nvflare.fuel.f3.comm_config import CommConfigurator
from nvflare.fuel.f3.comm_config_utils import requires_secure_connection
from nvflare.fuel.f3.comm_error import CommError
from nvflare.fuel.f3.connection import Connection
from nvflare.fuel.f3.drivers.driver import ConnectorInfo
from nvflare.fuel.f3.drivers.grpc.streamer_pb2_grpc import (
    StreamerServicer,
    StreamerStub,
    add_StreamerServicer_to_server,
)
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.security.logging import secure_format_exception

from .base_driver import BaseDriver
from .driver_params import DriverCap, DriverParams
from .grpc.qq import QQ
from .grpc.streamer_pb2 import Frame
from .grpc.utils import get_grpc_client_credentials, get_grpc_server_credentials, use_aio_grpc
from .net_utils import MAX_FRAME_SIZE, get_address, get_tcp_urls, ssl_required

GRPC_DEFAULT_OPTIONS = [
    ("grpc.max_send_message_length", MAX_FRAME_SIZE),
    ("grpc.max_receive_message_length", MAX_FRAME_SIZE),
]


class StreamConnection(Connection):

    seq_num = 0

    def __init__(self, oq: QQ, connector: ConnectorInfo, conn_props: dict, side: str, context=None, channel=None):
        super().__init__(connector)
        self.side = side
        self.oq = oq
        self.closing = False
        self.conn_props = conn_props
        self.context = context  # for server side
        self.channel = channel  # for client side
        self.lock = threading.Lock()
        self.logger = get_obj_logger(self)

    def get_conn_properties(self) -> dict:
        pass

    def close(self):
        pass

    def send_frame(self, frame: Union[bytes, bytearray, memoryview]):
        pass

    def read_loop(self, msg_iter):
        pass

    def generate_output(self):
        pass


class Servicer(StreamerServicer):
    def __init__(self, server):
        self.server = server
        self.logger = get_obj_logger(self)

    def Stream(self, request_iterator, context):
        pass


class Server:
    def __init__(
        self,
        driver,
        connector,
        max_workers,
        options,
    ):
        self.driver = driver
        self.logger = get_obj_logger(self)
        self.connector = connector
        self.grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers), options=options)
        servicer = Servicer(self)
        add_StreamerServicer_to_server(servicer, self.grpc_server)

        params = connector.params
        addr = get_address(params)
        try:
            self.logger.debug(f"SERVER: connector params: {params}")
            secure = ssl_required(params)
            if secure:
                credentials = get_grpc_server_credentials(params)
                self.grpc_server.add_secure_port(addr, server_credentials=credentials)
                self.logger.info(f"added secure port at {addr}")
            else:
                self.grpc_server.add_insecure_port(addr)
                self.logger.info(f"added insecure port at {addr}")
        except Exception as ex:
            error = f"cannot listen on {addr}: {type(ex)}: {secure_format_exception(ex)}"
            self.logger.debug(error)

    def start(self):
        pass

    def shutdown(self):
        pass


class GrpcDriver(BaseDriver):
    def __init__(self):
        BaseDriver.__init__(self)

        self.setup_grpc_env_var()

        self.server = None
        self.closing = False
        self.max_workers = 100
        self.options = GRPC_DEFAULT_OPTIONS
        self.logger = get_obj_logger(self)
        configurator = CommConfigurator()
        config = configurator.get_config()
        if config:
            my_params = config.get("grpc")
            if my_params:
                self.max_workers = my_params.get("max_workers", 100)
                self.options = my_params.get("options")
        self.logger.debug(f"GRPC Config: max_workers={self.max_workers}, options={self.options}")

    @staticmethod
    def supported_transports() -> List[str]:
        pass

    @staticmethod
    def capabilities() -> Dict[str, Any]:
        pass

    def listen(self, connector: ConnectorInfo):
        pass

    def connect(self, connector: ConnectorInfo):
        pass

    @staticmethod
    def get_urls(scheme: str, resources: dict) -> (str, str):
        pass

    def shutdown(self):
        pass

    @staticmethod
    def setup_grpc_env_var():
        pass
