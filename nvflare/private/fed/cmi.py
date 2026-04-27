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

from abc import ABC, abstractmethod

from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import FLContextKey, ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReservedHeaderKey, Shareable, make_reply
from nvflare.fuel.f3.cellnet.core_cell import FQCN, CoreCell, Message, MessageHeaderKey
from nvflare.fuel.f3.cellnet.core_cell import ReturnCode as CellReturnCode
from nvflare.private.defs import CellMessageHeaderKeys


class CellMessageInterface(FLComponent, ABC):

    HEADER_KEY_PEER_PROPS = "cmi.peer_props"
    HEADER_JOB_ID = "cmi.job_id"
    HEADER_PROJECT_NAME = "cmi.project"
    HEADER_SSID = "cmi.ssid"
    HEADER_CLIENT_TOKEN = "cmi.client_token"
    HEADER_CLIENT_NAME = "cmi.client_name"

    PROP_KEY_CLIENT = "cmi.client"
    PROP_KEY_FL_CTX = "cmi.fl_ctx"
    PROP_KEY_PEER_CTX = "cmi.peer_ctx"

    RC_TABLE = {
        CellReturnCode.TIMEOUT: ReturnCode.COMMUNICATION_ERROR,
        CellReturnCode.COMM_ERROR: ReturnCode.COMMUNICATION_ERROR,
        CellReturnCode.PROCESS_EXCEPTION: ReturnCode.EXECUTION_EXCEPTION,
        CellReturnCode.ABORT_RUN: CellReturnCode.ABORT_RUN,
        CellReturnCode.INVALID_REQUEST: CellReturnCode.INVALID_REQUEST,
        CellReturnCode.INVALID_SESSION: CellReturnCode.INVALID_SESSION,
        CellReturnCode.AUTHENTICATION_ERROR: CellReturnCode.UNAUTHENTICATED,
        CellReturnCode.SERVICE_UNAVAILABLE: CellReturnCode.SERVICE_UNAVAILABLE,
    }

    def __init__(
        self,
        engine,
    ):
        FLComponent.__init__(self)
        self.engine = engine
        self.cell = engine.get_cell()
        self.ready = False

        self.cell.add_incoming_request_filter(channel="*", topic="*", cb=self._filter_incoming_request)

        self.cell.add_outgoing_reply_filter(channel="*", topic="*", cb=self._filter_outgoing_message)

        self.cell.add_outgoing_request_filter(channel="*", topic="*", cb=self._filter_outgoing_message)

        self.cell.add_incoming_reply_filter(channel="*", topic="*", cb=self._filter_incoming_message)

    def new_cmi_message(self, fl_ctx: FLContext, headers=None, payload=None):
        pass

    def _filter_incoming_message(self, message: Message):
        pass

    def _filter_incoming_request(self, message: Message):
        pass

    def _filter_outgoing_message(self, message: Message):
        pass

    @staticmethod
    def _make_peer_ctx(props: dict) -> FLContext:
        pass

    @staticmethod
    def _convert_return_code(rc: CellReturnCode):
        pass

    @abstractmethod
    def send_to_cell(
        self,
        targets: [],
        channel: str,
        topic: str,
        request: Shareable,
        timeout: float,
        fl_ctx: FLContext,
        bulk_send=False,
    ) -> dict:
        pass


class JobCellMessenger(CellMessageInterface):
    def __init__(self, engine, job_id: str):
        super().__init__(engine)

        self.job_id = job_id

        self.cell.add_incoming_request_filter(channel="*", topic="*", cb=self._filter_incoming)
        self.cell.add_incoming_reply_filter(channel="*", topic="*", cb=self._filter_incoming)
        self.cell.add_outgoing_request_filter(channel="*", topic="*", cb=self._filter_outgoing)
        self.cell.add_outgoing_reply_filter(channel="*", topic="*", cb=self._filter_outgoing)

    def _filter_incoming(self, message: Message):
        pass

    def _filter_outgoing(self, message: Message):
        pass

    def send_to_cell(
        self,
        targets: [],
        channel: str,
        topic: str,
        request: Shareable,
        timeout: float,
        fl_ctx: FLContext,
        bulk_send=False,
        optional=False,
    ) -> dict:
        """Send request to the job cells of other target sites.
        Args:
            targets (list): list of client names that the request will be sent to
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
