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
import threading
import time
from typing import Optional

import xgboost

from nvflare.apis.client import Client
from nvflare.apis.controller_spec import ClientTask, Task
from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.impl.controller import Controller
from nvflare.apis.shareable import ReturnCode, Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.apis.utils.reliable_message import ReliableMessage
from nvflare.app_opt.xgboost.histogram_based_v2.adaptors.xgb_adaptor import XGBServerAdaptor
from nvflare.fuel.utils.validation_utils import check_number_range, check_object_type, check_positive_number, check_str
from nvflare.security.logging import secure_format_exception

from .defs import Constant


class ClientStatus:
    """
    Objects of this class keep processing status of each FL client during job execution.
    """

    def __init__(self):
        # Set when the client's config reply is received and the reply return code is OK.
        # If the client failed to reply or the return code is not OK, this value is not set.
        self.configured_time = None

        # Set when the client's start reply is received and the reply return code is OK.
        # If the client failed to reply or the return code is not OK, this value is not set.
        self.started_time = None

        # operation of the last XGB request from this client
        self.last_op = None

        # time of the last XGB op request from this client
        self.last_op_time = time.time()

        # whether the XGB process is done on this client
        self.xgb_done = False


class XGBController(Controller):
    def __init__(
        self,
        adaptor_component_id: str,
        num_rounds: int,
        data_split_mode: int,
        secure_training: bool,
        xgb_params: dict,
        xgb_options: Optional[dict] = None,
        disable_version_check=False,
        configure_task_name=Constant.CONFIG_TASK_NAME,
        configure_task_timeout=Constant.CONFIG_TASK_TIMEOUT,
        start_task_name=Constant.START_TASK_NAME,
        start_task_timeout=Constant.START_TASK_TIMEOUT,
        job_status_check_interval: float = Constant.JOB_STATUS_CHECK_INTERVAL,
        max_client_op_interval: float = Constant.MAX_CLIENT_OP_INTERVAL,
        progress_timeout: float = Constant.WORKFLOW_PROGRESS_TIMEOUT,
        client_ranks=None,
    ):
        """
        Constructor

        For the meaning of XGBoost parameters, please refer to the documentation for train API,
        https://xgboost.readthedocs.io/en/stable/python/python_api.html#xgboost.train

        Args:
            adaptor_component_id - the component ID of server target adaptor
            num_rounds - number of rounds
            data_split_mode - 0 for horizontal/row-split, 1 for vertical/column-split
            secure_training - If true, secure training is enabled
            xgb_params - The params argument for train method
            xgb_options - All other arguments for train method are passed through this dictionary
            disable_version_check - If true, XGBoost version check for secure training is skipped
            configure_task_name - name of the config task
            configure_task_timeout - time to wait for clients’ responses to the config task before timeout.
            start_task_name - name of the start task
            start_task_timeout - time to wait for clients’ responses to the start task before timeout.
            job_status_check_interval - how often to check client statuses of the job
            max_client_op_interval - max amount of time allowed between XGB ops from a client
            progress_timeout- the maximum amount of time allowed for the workflow to not make any progress.
                In other words, at least one participating client must have made progress during this time.
                Otherwise, the workflow will be considered to be in trouble and the job will be aborted.
            client_ranks: client rank assignments.
                If specified, must be a dict of client_name => rank.
                If not specified, client ranks will be randomly assigned.
                No matter how assigned, ranks must be consecutive integers, starting from 0.
        """
        Controller.__init__(self)
        self.adaptor_component_id = adaptor_component_id
        self.num_rounds = num_rounds
        self.data_split_mode = data_split_mode
        self.secure_training = secure_training
        self.xgb_params = xgb_params
        self.xgb_options = xgb_options
        self.disable_version_check = disable_version_check
        self.configure_task_name = configure_task_name
        self.start_task_name = start_task_name
        self.start_task_timeout = start_task_timeout
        self.configure_task_timeout = configure_task_timeout
        self.max_client_op_interval = max_client_op_interval
        self.progress_timeout = progress_timeout
        self.job_status_check_interval = job_status_check_interval
        self.client_ranks = client_ranks  # client rank assignments

        self.adaptor = None
        self.participating_clients = None
        self.status_lock = threading.Lock()
        self.client_statuses = {}  # client name => ClientStatus
        self.abort_signal = None

        if data_split_mode not in {0, 1}:
            raise ValueError(f"Invalid data_split_mode: {data_split_mode}. It must be either 0 or 1")

        if not self.xgb_params:
            raise ValueError("xgb_params can't be empty")

        if not self.xgb_options:
            self.xgb_options = {}

        check_str("adaptor_component_id", adaptor_component_id)
        check_number_range("configure_task_timeout", configure_task_timeout, min_value=1)
        check_number_range("start_task_timeout", start_task_timeout, min_value=1)
        check_positive_number("job_status_check_interval", job_status_check_interval)
        check_positive_number("num_rounds", num_rounds)
        check_number_range("max_client_op_interval", max_client_op_interval, min_value=10.0)
        check_number_range("progress_timeout", progress_timeout, min_value=5.0)
        if client_ranks:
            check_object_type("client_ranks", client_ranks, dict)

        # set up operation handlers
        self.op_table = {
            Constant.OP_ALL_GATHER: self._process_all_gather,
            Constant.OP_ALL_GATHER_V: self._process_all_gather_v,
            Constant.OP_ALL_REDUCE: self._process_all_reduce,
            Constant.OP_BROADCAST: self._process_broadcast,
        }

    def get_adaptor(self, fl_ctx: FLContext):
        pass

    def start_controller(self, fl_ctx: FLContext):
        pass

    def _trigger_stop(self, fl_ctx: FLContext, error=None):
        # first trigger the abort_signal to tell all components (mainly the controller's control_flow and adaptor)
        # that check this signal to abort.
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def _is_stopped(self):
        # check whether the abort signal is triggered
        pass

    def _update_client_status(self, fl_ctx: FLContext, op=None, client_done=False):
        """Update the status of the requesting client.

        Args:
            fl_ctx: FL context
            op: the XGB operation requested
            client_done: whether the client is done

        Returns: None

        """
        pass

    def _process_client_done(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        """Process the ClientDone report for a client

        Args:
            topic: topic of the message
            request: request to be processed
            fl_ctx: the FL context

        Returns: reply to the client

        """
        pass

    def _process_all_gather(self, request: Shareable, fl_ctx: FLContext) -> Shareable:
        """This is the op handler for Allgather.

        Args:
            request: the request containing op params
            fl_ctx: FL context

        Returns: a Shareable containing operation result

        """
        pass

    def _process_all_gather_v(self, request: Shareable, fl_ctx: FLContext) -> Shareable:
        """This is the op handler for AllgatherV.

        Args:
            request: the request containing op params
            fl_ctx: FL context

        Returns: a Shareable containing operation result

        """
        pass

    def _process_all_reduce(self, request: Shareable, fl_ctx: FLContext) -> Shareable:
        """This is the op handler for Allreduce.

        Args:
            request: the request containing op params
            fl_ctx: FL context

        Returns: a Shareable containing operation result

        """
        pass

    def _process_broadcast(self, request: Shareable, fl_ctx: FLContext) -> Shareable:
        """This is the op handler for Broadcast.

        Args:
            request: the request containing op params
            fl_ctx: FL context

        Returns: a Shareable containing operation result

        """
        pass

    def _process_xgb_request(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def _configure_clients(self, abort_signal: Signal, fl_ctx: FLContext):
        pass

    def _start_clients(self, abort_signal: Signal, fl_ctx: FLContext):
        pass

    def control_flow(self, abort_signal: Signal, fl_ctx: FLContext):
        """
        This is the control flow of the XGB Controller. To ensure smooth XGB execution:
        - ensure that all clients are online and ready to go before starting server
        - ensure that server is started and ready to take requests before asking clients to start operation
        - monitor the health of the clients
        - if anything goes wrong, terminate the job

        Args:
            abort_signal: abort signal that is used to notify components to abort
            fl_ctx: FL context

        Returns: None

        """
        pass

    def _xgb_server_stopped(self, rc, fl_ctx: FLContext):
        # This CB is called when XGB server target is stopped
        pass

    def _process_configure_reply(self, client_task: ClientTask, fl_ctx: FLContext):
        pass

    def _process_start_reply(self, client_task: ClientTask, fl_ctx: FLContext):
        pass

    def _check_job_status(self, fl_ctx: FLContext) -> bool:
        """Check job status and determine whether the job is done.

        Args:
            fl_ctx: FL context

        Returns: whether the job is considered done.

        """
        pass

    def process_result_of_unknown_task(
        self, client: Client, task_name: str, client_task_id: str, result: Shareable, fl_ctx: FLContext
    ):
        pass

    def stop_controller(self, fl_ctx: FLContext):
        pass
