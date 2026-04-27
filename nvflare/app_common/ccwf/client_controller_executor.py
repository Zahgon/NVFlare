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
import copy
import threading
import time
from typing import List

from nvflare.apis.event_type import EventType
from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import FLContextKey, ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.impl.task_controller import Task
from nvflare.apis.impl.wf_comm_client import WFCommClient
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.app_common.abstract.learnable import Learnable
from nvflare.app_common.abstract.learnable_persistor import LearnablePersistor
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.ccwf.common import Constant, StatusReport, make_task_name, topic_for_end_workflow
from nvflare.fuel.utils.validation_utils import check_number_range
from nvflare.security.logging import secure_format_exception


class ClientControllerExecutor(Executor):
    def __init__(
        self,
        controller_id_list: List,
        task_name_prefix: str = "",
        persistor_id=AppConstants.DEFAULT_PERSISTOR_ID,
        final_result_ack_timeout=Constant.FINAL_RESULT_ACK_TIMEOUT,
        max_task_timeout: int = Constant.MAX_TASK_TIMEOUT,
    ):
        """
        ClientControllerExecutor for running controllers on client-side using WFCommClient.

        Args:
            controller_id_list: List of controller ids, used in order.
            task_name_prefix: prefix of task names. All CCWF task names are prefixed with this.
            persistor_id: ID of the persistor component
            final_result_ack_timeout: timeout for sending final result to participating clients
            max_task_timeout: Maximum task timeout for Controllers using WFCommClient when `task.timeout` is set to 0. Defaults to 3600.
        """
        check_number_range("final_result_ack_timeout", final_result_ack_timeout, min_value=1.0)

        Executor.__init__(self)
        self.controller_id_list = controller_id_list
        self.task_name_prefix = task_name_prefix
        self.persistor_id = persistor_id
        self.final_result_ack_timeout = final_result_ack_timeout
        self.max_task_timeout = max_task_timeout

        self.start_task_name = make_task_name(task_name_prefix, Constant.BASENAME_START)
        self.configure_task_name = make_task_name(task_name_prefix, Constant.BASENAME_CONFIG)
        self.report_final_result_task_name = make_task_name(task_name_prefix, Constant.BASENAME_REPORT_FINAL_RESULT)

        self.persistor = None

        self.current_status = StatusReport()
        self.last_status_report_time = time.time()  # time of last status report to server
        self.config = None
        self.workflow_id = None
        self.finalize_lock = threading.Lock()

        self.asked_to_stop = False
        self.status_lock = threading.Lock()
        self.engine = None
        self.me = None
        self.is_starting_client = False
        self.workflow_done = False
        self.fatal_system_error = False

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

    def initialize_controller(self, controller_id, fl_ctx):
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

    def execute(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def _get_status_report(self):
        pass

    def update_status(self, last_round=None, action=None, error=None, all_done=False):
        pass

    def _process_final_result(self, request: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def _process_end_workflow(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def is_task_secure(self, fl_ctx: FLContext) -> bool:
        """
        Determine whether the task should be secure. A secure task requires encrypted communication between the peers.
        The task is secure only when the training is in secure mode AND private_p2p is set to True.
        """
        pass

    def broadcast_final_result(self, result: Learnable, fl_ctx: FLContext):
        pass
