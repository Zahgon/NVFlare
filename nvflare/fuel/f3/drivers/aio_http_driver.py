# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
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
import logging
from typing import Any, Dict, List

import aiohttp
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import StreamResponse

from nvflare.fuel.f3.comm_config_utils import requires_secure_connection
from nvflare.fuel.f3.connection import BytesAlike, Connection
from nvflare.fuel.f3.drivers import net_utils
from nvflare.fuel.f3.drivers.aio_context import AioContext
from nvflare.fuel.f3.drivers.base_driver import BaseDriver
from nvflare.fuel.f3.drivers.driver import ConnectorInfo
from nvflare.fuel.f3.drivers.driver_params import DriverCap, DriverParams
from nvflare.fuel.f3.drivers.net_utils import get_tcp_urls
from nvflare.fuel.hci.security import get_certificate_common_name
from nvflare.security.logging import secure_format_exception

log = logging.getLogger(__name__)

WS_PATH = "f3"
MAX_FRAME_SIZE = 2 * 1024 * 1024 * 1024  # Set it to 2GB


class WsConnection(Connection):
    def __init__(self, websocket: Any, aio_context: AioContext, connector: ConnectorInfo, ssl_context):
        super().__init__(connector)
        self.websocket = websocket
        self.aio_context = aio_context
        self.closing = False
        self.ssl_context = ssl_context

        self.conn_props = self._get_ws_properties()

    def get_conn_properties(self) -> dict:
        pass

    def close(self):
        pass

    def send_frame(self, frame: BytesAlike):
        pass

    def _get_ws_properties(self) -> dict:

        pass

    async def _async_send_frame(self, frame: BytesAlike):
        pass


class AioHttpDriver(BaseDriver):
    """Async HTTP driver using aiohttp library"""

    def __init__(self):
        super().__init__()
        self.aio_context = AioContext.get_global_context()
        self.loop = self.aio_context.get_event_loop()
        self.ssl_context = None
        self.stop_event = self.loop.create_future()
        self.app = None
        self.site = None
        self.runner = None

    @staticmethod
    def supported_transports() -> List[str]:
        pass

    @staticmethod
    def capabilities() -> Dict[str, Any]:
        pass

    def listen(self, connector: ConnectorInfo):
        async def setup():
            pass
        pass

    def connect(self, connector: ConnectorInfo):
        async def async_connect():
            pass
        pass

    def shutdown(self):
        pass

    @staticmethod
    def get_urls(scheme: str, resources: dict) -> (str, str):
        pass

    # Internal methods

    async def _connection_handler(self, websocket):
        pass

    async def _websocket_handler(self, request: Request) -> StreamResponse:
        pass

    @staticmethod
    async def _read_loop(conn: WsConnection):

        pass

    async def _async_shutdown(self):
        pass
