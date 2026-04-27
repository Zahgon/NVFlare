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
import errno
import logging
import select
import socket
import time
from socketserver import BaseRequestHandler
from typing import Any, Union

from nvflare.fuel.f3.comm_config import CommConfigurator
from nvflare.fuel.f3.comm_error import CommError
from nvflare.fuel.f3.connection import BytesAlike, Connection
from nvflare.fuel.f3.drivers.driver import ConnectorInfo
from nvflare.fuel.f3.drivers.driver_params import DriverParams
from nvflare.fuel.f3.drivers.net_utils import MAX_FRAME_SIZE
from nvflare.fuel.f3.sfm.prefix import PREFIX_LEN, Prefix
from nvflare.fuel.hci.security import get_certificate_common_name
from nvflare.security.logging import secure_format_exception

log = logging.getLogger(__name__)


class SocketConnection(Connection):
    def __init__(self, sock: Any, connector: ConnectorInfo, secure: bool = False):
        super().__init__(connector)
        self.sock = sock
        self.secure = secure
        self.closing = False
        self.conn_props = self._get_socket_properties()
        self.send_timeout = CommConfigurator().get_streaming_send_timeout(30.0)

    def get_conn_properties(self) -> dict:
        pass

    def close(self):
        pass

    def send_frame(self, frame: BytesAlike):
        pass

    @staticmethod
    def _is_timeout_exception(ex: Exception) -> bool:
        pass

    @staticmethod
    def _is_closed_socket_exception(ex: Exception) -> bool:
        pass

    def _send_with_timeout(self, frame: BytesAlike, timeout_sec: float):
        pass

    def read_loop(self):
        pass

    def read_frame_loop(self):
        # read_frame throws exception on stale/bad connection so this is not a dead loop
        pass

    def read_frame(self) -> BytesAlike:

        pass

    def read_into(self, buffer: BytesAlike, offset: int, length: int):
        pass

    @staticmethod
    def _format_address(addr: Union[str, tuple], fileno: int) -> str:

        pass

    def _get_socket_properties(self) -> dict:
        pass


class ConnectionHandler(BaseRequestHandler):
    def handle(self):

        # noinspection PyUnresolvedReferences
        pass
