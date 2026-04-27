# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
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
from typing import Union

from nvflare.apis.fl_context import FLContext
from nvflare.apis.streaming import StreamContext
from nvflare.app_common.streamers.file_streamer import FileStreamer
from nvflare.fuel.f3.cellnet.cell import Cell
from nvflare.fuel.f3.cellnet.defs import CellChannel
from nvflare.fuel.f3.message import Message as CellMessage
from nvflare.fuel.hci.conn import Connection
from nvflare.fuel.hci.proto import MetaKey, MetaStatusValue, ProtoKey, StreamChannel, make_meta, validate_proto
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.private.fed.server.cred_keeper import CredKeeper
from nvflare.security.logging import secure_log_traceback

from .constants import ConnProps
from .reg import ServerCommandRegister

logger = logging.getLogger(__name__)


class AdminServer:

    def __init__(
        self,
        cell: Cell,
        cmd_reg: ServerCommandRegister,
        engine,
        extra_conn_props=None,
    ):
        """Base class of FedAdminServer to create a server that can receive commands.

        Args:
            cell: the communication cell
            cmd_reg: CommandRegister
            extra_conn_props: a dict of extra conn props, if specified
        """
        if extra_conn_props is not None:
            assert isinstance(extra_conn_props, dict), "extra_conn_props must be dict but got {}".format(
                extra_conn_props
            )

        self.cell = cell
        self.engine = engine
        self.fl_ctx = None
        self.extra_conn_props = extra_conn_props
        self.cmd_reg = cmd_reg
        self.cred_keeper = CredKeeper()
        self.logger = get_obj_logger(self)

        cmd_reg.finalize()

        cell.register_request_cb(
            channel=CellChannel.HCI,
            topic="*",
            cb=self._process_admin_request,
        )

        if engine:
            self.fl_ctx = engine.new_context()
            FileStreamer.register_stream_processing(
                fl_ctx=self.fl_ctx,
                channel=StreamChannel.UPLOAD,
                topic="*",
                stream_done_cb=self._process_upload,
            )

    def get_id_asserter(self):
        pass

    def get_id_verifier(self):
        pass

    def _create_conn(self, conn_data: str, cmd_headers=None) -> (bool, str, Connection):
        pass

    def _process_upload(self, stream_ctx: StreamContext, fl_ctx: FLContext, **kwargs):
        pass

    def _process_admin_request(self, request: CellMessage) -> Union[None, CellMessage]:
        pass

    def stop(self):
        pass

    def set_command_registry(self, cmd_reg: ServerCommandRegister):
        pass

    def start(self):
        pass
