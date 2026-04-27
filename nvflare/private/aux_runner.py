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

import time
from threading import Lock
from typing import List, Tuple

from nvflare.apis.client import Client
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import ConfigVarName, ProcessType, ReturnCode, SystemConfigs
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReservedHeaderKey, Shareable, make_reply
from nvflare.fuel.f3.cellnet.core_cell import Message, MessageHeaderKey
from nvflare.fuel.f3.cellnet.core_cell import ReturnCode as CellReturnCode
from nvflare.fuel.f3.cellnet.core_cell import TargetMessage
from nvflare.fuel.f3.cellnet.fqcn import FQCN
from nvflare.fuel.utils.config_service import ConfigService
from nvflare.private.defs import CellChannel
from nvflare.security.logging import secure_format_exception, secure_format_traceback


class AuxMsgTarget:
    def __init__(self, name: str, fqcn: str):
        self.name = name
        self.fqcn = fqcn

    @staticmethod
    def server_target():
        pass

    @staticmethod
    def client_target(client: Client):
        pass

    def __str__(self):
        return f"AuxMsgTarget[name={self.name} fqcn={self.fqcn}]"


class AuxRunner(FLComponent):
    def __init__(self, engine):
        """To init the AuxRunner."""
        FLComponent.__init__(self)
        self.engine = engine
        self.topic_table = {}  # topic => handler
        self.reg_lock = Lock()
        self.cell_wait_timeout = None

    def register_aux_message_handler(self, topic: str, message_handle_func):
        """Register aux message handling function with specified topics.

        This method should be called by Engine's register_aux_message_handler method.

        Args:
            topic: the topic to be handled by the func
            message_handle_func: the func to handle the message. Must follow aux_message_handle_func_signature.

        Returns: N/A

        Exception is raised when:
            a handler is already registered for the topic;
            bad topic - must be a non-empty string
            bad message_handle_func - must be callable

        """
        pass

    def _process_request(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        """Call to process the request.

        .. note::

            peer_ctx props must have been set into the PEER_PROPS header of the request by Engine.

        Args:
            topic: topic of the message
            request: message to be handled
            fl_ctx: fl context

        Returns: reply message

        """
        pass

    def dispatch(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        """This method is to be called by the Engine when an aux message is received from peer.

        .. note::

            peer_ctx props must have been set into the PEER_PROPS header of the request by Engine.

        Args:
            topic: message topic
            request: request message
            fl_ctx: FLContext

        Returns: reply message

        """
        pass

    def _wait_for_cell(self):
        pass

    def _process_cell_replies(
        self,
        cell_replies: dict,
        topic: str,
        channel: str,
        fqcn_to_name: dict,
    ):
        pass

    def multicast_aux_requests(
        self,
        topic: str,
        target_requests: List[Tuple[AuxMsgTarget, Shareable]],
        timeout: float,
        fl_ctx: FLContext,
        optional: bool = False,
        secure: bool = False,
    ) -> dict:
        pass

    def _send_multi_requests(
        self,
        topic: str,
        target_requests: List[Tuple[AuxMsgTarget, Shareable]],
        timeout: float,
        fl_ctx: FLContext,
        optional: bool = False,
        secure: bool = False,
    ) -> dict:
        pass

    def send_aux_request(
        self,
        targets: List[AuxMsgTarget],
        topic: str,
        request: Shareable,
        timeout: float,
        fl_ctx: FLContext,
        bulk_send: bool = False,
        optional: bool = False,
        secure: bool = False,
    ) -> dict:
        """Send aux request to specified targets.

        Args:
            targets: a list of AuxMsgTarget(s)
            topic: topic of the message
            request: the request to be sent
            timeout: timeout of the request
            fl_ctx: FL context data
            bulk_send: whether to bulk send
            optional: whether the request is optional
            secure: whether to use P2P message encryption

        Returns: a dict of target_name => reply

        Note: each AuxMsgTarget in "targets" has the target's name and FQCN.
        The returned dict is keyed on the client Name, not client FQCN (which can be multiple levels).

        """
        pass

    def _send_to_cell(
        self,
        targets: List[AuxMsgTarget],
        channel: str,
        topic: str,
        request: Shareable,
        timeout: float,
        fl_ctx: FLContext,
        bulk_send=False,
        optional=False,
        secure=False,
    ) -> dict:
        """Send request to the job cells of other target sites.

        Args:
            targets (list): list of AuxMsgTarget that the request will be sent to
            channel (str): channel of the request
            topic (str): topic of the request
            request (Shareable): request
            timeout (float): how long to wait for result. 0 means fire-and-forget
            fl_ctx (FLContext): the FL context
            bulk_send: whether to bulk send this request (only applies in the fire-and-forget situation)
            optional: whether the request is optional

        Returns:
            A dict of Shareables

        """
        pass

    @staticmethod
    def _get_target_fqcn(target: AuxMsgTarget, fl_ctx: FLContext):
        pass

    @staticmethod
    def _convert_return_code(rc):
        pass
