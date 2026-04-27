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

import threading
import time

from nvflare.apis.client import Client
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import FilterKey, FLContextKey, ReservedKey, ReservedTopic, ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.server_engine_spec import ServerEngineSpec
from nvflare.apis.shareable import ReservedHeaderKey, Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.apis.utils.fl_context_utils import add_job_audit_event
from nvflare.apis.utils.reliable_message import ReliableMessage
from nvflare.apis.utils.task_utils import apply_filters
from nvflare.fuel.f3.streaming.download_service import DownloadService
from nvflare.fuel.utils.job_utils import build_client_hierarchy
from nvflare.private.defs import SpecialTaskName, TaskConstant
from nvflare.private.fed.tbi import TBI
from nvflare.private.privacy_manager import Scope
from nvflare.security.logging import secure_format_exception
from nvflare.widgets.info_collector import GroupInfoCollector, InfoCollector


class ServerRunnerConfig(object):
    def __init__(
        self,
        heartbeat_timeout: int,
        task_request_interval: float,
        workflows: [],
        task_data_filters: dict,
        task_result_filters: dict,
        handlers=None,
        components=None,
    ):
        """Configuration for ServerRunner.

        Args:
            heartbeat_timeout (int): Client heartbeat timeout in seconds
            task_request_interval (float): Task request interval in seconds
            workflows (list): A list of workflow
            task_data_filters (dict):  A dict of  {task_name: list of filters apply to data (pre-process)}
            task_result_filters (dict): A dict of {task_name: list of filters apply to result (post-process)}
            handlers (list, optional):  A list of event handlers
            components (dict, optional):  A dict of extra python objects {id: object}
        """
        self.heartbeat_timeout = heartbeat_timeout
        self.task_request_interval = task_request_interval
        self.workflows = workflows
        self.task_data_filters = task_data_filters
        self.task_result_filters = task_result_filters
        self.handlers = handlers
        self.components = components

    def add_component(self, comp_id: str, component: object):
        pass


class ServerRunner(TBI):

    ABORT_RETURN_CODES = [
        ReturnCode.RUN_MISMATCH,
        ReturnCode.TASK_UNKNOWN,
        ReturnCode.UNSAFE_JOB,
    ]

    def __init__(self, config: ServerRunnerConfig, job_id: str, engine: ServerEngineSpec):
        """Server runner class.

        Args:
            config (ServerRunnerConfig): configuration of server runner
            job_id (str): The number to distinguish each experiment
            engine (ServerEngineSpec): server engine
        """
        TBI.__init__(self)
        self.job_id = job_id
        self.config = config
        self.engine = engine
        self.abort_signal = Signal()
        self.wf_lock = threading.Lock()
        self.current_wf = None
        self.current_wf_index = 0
        self.status = "init"
        self.turn_to_cold = False
        # track tasks currently being processed (during filtering) to prevent duplicate assignments
        self._processing_tasks = {}  # client_name => task_id
        self._processing_tasks_lock = threading.Lock()  # protect _processing_tasks from race conditions
        self._register_aux_message_handler(engine)

    def _register_aux_message_handler(self, engine):
        pass

    def _handle_sync_runner(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        # simply ack
        pass

    def _execute_run(self):
        pass

    def run(self):
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def _task_try_again(self) -> (str, str, Shareable):
        pass

    def process_task_request(self, client: Client, fl_ctx: FLContext) -> (str, str, Shareable):
        """Process task request from a client.

        NOTE: the Engine will create a new fl_ctx and call this method:

            with engine.new_context() as fl_ctx:
                name, id, data = runner.process_task_request(client, fl_ctx)
                ...

        Args:
            client (Client): client object
            fl_ctx (FLContext): FL context

        Returns:
            A tuple of (task name, task id, and task data)
        """
        pass

    def _try_to_get_task(self, client, fl_ctx, timeout=None, retry_interval=0.005):
        pass

    def handle_dead_job(self, client_name: str, fl_ctx: FLContext):
        pass

    def process_submission(self, client: Client, task_name: str, task_id: str, result: Shareable, fl_ctx: FLContext):
        """Process task result submitted from a client.

        NOTE: the Engine will create a new fl_ctx and call this method:

            with engine.new_context() as fl_ctx:
                name, id, data = runner.process_submission(client, fl_ctx)

        Args:
            client: Client object
            task_name: task name
            task_id: task id
            result: task result
            fl_ctx: FLContext
        """
        pass

    def _report_client_active(self, reason: str, fl_ctx: FLContext):
        pass

    def _handle_job_heartbeat(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def _handle_task_check(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def abort(self, fl_ctx: FLContext, turn_to_cold: bool = False):
        pass

    def get_persist_state(self, fl_ctx: FLContext) -> dict:
        pass

    def restore(self, state_data: dict, fl_ctx: FLContext):
        pass
