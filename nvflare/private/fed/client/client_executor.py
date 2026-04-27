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
import copy
import json
import threading
import time
from abc import ABC, abstractmethod

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import AdminCommandNames, ConnPropKey, FLContextKey, RunProcessKey, SystemConfigs
from nvflare.apis.fl_context import FLContext
from nvflare.apis.job_launcher_spec import JobLauncherSpec, JobProcessArgs
from nvflare.apis.resource_manager_spec import ResourceManagerSpec
from nvflare.apis.workspace import Workspace
from nvflare.fuel.common.exit_codes import PROCESS_EXIT_REASON, ProcessExitCode
from nvflare.fuel.f3.cellnet.core_cell import FQCN
from nvflare.fuel.f3.cellnet.defs import MessageHeaderKey, ReturnCode
from nvflare.fuel.f3.message import Message as CellMessage
from nvflare.fuel.utils.config_service import ConfigService
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.private.defs import CellChannel, CellChannelTopic, JobFailureMsgKey, new_cell_message
from nvflare.private.fed.utils.fed_utils import get_job_launcher, get_return_code
from nvflare.security.logging import secure_format_exception, secure_log_traceback

from .client_status import ClientStatus, get_status_message


class ClientExecutor(ABC):
    @abstractmethod
    def start_app(
        self,
        client,
        job_id,
        job_meta,
        args,
        allocated_resource,
        token,
        resource_manager,
        fl_ctx: FLContext,
    ):
        """Starts the client app.

        Args:
            client: the FL client object
            job_id: the job_id
            args: admin command arguments for starting the FL client training
            allocated_resource: allocated resources
            token: token from resource manager
            resource_manager: resource manager
            fl_ctx: FLContext
        """
        pass

    @abstractmethod
    def check_status(self, job_id) -> str:
        """Checks the status of the running client.

        Args:
            job_id: the job_id

        Returns:
            A client status message
        """
        pass

    @abstractmethod
    def abort_app(self, job_id):
        """Aborts the running app.

        Args:
            job_id: the job_id
        """
        pass

    @abstractmethod
    def abort_task(self, job_id):
        """Aborts the client executing task.

        Args:
            job_id: the job_id
        """
        pass

    @abstractmethod
    def get_run_info(self, job_id):
        """Gets the run information.

        Args:
            job_id: the job_id

        Returns:
            A dict of run information.
        """

    @abstractmethod
    def get_errors(self, job_id):
        """Get the error information.

        Returns:
            A dict of error information.

        """

    @abstractmethod
    def reset_errors(self, job_id):
        """Resets the error information.

        Args:
            job_id: the job_id
        """


class JobExecutor(ClientExecutor):
    """Run the Client executor in a child process."""

    def __init__(self, client, startup):
        """To init the ProcessExecutor.

        Args:
            startup: startup folder
        """
        self.client = client
        self.logger = get_obj_logger(self)
        self.startup = startup
        self.run_processes = {}
        self.lock = threading.Lock()

        self.job_query_timeout = ConfigService.get_float_var(
            name="job_query_timeout", conf=SystemConfigs.APPLICATION_CONF, default=5.0
        )

    def start_app(
        self,
        client,
        job_id,
        job_meta,
        args,
        allocated_resource,
        token,
        resource_manager: ResourceManagerSpec,
        fl_ctx: FLContext,
    ):
        """Starts the app.

        Args:
            client: the FL client object
            job_id: the job_id
            job_meta: job metadata
            args: admin command arguments for starting the worker process
            allocated_resource: allocated resources
            token: token from resource manager
            resource_manager: resource manager
            fl_ctx: FLContext
        """
        pass

    def _get_job_launcher(self, job_meta: dict, fl_ctx: FLContext) -> JobLauncherSpec:
        pass

    def notify_job_status(self, job_id, job_status):
        pass

    def _job_fqcn(self, job_id: str):
        pass

    def check_status(self, job_id):
        """Checks the status of the running client.

        Args:
            job_id: the job_id

        Returns:
            A client status message
        """
        pass

    def get_run_info(self, job_id):
        """Gets the run information.

        Args:
            job_id: the job_id

        Returns:
            A dict of run information.
        """
        pass

    def get_errors(self, job_id):
        """Get the error information.

        Args:
            job_id: the job_id

        Returns:
            A dict of error information.
        """
        pass

    def configure_job_log(self, job_id, config):
        """Configure the job log.

        Args:
            job_id: the job_id
            config: log config

         Returns:
            configure_job_log command message
        """
        pass

    def reset_errors(self, job_id):
        """Resets the error information.

        Args:
            job_id: the job_id
        """
        pass

    def abort_app(self, job_id):
        """Aborts the running app.

        Args:
            job_id: the job_id
        """
        pass

    def send_to_job(
        self,
        job_id,
        channel: str,
        topic: str,
        msg: CellMessage,
        timeout: float,
        optional=False,
    ) -> CellMessage:
        """Send a message to CJ

        Args:
            job_id: id of the job
            channel: message channel
            topic: message topic
            msg: the message to be sent
            timeout: how long to wait for reply
            optional: whether the message is optional

        Returns: reply from CJ

        """
        pass

    def _terminate_job(self, job_handle, job_id):
        pass

    def abort_task(self, job_id):
        """Aborts the client executing task.

        Args:
            job_id: the job_id
        """
        pass

    def _wait_child_process_finish(
        self, client, job_id, allocated_resource, token, resource_manager, workspace, fl_ctx
    ):
        pass

    def get_status(self, job_id):
        pass

    def get_run_processes_keys(self):
        pass
