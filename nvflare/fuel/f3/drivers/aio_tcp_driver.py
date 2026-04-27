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
import logging
from concurrent.futures import CancelledError
from typing import Any, Dict, List

from nvflare.fuel.f3.comm_error import CommError
from nvflare.fuel.f3.drivers.aio_conn import AioConnection
from nvflare.fuel.f3.drivers.aio_context import AioContext
from nvflare.fuel.f3.drivers.base_driver import BaseDriver
from nvflare.fuel.f3.drivers.connector_info import ConnectorInfo, Mode
from nvflare.fuel.f3.drivers.driver_params import DriverCap, DriverParams
from nvflare.fuel.f3.drivers.net_utils import get_ssl_context
from nvflare.fuel.f3.drivers.tcp_driver import TcpDriver

log = logging.getLogger(__name__)


class AioTcpDriver(BaseDriver):
    def __init__(self):
        super().__init__()
        self.aio_ctx = AioContext.get_global_context()
        self.server = None
        self.ssl_context = None

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

    def shutdown(self):
        pass

    @staticmethod
    def get_urls(scheme: str, resources: dict) -> (str, str):
        pass

    # Internal methods

    def _run(self, connector: ConnectorInfo, mode: Mode):
        pass

    async def _async_run(self, mode: Mode):

        pass

    async def _tcp_connect(self, host, port):
        pass

    async def _tcp_listen(self, host, port):
        pass

    async def _create_connection(self, reader, writer):
        pass
