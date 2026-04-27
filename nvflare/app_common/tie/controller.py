# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
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
from abc import ABC, abstractmethod

from nvflare.apis.client import Client
from nvflare.apis.controller_spec import ClientTask, Task
from nvflare.apis.fl_context import FLContext
from nvflare.apis.impl.controller import Controller
from nvflare.apis.shareable import ReturnCode, Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.apis.utils.reliable_message import ReliableMessage
from nvflare.app_common.tie.connector import Connector
from nvflare.fuel.utils.validation_utils import check_number_range, check_positive_number
from nvflare.security.logging import secure_format_exception

from .applet import Applet
from .defs import Constant


class _ClientStatus:
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

        # operation of the last request from this client
        self.last_op = None

        # time of the last op request from this client
        self.last_op_time = time.time()

        # whether the app process is finished on this client
        self.app_done = False


class TieController(Controller, ABC):
    def __init__(
        self,
        configure_task_name=Constant.CONFIG_TASK_NAME,
        configure_task_timeout=Constant.CONFIG_TASK_TIMEOUT,
        start_task_name=Constant.START_TASK_NAME,
        start_task_timeout=Constant.START_TASK_TIMEOUT,
        job_status_check_interval: float = Constant.JOB_STATUS_CHECK_INTERVAL,
        max_client_op_interval: float = Constant.MAX_CLIENT_OP_INTERVAL,
        progress_timeout: float = Constant.WORKFLOW_PROGRESS_TIMEOUT,
    ):
        """
        Constructor

        Args:
            configure_task_name - name of the config task
            configure_task_timeout - time to wait for clients’ responses to the config task before timeout.
            start_task_name - name of the start task
            start_task_timeout - time to wait for clients’ responses to the start task before timeout.
            job_status_check_interval - how often to check client statuses of the job
            max_client_op_interval - max amount of time allowed between app ops from a client
            progress_timeout- the maximum amount of time allowed for the workflow to not make any progress.
                In other words, at least one participating client must have made progress during this time.
                Otherwise, the workflow will be considered to be in trouble and the job will be aborted.
        """
        Controller.__init__(self)
        self.configure_task_name = configure_task_name
        self.start_task_name = start_task_name
        self.start_task_timeout = start_task_timeout
        self.configure_task_timeout = configure_task_timeout
        self.max_client_op_interval = max_client_op_interval
        self.progress_timeout = progress_timeout
        self.job_status_check_interval = job_status_check_interval

        self.connector = None
        self.participating_clients = None
        self.status_lock = threading.Lock()
        self.client_statuses = {}  # client name => ClientStatus
        self.abort_signal = None

        check_number_range("configure_task_timeout", configure_task_timeout, min_value=1)
        check_number_range("start_task_timeout", start_task_timeout, min_value=1)
        check_positive_number("job_status_check_interval", job_status_check_interval)
        check_number_range("max_client_op_interval", max_client_op_interval, min_value=10.0)
        check_number_range("progress_timeout", progress_timeout, min_value=5.0)

    @abstractmethod
    def get_client_config_params(self, fl_ctx: FLContext) -> dict:
        """Called by the TieController to get config parameters to be sent to FL clients.
        Subclass of TieController must implement this method.

        Args:
            fl_ctx: FL context

        Returns: a dict of config params

        """
        pass

    @abstractmethod
    def get_connector_config_params(self, fl_ctx: FLContext) -> dict:
        """Called by the TieController to get config parameters for configuring the connector.
        Subclass of TieController must implement this method.

        Args:
            fl_ctx: FL context

        Returns: a dict of config params

        """
        pass

    @abstractmethod
    def get_connector(self, fl_ctx: FLContext) -> Connector:
        """Called by the TieController to get the Connector to be used with the controller.
        Subclass of TieController must implement this method.

        Args:
            fl_ctx: FL context

        Returns: a Connector object

        """
        pass

    @abstractmethod
    def get_applet(self, fl_ctx: FLContext) -> Applet:
        """Called by the TieController to get the Applet to be used with the controller.
        Subclass of TieController must implement this method.

        Args:
            fl_ctx: FL context

        Returns: an Applet object

        """
        pass

    def start_controller(self, fl_ctx: FLContext):
        """Start the controller.
        It first tries to get the connector and applet to be used.
        It then initializes the applet, set the applet to the connector, and initializes the connector.
        It finally registers message handlers for APP_REQUEST and CLIENT_DONE.
        If error occurs in any step, the job is stopped.

        Note: if a subclass overwrites this method, it must call super().start_controller()!

        Args:
            fl_ctx: the FL context

        Returns: None

        """
        pass

    def _trigger_stop(self, fl_ctx: FLContext, error=None):
        # first trigger the abort_signal to tell all components (mainly the controller's control_flow and connector)
        # that check this signal to abort.
        pass

    def _update_client_status(self, fl_ctx: FLContext, op=None, client_done=False):
        """Update the status of the requesting client.

        Args:
            fl_ctx: FL context
            op: the app operation requested
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

    def _handle_app_request(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        """Handle app request from applets on other sites
        It calls the connector to process the app request. If the connector fails to process the request, the
        job will be stopped.

        Args:
            topic: message topic
            request: the request data
            fl_ctx: FL context

        Returns: processing result as a Shareable object

        """
        pass

    def _configure_clients(self, abort_signal: Signal, fl_ctx: FLContext):
        pass

    def _start_clients(self, abort_signal: Signal, fl_ctx: FLContext):
        pass

    def control_flow(self, abort_signal: Signal, fl_ctx: FLContext):
        """
        To ensure smooth app execution:
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

    def _app_stopped(self, rc, fl_ctx: FLContext):
        # This CB is called when app server is stopped
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
        """This is called by base controller to stop.
        If a subclass overwrites this method, it must call super().stop_controller(fl_ctx).

        Args:
            fl_ctx:

        Returns:

        """
        pass
