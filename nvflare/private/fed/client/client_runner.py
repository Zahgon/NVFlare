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
import fnmatch
import threading
import time
import uuid

from nvflare.apis.event_type import EventType
from nvflare.apis.executor import Executor
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import ConfigVarName, FilterKey, FLContextKey, ReservedKey, ReservedTopic, ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.fl_exception import UnsafeJobError
from nvflare.apis.shareable import ReservedHeaderKey, Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.apis.utils.event import fire_event_to_components
from nvflare.apis.utils.fl_context_utils import add_job_audit_event
from nvflare.apis.utils.reliable_message import ReliableMessage
from nvflare.apis.utils.task_utils import apply_filters
from nvflare.fuel.f3.cellnet.fqcn import FQCN
from nvflare.fuel.f3.streaming.download_service import DownloadService
from nvflare.fuel.utils.msg_root_utils import delete_msg_root
from nvflare.private.defs import SpecialTaskName, TaskConstant
from nvflare.private.fed.client.client_engine_executor_spec import ClientEngineExecutorSpec, TaskAssignment
from nvflare.private.fed.tbi import TBI
from nvflare.private.json_configer import ConfigError
from nvflare.private.privacy_manager import Scope
from nvflare.security.logging import secure_format_exception
from nvflare.widgets.info_collector import GroupInfoCollector, InfoCollector

from .utils import determine_parent_name

_TASK_CHECK_RESULT_OK = 0
_TASK_CHECK_RESULT_TRY_AGAIN = 1
_TASK_CHECK_RESULT_TASK_GONE = 2


class TaskRouter:
    def __init__(self):
        self.task_table = {}
        self.patterns = []

    @staticmethod
    def _is_pattern(p: str):
        pass

    def add_executor(self, tasks: list, executor: Executor):
        pass

    def route(self, task_name: str):
        pass


class ClientRunnerConfig(object):
    def __init__(
        self,
        task_router: TaskRouter,
        task_data_filters: dict,  # task_name => list of filters
        task_result_filters: dict,  # task_name => list of filters
        handlers=None,  # list of event handlers
        components=None,  # dict of extra python objects: id => object
        default_task_fetch_interval: float = 0.5,
    ):
        """To init ClientRunnerConfig.

        Args:
            task_router: TaskRouter object to find executor for a task
            task_data_filters: task_name => list of data filters
            task_result_filters: task_name => list of result filters
            handlers: list of event handlers
            components: dict of extra python objects: id => object
            default_task_fetch_interval: default task fetch interval before getting the correct value from server.
                default is set to 0.5.
        """
        self.task_router = task_router
        self.task_data_filters = task_data_filters
        self.task_result_filters = task_result_filters
        self.handlers = handlers
        self.components = components
        self.default_task_fetch_interval = default_task_fetch_interval

        if not components:
            self.components = {}

        if not handlers:
            self.handlers = []

    def add_component(self, comp_id: str, component: object):
        pass


class ClientRunner(TBI):
    def __init__(
        self,
        client_config: dict,
        config: ClientRunnerConfig,
        job_id: str,
        engine: ClientEngineExecutorSpec,
    ):
        """Initializes the ClientRunner.

        Args:
            client_config: provisioned client config.
            config: ClientRunnerConfig
            job_id: job id
            engine: ClientEngine object
        """

        TBI.__init__(self)
        self.client_config = client_config
        self.task_router = config.task_router
        self.task_data_filters = config.task_data_filters
        self.task_result_filters = config.task_result_filters
        self.default_task_fetch_interval = config.default_task_fetch_interval

        # parent target is where we will pull task and send task results to
        self.parent_target = self._determine_parent_target()
        self.job_id = job_id
        self.engine = engine
        self.run_abort_signal = Signal()
        self.task_lock = threading.Lock()
        self.running_tasks = {}  # task_id => TaskAssignment

        self.task_check_timeout = self.get_positive_float_var(ConfigVarName.TASK_CHECK_TIMEOUT, 5.0)
        self.task_check_interval = self.get_positive_float_var(ConfigVarName.TASK_CHECK_INTERVAL, 5.0)
        self.job_heartbeat_interval = self.get_positive_float_var(ConfigVarName.JOB_HEARTBEAT_INTERVAL, 10.0)
        self.get_task_timeout = self.get_positive_float_var(ConfigVarName.GET_TASK_TIMEOUT, None)
        self.submit_task_result_timeout = self.get_positive_float_var(ConfigVarName.SUBMIT_TASK_RESULT_TIMEOUT, None)
        self._register_aux_message_handlers(engine)
        self.register_event_handler(EventType.TASK_ASSIGNMENT_SENT, self._handle_task_sent_event)
        self.register_event_handler(EventType.TASK_RESULT_RECEIVED, self._handle_task_result_received_event)

    def _handle_task_sent_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def _handle_task_result_received_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def set_cell(self, cell):
        pass

    def find_executor(self, task_name):
        pass

    def _register_aux_message_handlers(self, engine):
        pass

    @staticmethod
    def _reply_and_audit(reply: Shareable, ref, msg, fl_ctx: FLContext) -> Shareable:
        pass

    def _process_task(self, task: TaskAssignment, fl_ctx: FLContext) -> Shareable:
        pass

    def _do_process_task(self, task: TaskAssignment, fl_ctx: FLContext) -> Shareable:
        pass

    def _do_task(self, task: TaskAssignment, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def _try_run(self):
        pass

    def _send_job_heartbeat(self):
        pass

    def fetch_and_run_one_task(self, fl_ctx) -> (float, bool):
        """Fetches and runs a task.

        Returns:
            A tuple of (task_fetch_interval, task_processed).
        """
        pass

    def _send_task_result(self, result: Shareable, task_id: str, fl_ctx: FLContext):
        pass

    def _try_send_result_once(self, result: Shareable, task_id: str, fl_ctx: FLContext):
        # wait until server is ready to receive
        pass

    def _check_task_once(self, task_id: str, fl_ctx: FLContext) -> int:
        """This method checks whether the server is still waiting for the specified task.
        The real reason for this method is to fight against unstable network connections.
        We try to make sure that when we send task result to the server, the connection is available.
        If the task check succeeds, then the network connection is likely to be available.
        Otherwise, we keep retrying until task check succeeds or the server tells us that the task is gone (timed out).
        Args:
            task_id:
            fl_ctx:
        Returns:
        """
        pass

    def run(self, app_root, args):
        pass

    def _determine_parent_target(self):
        pass

    def init_run(self, app_root, args):
        # set up syncing for children
        pass

    def _handle_sync_runner(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        # simply ack
        pass

    def _handle_task_check(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def _handle_job_heartbeat(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def end_run_events_sequence(self):
        pass

    def abort(self, msg: str = ""):
        """To Abort the current run.

        Returns: N/A

        """
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def _handle_end_run(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        # This happens when the controller on server asks the client to end the job.
        # Usually at the end of the workflow.
        pass

    def _handle_do_task(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        pass
