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

import asyncio
import random
import threading
import time
from typing import Any, Dict, List

import grpc

from nvflare.fuel.f3.comm_config import CommConfigurator
from nvflare.fuel.f3.comm_config_utils import requires_secure_connection
from nvflare.fuel.f3.comm_error import CommError
from nvflare.fuel.f3.connection import BytesAlike, Connection
from nvflare.fuel.f3.drivers.aio_context import AioContext
from nvflare.fuel.f3.drivers.driver import ConnectorInfo
from nvflare.fuel.f3.drivers.grpc.streamer_pb2_grpc import (
    StreamerServicer,
    StreamerStub,
    add_StreamerServicer_to_server,
)
from nvflare.fuel.f3.drivers.grpc_driver import GrpcDriver
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.security.logging import secure_format_exception, secure_format_traceback

from .base_driver import BaseDriver
from .driver_params import DriverCap, DriverParams
from .grpc.streamer_pb2 import Frame
from .grpc.utils import get_grpc_client_credentials, get_grpc_server_credentials, use_aio_grpc
from .net_utils import MAX_FRAME_SIZE, get_address, get_tcp_urls, ssl_required

GRPC_DEFAULT_OPTIONS = [
    ("grpc.max_send_message_length", MAX_FRAME_SIZE),
    ("grpc.max_receive_message_length", MAX_FRAME_SIZE),
]


class _ConnCtx:
    def __init__(self):
        self.conn = None
        self.error = None
        self.waiter = threading.Event()


class AioStreamSession(Connection):

    seq_num = 0

    def __init__(self, aio_ctx: AioContext, connector: ConnectorInfo, conn_props: dict, context=None, channel=None):
        super().__init__(connector)
        self.aio_ctx = aio_ctx
        self.logger = get_obj_logger(self)

        self.oq = asyncio.Queue(16)
        self.closing = False
        self.conn_props = conn_props
        self.context = context  # for server side
        self.channel = channel  # for client side
        self.read_task = None
        self.lock = threading.Lock()

        conf = CommConfigurator()
        if conf.get_bool_var("simulate_unstable_network", default=False):
            if context:
                # only server side
                self.disconn = threading.Thread(target=self._disconnect, name="grpc_disc", daemon=True)
                self.disconn.start()

    def _disconnect(self):
        pass

    def get_conn_properties(self) -> dict:
        pass

    async def _abort(self):
        pass

    def close(self):
        pass

    def send_frame(self, frame: BytesAlike):
        pass

    async def read_loop(self, msg_iter):
        pass

    async def generate_output(self):
        pass

    async def read_oq(self):
        # self.oq.get() does not return before an item is placed into the queue. This could cause it to wait for
        # a long time. If the connection is closed during this time, the coro won't be done immediately.
        # To be able to cancel the queue read operation, we wrap it into a task so that we can cancel it when
        # closing the connection. Once cancelled, "await task" will finish with asyncio.CancelledError exception.
        pass


class Servicer(StreamerServicer):
    def __init__(self, server, aio_ctx: AioContext):
        self.server = server
        self.aio_ctx = aio_ctx
        self.logger = get_obj_logger(self)

    async def Stream(self, request_iterator, context):
        pass


class Server:
    def __init__(self, driver, connector, aio_ctx: AioContext, options, conn_ctx: _ConnCtx):
        self.logger = get_obj_logger(self)
        self.driver = driver
        self.connector = connector
        self.grpc_server = grpc.aio.server(options=options)
        self.grpc_server_stop_grace = 0.5
        servicer = Servicer(self, aio_ctx)
        add_StreamerServicer_to_server(servicer, self.grpc_server)
        params = connector.params
        addr = get_address(params)
        try:
            self.logger.debug(f"SERVER: connector params: {params}")

            secure = ssl_required(params)
            if secure:
                credentials = get_grpc_server_credentials(params)
                self.grpc_server.add_secure_port(addr, server_credentials=credentials)
                self.logger.info(f"AIO_GRPC: added secure port at {addr}")
            else:
                self.grpc_server.add_insecure_port(addr)
                self.logger.info(f"AIO_GRPC: added insecure port at {addr}")
        except Exception as ex:
            conn_ctx.error = f"cannot listen on {addr}: {type(ex)}: {secure_format_exception(ex)}"
            self.logger.debug(conn_ctx.error)

    async def start(self, conn_ctx: _ConnCtx):
        pass

    async def shutdown(self):
        pass


class AioGrpcDriver(BaseDriver):

    aio_ctx = None

    def __init__(self):
        super().__init__()
        GrpcDriver.setup_grpc_env_var()

        self.server = None
        self.options = GRPC_DEFAULT_OPTIONS
        self.logger = get_obj_logger(self)
        configurator = CommConfigurator()
        config = configurator.get_config()
        if config:
            my_params = config.get("grpc")
            if my_params:
                self.options = my_params.get("options")
        self.logger.debug(f"GRPC Config: options={self.options}")
        self.closing = False

    @staticmethod
    def supported_transports() -> List[str]:
        pass

    @staticmethod
    def capabilities() -> Dict[str, Any]:
        pass

    async def _start_server(self, connector: ConnectorInfo, aio_ctx: AioContext, conn_ctx: _ConnCtx):
        pass

    def listen(self, connector: ConnectorInfo):
        pass

    async def _start_connect(self, connector: ConnectorInfo, aio_ctx: AioContext, conn_ctx: _ConnCtx):
        pass

    def connect(self, connector: ConnectorInfo):
        pass

    def shutdown(self):
        pass

    @staticmethod
    def get_urls(scheme: str, resources: dict) -> (str, str):
        pass
