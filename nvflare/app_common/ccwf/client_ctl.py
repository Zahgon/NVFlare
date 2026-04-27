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
import copy
import gc
import threading
import time
from abc import abstractmethod

from nvflare.apis.event_type import EventType
from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import FLContextKey, ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.impl.task_controller import Task, TaskController
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.app_common.abstract.learnable import Learnable
from nvflare.app_common.abstract.learnable_persistor import LearnablePersistor
from nvflare.app_common.abstract.shareable_generator import ShareableGenerator
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.app_event_type import AppEventType
from nvflare.app_common.ccwf.common import Constant, ResultType, StatusReport, make_task_name, topic_for_end_workflow
from nvflare.fuel.utils.validation_utils import check_non_empty_str, check_number_range, check_positive_number
from nvflare.security.logging import secure_format_traceback


class _LearnTask:
    def __init__(self, task_name: str, task_data: Shareable, fl_ctx: FLContext):
        self.task_name = task_name
        self.task_data = task_data
        self.fl_ctx = fl_ctx
        self.abort_signal = Signal()


class ClientSideController(Executor, TaskController):
    def __init__(
        self,
        task_name_prefix: str,
        learn_task_name=AppConstants.TASK_TRAIN,
        persistor_id=AppConstants.DEFAULT_PERSISTOR_ID,
        shareable_generator_id=AppConstants.DEFAULT_SHAREABLE_GENERATOR_ID,
        learn_task_check_interval=Constant.LEARN_TASK_CHECK_INTERVAL,
        learn_task_ack_timeout=Constant.LEARN_TASK_ACK_TIMEOUT,
        learn_task_abort_timeout=Constant.LEARN_TASK_ABORT_TIMEOUT,
        final_result_ack_timeout=Constant.FINAL_RESULT_ACK_TIMEOUT,
        allow_busy_task: bool = False,
    ):
        """
        Constructor of a ClientSideController object.

        Args:
            task_name_prefix: prefix of task names. All CCWF task names are prefixed with this.
            learn_task_name: name for the Learning Task (LT)
            persistor_id: ID of the persistor component
            shareable_generator_id: ID of the shareable generator component
            learn_task_check_interval: interval for checking incoming Learning Task (LT)
            learn_task_ack_timeout: timeout for sending the LT to other client(s)
            final_result_ack_timeout: timeout for sending final result to participating clients
            learn_task_abort_timeout: time to wait for the LT to become stopped after aborting it
            allow_busy_task: whether a new learn task is allowed when working on current learn task
        """
        check_non_empty_str("task_name_prefix", task_name_prefix)
        check_positive_number("learn_task_check_interval", learn_task_check_interval)
        check_number_range("learn_task_ack_timeout", learn_task_ack_timeout, min_value=1.0)
        check_positive_number("learn_task_abort_timeout", learn_task_abort_timeout)
        check_number_range("final_result_ack_timeout", final_result_ack_timeout, min_value=1.0)

        Executor.__init__(self)
        TaskController.__init__(self)
        self.task_name_prefix = task_name_prefix
        self.start_task_name = make_task_name(task_name_prefix, Constant.BASENAME_START)
        self.configure_task_name = make_task_name(task_name_prefix, Constant.BASENAME_CONFIG)
        self.do_learn_task_name = make_task_name(task_name_prefix, Constant.BASENAME_LEARN)
        self.report_final_result_task_name = make_task_name(task_name_prefix, Constant.BASENAME_REPORT_FINAL_RESULT)
        self.learn_task_name = learn_task_name
        self.learn_task_abort_timeout = learn_task_abort_timeout
        self.learn_task_check_interval = learn_task_check_interval
        self.learn_task_ack_timeout = learn_task_ack_timeout
        self.final_result_ack_timeout = final_result_ack_timeout
        self.allow_busy_task = allow_busy_task
        self.persistor_id = persistor_id
        self.shareable_generator_id = shareable_generator_id

        self.persistor = None
        self.shareable_generator = None

        self.current_status = StatusReport()
        self.last_status_report_time = time.time()  # time of last status report to server
        self.config = None
        self.workflow_id = None
        self.finalize_lock = threading.Lock()

        self.learn_thread = threading.Thread(target=self._do_learn)
        self.learn_thread.daemon = True
        self.learn_task = None
        self.current_task = None
        self.learn_executor = None
        self.learn_task_lock = threading.Lock()
        self.asked_to_stop = False
        self.status_lock = threading.Lock()
        self.engine = None
        self.me = None
        self.is_starting_client = False
        self.last_result = None
        self.last_round = None
        self.best_result = None
        self.best_metric = None
        self.best_round = 0
        self.workflow_done = False

    def get_config_prop(self, name: str, default=None):
        """
        Get a specified config property.

        Args:
            name: name of the property
            default: default value to return if the property is not defined.

        Returns:

        """
        pass

    def start_run(self, fl_ctx: FLContext):
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def _add_status_report(self, report: StatusReport, fl_ctx: FLContext):
        pass

    def initialize(self, fl_ctx: FLContext):
        """Called to initialize the executor.

        Args:
            fl_ctx: The FL Context

        Returns: None

        """
        pass

    def finalize(self, fl_ctx: FLContext):
        """Called to finalize the executor.

        Args:
            fl_ctx: the FL Context

        Returns: None

        """
        pass

    def process_config(self, fl_ctx: FLContext):
        """This is called to allow the subclass to process config props.

        Returns: None

        """
        pass

    def topic_for_my_workflow(self, base_topic: str):
        pass

    def broadcast_final_result(
        self, fl_ctx: FLContext, result_type: str, result: Learnable, metric=None, round_num=None
    ):
        pass

    def _try_broadcast_final_result(
        self, fl_ctx: FLContext, result_type: str, result: Learnable, metric=None, round_num=None
    ):
        pass

    def execute(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    @abstractmethod
    def start_workflow(self, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        """
        This is called for the subclass to start the workflow.
        This only happens on the starting_client.

        Args:
            shareable: the initial task data (e.g. initial model weights)
            fl_ctx: FL context
            abort_signal: abort signal for task execution

        Returns:

        """
        pass

    def _get_status_report(self):
        pass

    def _abort_current_task(self, fl_ctx: FLContext):
        pass

    def set_learn_task(self, task_data: Shareable, fl_ctx: FLContext) -> bool:
        pass

    def _do_learn(self):
        pass

    def update_status(self, last_round=None, action=None, error=None, all_done=False):
        pass

    @abstractmethod
    def do_learn_task(self, name: str, data: Shareable, fl_ctx: FLContext, abort_signal: Signal):
        """This is called to do a Learn Task.
        Subclass must implement this method.

        Args:
            name: task name
            data: task data
            fl_ctx: FL context of the task
            abort_signal: abort signal for the task execution

        Returns:

        """
        pass

    def _process_final_result(self, request: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def _process_end_workflow(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def _process_learn_request(self, request: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def _try_process_learn_request(self, request: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def send_learn_task(self, targets: list, request: Shareable, fl_ctx: FLContext) -> bool:
        pass

    def execute_learn_task(self, data: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def record_last_result(
        self,
        fl_ctx: FLContext,
        round_num: int,
        result: Learnable,
    ):
        pass

    def is_task_secure(self, fl_ctx: FLContext) -> bool:
        """
        Determine whether the task should be secure. A secure task requires encrypted communication between the peers.
        The task is secure only when the training is in secure mode AND private_p2p is set to True.
        """
        pass
