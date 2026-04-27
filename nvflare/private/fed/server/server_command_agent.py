# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
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

from nvflare.apis.fl_constant import ServerCommandKey
from nvflare.apis.shareable import ReservedHeaderKey, Shareable
from nvflare.apis.utils.fl_context_utils import gen_new_peer_ctx
from nvflare.fuel.f3.cellnet.cell import Cell
from nvflare.fuel.f3.cellnet.core_cell import MessageHeaderKey, ReturnCode, make_reply
from nvflare.fuel.f3.message import Message as CellMessage
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.private.defs import CellChannel, CellMessageHeaderKeys, new_cell_message

from .server_commands import ServerCommands


class ServerCommandAgent(object):
    def __init__(self, engine, cell: Cell) -> None:
        """To init the CommandAgent.

        Args:
            listen_port: port to listen the command
        """
        self.logger = get_obj_logger(self)
        self.asked_to_stop = False
        self.engine = engine
        self.cell = cell

    def start(self):
        pass

    def execute_command(self, request: CellMessage) -> CellMessage:

        pass

    def _get_client(self, token):
        pass

    def aux_communicate(self, request: CellMessage) -> CellMessage:

        pass

    def shutdown(self):
        pass
