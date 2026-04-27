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
import json
import os.path
import threading
import time
from random import randrange

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.job_def import JobMetaKey
from nvflare.edge.constants import (
    EdgeApiStatus,
    EdgeConfigFile,
    EdgeContextKey,
    EdgeEventType,
    EdgeMsgTopic,
    JobDataKey,
)
from nvflare.edge.web.models.job_request import JobRequest
from nvflare.edge.web.models.job_response import JobResponse
from nvflare.edge.web.models.result_response import ResultResponse
from nvflare.edge.web.models.selection_response import SelectionResponse
from nvflare.edge.web.models.task_response import TaskResponse
from nvflare.fuel.f3.cellnet.cell import ReturnCode as CellReturnCode
from nvflare.fuel.f3.cellnet.defs import CellChannel, MessageHeaderKey
from nvflare.fuel.f3.cellnet.utils import new_cell_message
from nvflare.fuel.f3.message import Message as CellMessage
from nvflare.widgets.widget import Widget


class EdgeTaskDispatcher(Widget):
    """Edge Task Dispatcher (ETD) is to be used to dispatch a received edge request to a running job (CJ).
    ETD must be installed on CP (local/resources.json) before the CP is started.

    Note: ETD does not interact with edge devices directly. It's another component's responsibility (e.g. web agent)
    to interact with edge devices with whatever protocol between them.

    ETD indirectly interacts with edge-device-interacting component (also installed on the CP) via Flare Events:
        EdgeEventType.EDGE_JOB_REQUEST_RECEIVED for receiving job requests;
        EdgeEventType.EDGE_TASK_REQUEST_RECEIVED for receiving task requests;
        EdgeEventType.EDGE_SELECTION_REQUEST_RECEIVED for receiving selection requests;
        EdgeEventType.EDGE_RESULT_REPORT_RECEIVED for receiving result reports;

    """

    def __init__(self, request_timeout: float = 5.0):
        Widget.__init__(self)
        self.request_timeout = request_timeout
        self.edge_jobs = {}  # job name => list of job_ids
        self.job_metas = {}  # job_id => job_meta
        self.job_device_config = {}  # job_id => device config
        self.lock = threading.Lock()

        self.register_event_handler(
            EventType.AFTER_JOB_LAUNCH,
            self._handle_job_launched,
        )
        self.register_event_handler(
            [EventType.JOB_COMPLETED, EventType.JOB_CANCELLED, EventType.JOB_ABORTED],
            self._handle_job_done,
        )
        self.register_event_handler(
            EdgeEventType.EDGE_JOB_REQUEST_RECEIVED,
            self._handle_edge_job_request,
        )
        self.register_event_handler(
            EdgeEventType.EDGE_TASK_REQUEST_RECEIVED,
            self._handle_edge_request,
            msg_topic=EdgeMsgTopic.TASK_REQUEST,
            bad_req_reply=TaskResponse(EdgeApiStatus.INVALID_REQUEST),
            no_job_reply=TaskResponse(EdgeApiStatus.NO_JOB),
            comm_err_reply=TaskResponse(EdgeApiStatus.RETRY),
        )
        self.register_event_handler(
            EdgeEventType.EDGE_SELECTION_REQUEST_RECEIVED,
            self._handle_edge_request,
            msg_topic=EdgeMsgTopic.SELECTION_REQUEST,
            bad_req_reply=SelectionResponse(EdgeApiStatus.INVALID_REQUEST),
            no_job_reply=SelectionResponse(EdgeApiStatus.NO_JOB),
            comm_err_reply=SelectionResponse(EdgeApiStatus.RETRY),
        )
        self.register_event_handler(
            EdgeEventType.EDGE_RESULT_REPORT_RECEIVED,
            self._handle_edge_request,
            msg_topic=EdgeMsgTopic.RESULT_REPORT,
            bad_req_reply=ResultResponse(EdgeApiStatus.INVALID_REQUEST),
            no_job_reply=ResultResponse(EdgeApiStatus.NO_JOB),
            comm_err_reply=ResultResponse(EdgeApiStatus.RETRY),
        )
        self.logger.debug("EdgeTaskDispatcher created!")

    def _add_job(self, job_meta: dict, fl_ctx: FLContext):
        pass

    def _remove_job(self, job_id: str):
        pass

    def _match_job(self, job_name: str):
        pass

    def _job_exists(self, job_id: str):
        pass

    def _handle_job_launched(self, event_type: str, fl_ctx: FLContext):
        pass

    def _handle_job_done(self, event_type: str, fl_ctx: FLContext):
        pass

    def _handle_edge_job_request(self, event_type: str, fl_ctx: FLContext):
        pass

    @staticmethod
    def _set_edge_reply(reply, fl_ctx: FLContext):
        """Prepare the reply to the edge device.

        Args:
            reply: the reply to be set
            fl_ctx: FLContext object

        Returns: None

        """
        pass

    def _handle_edge_request(
        self,
        event_type: str,
        fl_ctx: FLContext,
        msg_topic: str,
        bad_req_reply,
        no_job_reply,
        comm_err_reply,
    ):
        pass
