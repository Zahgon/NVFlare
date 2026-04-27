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

import time
from datetime import datetime
from typing import List

from nvflare.apis.client import Client
from nvflare.apis.controller_spec import ClientTask, Task
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.impl.controller import Controller
from nvflare.apis.shareable import ReturnCode, Shareable
from nvflare.apis.signal import Signal
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.ccwf.common import (
    Constant,
    StatusReport,
    make_task_name,
    status_report_from_dict,
    topic_for_end_workflow,
)
from nvflare.fuel.utils.validation_utils import (
    DefaultValuePolicy,
    check_number_range,
    check_object_type,
    check_positive_int,
    check_positive_number,
    check_str,
    normalize_config_arg,
    validate_candidate,
    validate_candidates,
)
from nvflare.security.logging import secure_format_traceback


class ClientStatus:
    def __init__(self):
        self.ready_time = None
        self.last_report_time = time.time()
        self.last_progress_time = time.time()
        self.num_reports = 0
        self.status = StatusReport()


class ServerSideController(Controller):
    def __init__(
        self,
        num_rounds: int = 1,
        start_round: int = 0,
        task_name_prefix: str = "wf",
        configure_task_timeout=Constant.CONFIG_TASK_TIMEOUT,
        end_workflow_timeout=Constant.END_WORKFLOW_TIMEOUT,
        start_task_timeout=Constant.START_TASK_TIMEOUT,
        task_check_period: float = Constant.TASK_CHECK_INTERVAL,
        job_status_check_interval: float = Constant.JOB_STATUS_CHECK_INTERVAL,
        starting_client: str = "",
        starting_client_policy: str = DefaultValuePolicy.ANY,
        participating_clients=None,
        result_clients: List[str] = None,
        result_clients_policy: str = DefaultValuePolicy.ALL,
        max_status_report_interval: float = Constant.PER_CLIENT_STATUS_REPORT_TIMEOUT,
        progress_timeout: float = Constant.WORKFLOW_PROGRESS_TIMEOUT,
        private_p2p: bool = True,
        min_clients: int = 0,
    ):
        """
        Constructor

        Args:
            num_rounds - the number of rounds to be performed. This is a workflow config parameter. Defaults to 1.
            start_round - the starting round number. This is a workflow config parameter.
            task_name_prefix - the prefix for task names of this workflow.
                The workflow requires multiple tasks (e.g. config and start) between the server controller and the client.
                The full names of these tasks are <prefix>_config and <prefix>_start.
                Subclasses may send additional tasks. Naming these tasks with a common prefix can make it easier to
                configure task executors for FL clients.
            participating_clients - the names of the clients that will participate in the job. None means all clients.
            result_clients - names of the clients that will receive final learning results.
            result_clients_policy - how to determine result_clients if their names are not explicitly specified.
                Possible values are:
                    ALL - all participating clients
                    ANY - any one of the participating clients
                    EMPTY - no result_clients
                    DISALLOW - does not allow implicit - result_clients must be explicitly specified
            configure_task_timeout - time to wait for clients’ responses to the config task before timeout.
            starting_client - name of the starting client.
            starting_client_policy - how to determine the starting client if the name is not explicitly specified.
                Possible values are:
                    ANY - any one of the participating clients (the first client)
                    RANDOM - a random client
                    EMPTY - no starting client
                    DISALLOW - does not allow implicit - starting_client must be explicitly specified
            start_task_timeout - how long to wait for the starting client to finish the “start” task.
                If timed out, the job will be aborted.
                If the starting_client is not specified, then no start task will be sent.
                max_status_report_interval - the maximum amount of time allowed for a client to miss a status report.
                In other words, if a client fails to report its status for this much time, the client will be considered in
                trouble and the job will be aborted.
            progress_timeout- the maximum amount of time allowed for the workflow to not make any progress.
                In other words, at least one participating client must have made progress during this time.
                Otherwise, the workflow will be considered to be in trouble and the job will be aborted.
            end_workflow_timeout - timeout for ending workflow message.
            min_clients - minimum number of clients required for the workflow to proceed.
                0 means all participating clients are required (default, backward compatible).
                N > 0 means the workflow proceeds as long as at least N clients are active;
                the job only aborts when active clients drop below this threshold.
            private_p2p - whether to make peer-to-peer communications private.
                When set to True, P2P communications will be encrypted.
                Private P2P communication is an additional level of protection on basic communication security
                (such as SSL). Each pair of peers have their own encryption keys to ensure that only they themselves
                can understand their messages, even if the messages may be relayed through other sites (e.g. server).
                Different pairs of peers have different keys.
                Currently, private P2P is enabled only when the system is in secure mode. This is because key exchange
                between peers requires both sides to have PKI certificates and keys, which requires the project
                to be provisioned in secure mode.
        """
        Controller.__init__(self, task_check_period)
        participating_clients = normalize_config_arg(participating_clients)
        if participating_clients is None:
            raise ValueError("participating_clients must not be empty")

        self.task_name_prefix = task_name_prefix
        self.configure_task_name = make_task_name(task_name_prefix, Constant.BASENAME_CONFIG)
        self.configure_task_timeout = configure_task_timeout
        self.start_task_name = make_task_name(task_name_prefix, Constant.BASENAME_START)
        self.start_task_timeout = start_task_timeout
        self.end_workflow_timeout = end_workflow_timeout
        self.num_rounds = num_rounds
        self.start_round = start_round
        self.max_status_report_interval = max_status_report_interval
        self.progress_timeout = progress_timeout
        self.job_status_check_interval = job_status_check_interval
        self.starting_client = starting_client
        self.starting_client_policy = starting_client_policy
        self.participating_clients = participating_clients
        self.result_clients = result_clients if result_clients else []
        self.result_clients_policy = result_clients_policy

        # make private_p2p bool
        check_object_type("private_p2p", private_p2p, bool)
        self.private_p2p = private_p2p

        self.client_statuses = {}  # client name => ClientStatus
        self.cw_started = False
        self.asked_to_stop = False
        self.workflow_id = None

        if min_clients < 0:
            raise ValueError(f"min_clients must be >= 0, but got {min_clients}")
        self.min_clients = min_clients

        check_positive_int("num_rounds", num_rounds)
        check_number_range("configure_task_timeout", configure_task_timeout, min_value=1)
        check_number_range("end_workflow_timeout", end_workflow_timeout, min_value=1)
        check_positive_number("job_status_check_interval", job_status_check_interval)
        check_number_range("max_status_report_interval", max_status_report_interval, min_value=10.0)
        check_number_range("progress_timeout", progress_timeout, min_value=5.0)
        check_str("starting_client_policy", starting_client_policy)

        if participating_clients and len(participating_clients) < 2:
            raise ValueError(f"Not enough participating_clients: must > 1, but got {participating_clients}")

    def start_controller(self, fl_ctx: FLContext):
        pass

    def prepare_config(self) -> dict:
        pass

    def sub_flow(self, abort_signal: Signal, fl_ctx: FLContext):
        pass

    def control_flow(self, abort_signal: Signal, fl_ctx: FLContext):
        # wait for every client to become ready
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def process_config_reply(self, client_name: str, reply: Shareable, fl_ctx: FLContext) -> bool:
        pass

    def _process_configure_reply(self, client_task: ClientTask, fl_ctx: FLContext):
        pass

    def client_started(self, client_task: ClientTask, fl_ctx: FLContext):
        pass

    def _process_start_reply(self, client_task: ClientTask, fl_ctx: FLContext):
        pass

    def is_sub_flow_done(self, fl_ctx: FLContext) -> bool:
        pass

    def _check_job_status(self, fl_ctx: FLContext):
        # see whether the server side thinks it's done
        pass

    def _update_client_status(self, fl_ctx: FLContext):
        pass

    def process_result_of_unknown_task(
        self, client: Client, task_name: str, client_task_id: str, result: Shareable, fl_ctx: FLContext
    ):
        pass

    def stop_controller(self, fl_ctx: FLContext):
        pass
