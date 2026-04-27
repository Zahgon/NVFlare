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
import traceback
from typing import Union

from nvflare.app_common.decomposers import numpy_decomposers
from nvflare.client.ipc import defs
from nvflare.fuel.f3.cellnet.cell import Cell, Message
from nvflare.fuel.f3.cellnet.defs import MessageHeaderKey, ReturnCode
from nvflare.fuel.f3.cellnet.net_agent import NetAgent
from nvflare.fuel.f3.cellnet.utils import make_reply
from nvflare.fuel.f3.drivers.driver_params import DriverParams
from nvflare.fuel.utils.config_service import ConfigService
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.private.fed.utils.fed_utils import register_ext_decomposers

_SSL_ROOT_CERT = "rootCA.pem"
_SHORT_SLEEP_TIME = 0.2


class IPCAgent:
    def __init__(
        self,
        flare_site_url: str,
        flare_site_name: str,
        agent_id: str,
        workspace_dir: str,
        secure_mode=False,
        submit_result_timeout=30.0,
        flare_site_connection_timeout=60.0,
        flare_site_heartbeat_timeout=None,
        resend_result_interval=2.0,
        decomposer_module=None,
    ):
        """Constructor of Flare Agent. The agent is responsible for communicating with the Flare Client Job cell (CJ)
        to get task and to submit task result.

        Args:
            flare_site_url: the URL to the client parent cell (CP)
            flare_site_name: the CJ's site name (client name)
            agent_id: the unique ID of the agent
            workspace_dir: directory that contains startup folder and comm_config.json
            secure_mode: whether the connection is in secure mode or not
            submit_result_timeout: when submitting task result, how long to wait for response from the CJ
            flare_site_heartbeat_timeout: time for missing heartbeats from CJ before considering it dead
            flare_site_connection_timeout: time for missing heartbeats from CJ before considering it disconnected
        """
        ConfigService.initialize(section_files={}, config_path=[workspace_dir])

        self.logger = get_obj_logger(self)
        self.cell_name = defs.agent_site_fqcn(flare_site_name, agent_id)
        self.workspace_dir = workspace_dir
        self.secure_mode = secure_mode
        self.flare_site_url = flare_site_url
        self.submit_result_timeout = submit_result_timeout
        self.flare_site_heartbeat_timeout = flare_site_heartbeat_timeout
        self.flare_site_connection_timeout = flare_site_connection_timeout
        self.resend_result_interval = resend_result_interval
        self.num_results_submitted = 0
        self.current_task = None
        self.pending_task = None
        self.task_lock = threading.Lock()
        self.last_msg_time = time.time()  # last time to get msg from flare site
        self.peer_fqcn = None
        self.is_done = False
        self.is_started = False  # has the agent been started?
        self.is_stopped = False  # has the agent been stopped?
        self.is_connected = False  # is the agent connected to the flare site?
        self.credentials = {}  # security credentials for secure connection

        if secure_mode:
            root_cert_path = ConfigService.find_file(_SSL_ROOT_CERT)
            if not root_cert_path:
                raise ValueError(f"cannot find {_SSL_ROOT_CERT} from config path {workspace_dir}")

            self.credentials = {
                DriverParams.CA_CERT.value: root_cert_path,
            }

        self.cell = Cell(
            fqcn=self.cell_name,
            root_url="",
            parent_url=self.flare_site_url,
            secure=self.secure_mode,
            credentials=self.credentials,
            create_internal_listener=False,
        )
        self.net_agent = NetAgent(self.cell)

        self.cell.register_request_cb(channel=defs.CHANNEL, topic=defs.TOPIC_GET_TASK, cb=self._receive_task)
        self.logger.info(f"registered task CB for {defs.CHANNEL} {defs.TOPIC_GET_TASK}")
        self.cell.register_request_cb(channel=defs.CHANNEL, topic=defs.TOPIC_HEARTBEAT, cb=self._handle_heartbeat)
        self.cell.register_request_cb(channel=defs.CHANNEL, topic=defs.TOPIC_BYE, cb=self._handle_bye)
        self.cell.register_request_cb(channel=defs.CHANNEL, topic=defs.TOPIC_ABORT, cb=self._handle_abort_task)
        self.cell.core_cell.add_incoming_request_filter(
            channel="*",
            topic="*",
            cb=self._msg_received,
        )
        self.cell.core_cell.add_incoming_reply_filter(
            channel="*",
            topic="*",
            cb=self._msg_received,
        )
        numpy_decomposers.register()
        if decomposer_module:
            register_ext_decomposers(decomposer_module)

    def start(self):
        """Start the agent. This method must be called to enable CJ/Agent communication.

        Returns: None

        """
        pass

    def stop(self):
        """Stop the agent. After this is called, there will be no more communications between CJ and agent.

        Returns: None

        """
        pass

    def _monitor(self):
        pass

    def _handle_bye(self, request: Message) -> Union[None, Message]:
        pass

    def _msg_received(self, request: Message):
        pass

    def _handle_heartbeat(self, request: Message) -> Union[None, Message]:
        pass

    def _handle_abort_task(self, request: Message) -> Union[None, Message]:
        pass

    def _receive_task(self, request: Message) -> Union[None, Message]:
        pass

    def _create_task(self, request: Message):
        pass

    def _do_receive_task(self, request: Message) -> Union[None, Message]:
        pass

    def get_task(self, timeout=None):
        """Get a task from FLARE. This is a blocking call.

        If timeout is specified, this call is blocked only for the specified amount of time.
        If timeout is not specified, this call is blocked forever until a task is received or agent is closed.

        Args:
            timeout: amount of time to block

        Returns: None if no task is available during before timeout; or a Task object if task is available.
        Raises:
            AgentClosed exception if the agent is closed before timeout.
            CallStateError exception if the call is not made properly.

        Note: the application must make the call only when it is just started or after a previous task's result
        has been submitted.

        """
        pass

    def submit_result(self, result: defs.TaskResult) -> bool:
        """Submit the result of the current task.
        This is a blocking call. The agent will try to send the result to flare site until it is successfully sent or
        the task is aborted or the agent is closed.

        Args:
            result: result to be submitted

        Returns: whether the result is submitted successfully
        Raises: the CallStateError exception if the submit_result call is not made properly.

        Notes: the application must only make this call after the received task is processed. The call can only be
        made a single time regardless whether the submission is successful.

        """
        pass

    def _do_submit_result(self, result: defs.TaskResult) -> bool:
        pass

    def _send_result(self, current_task: defs.Task, result: defs.TaskResult):
        pass
