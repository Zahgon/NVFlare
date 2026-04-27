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
import logging
from asyncio import CancelledError, IncompleteReadError, StreamReader, StreamWriter

from nvflare.fuel.f3.comm_error import CommError
from nvflare.fuel.f3.connection import BytesAlike, Connection
from nvflare.fuel.f3.drivers.aio_context import AioContext
from nvflare.fuel.f3.drivers.connector_info import ConnectorInfo
from nvflare.fuel.f3.drivers.driver_params import DriverParams
from nvflare.fuel.f3.drivers.net_utils import MAX_FRAME_SIZE
from nvflare.fuel.f3.sfm.prefix import PREFIX_LEN, Prefix
from nvflare.fuel.hci.security import get_certificate_common_name
from nvflare.security.logging import secure_format_exception

log = logging.getLogger(__name__)


class AioConnection(Connection):
    def __init__(
        self,
        connector: ConnectorInfo,
        aio_ctx: AioContext,
        reader: StreamReader,
        writer: StreamWriter,
        secure: bool = False,
    ):
        super().__init__(connector)
        self.reader = reader
        self.writer = writer
        self.aio_ctx = aio_ctx
        self.closing = False
        self.secure = secure
        self.conn_props = self._get_aio_properties()

    def get_conn_properties(self) -> dict:
        pass

    def close(self):
        pass

    def send_frame(self, frame: BytesAlike):
        pass

    async def read_loop(self):
        pass

    # Internal methods

    async def _async_send_frame(self, frame: BytesAlike):
        pass

    async def _async_read_frame(self):

        pass

    def _get_aio_properties(self) -> dict:

        pass
