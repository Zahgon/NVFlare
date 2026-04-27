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

from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.apis.utils.fl_context_utils import gen_new_peer_ctx
from nvflare.fuel.f3.cellnet.core_cell import Message as CellMessage
from nvflare.fuel.f3.cellnet.core_cell import MessageHeaderKey, ReturnCode
from nvflare.fuel.f3.cellnet.core_cell import make_reply as make_cellnet_reply
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.private.defs import CellChannel, new_cell_message

from .admin_commands import AdminCommands


class CommandAgent(object):
    def __init__(self, federated_client) -> None:
        """To init the CommandAgent.

        Args:
            federated_client: FL client object
        """
        self.federated_client = federated_client
        self.thread = None
        self.asked_to_stop = False

        self.commands = AdminCommands.commands
        self.logger = get_obj_logger(self)

    def start(self, fl_ctx: FLContext):
        pass

    def register_cell_cb(self):
        pass

    def execute_command(self, request: CellMessage) -> CellMessage:

        pass

    def aux_communication(self, request: CellMessage) -> CellMessage:

        pass

    def shutdown(self):
        pass
