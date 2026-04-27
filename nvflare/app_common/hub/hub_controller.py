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

import json
import time
from typing import Union

from nvflare.apis.client import Client
from nvflare.apis.controller_spec import (
    ClientTask,
    ControllerSpec,
    OperatorConfigKey,
    OperatorMethod,
    Task,
    TaskOperatorKey,
)
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import FLContextKey, ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.impl.controller import Controller
from nvflare.apis.operator_spec import OperatorSpec
from nvflare.apis.shareable import ReservedHeaderKey, Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.app_common.abstract.aggregator import Aggregator
from nvflare.app_common.abstract.learnable_persistor import LearnablePersistor
from nvflare.app_common.abstract.shareable_generator import ShareableGenerator
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.app_event_type import AppEventType
from nvflare.fuel.utils.constants import PipeChannelName
from nvflare.fuel.utils.pipe.pipe import Message, Pipe
from nvflare.fuel.utils.pipe.pipe_handler import PipeHandler, Topic
from nvflare.fuel.utils.validation_utils import check_object_type, check_positive_number, check_str


class BcastOperator(OperatorSpec, FLComponent):

    _PROP_AGGR = "aggr"

    def __init__(self):
        OperatorSpec.__init__(self)
        FLComponent.__init__(self)
        self.current_aggregator = None

    @staticmethod
    def _get_aggregator(op_description: dict, fl_ctx: FLContext):
        pass

    def operate(
        self,
        op_description: dict,
        controller: ControllerSpec,
        task_name: str,
        task_data: Shareable,
        abort_signal: Signal,
        fl_ctx: FLContext,
    ) -> Union[Shareable, None]:
        pass

    def _process_bcast_result(self, client_task: ClientTask, fl_ctx: FLContext) -> None:
        pass

    def process_result_of_unknown_task(
        self, client: Client, task_name: str, client_task_id: str, result: Shareable, fl_ctx: FLContext
    ):
        pass


class RelayOperator(OperatorSpec, FLComponent):

    _PROP_LAST_RESULT = "last_result"
    _PROP_SHAREABLE_GEN = "shareable_generator"

    def __init__(self):
        OperatorSpec.__init__(self)
        FLComponent.__init__(self)

    @staticmethod
    def _get_shareable_generator(op_description: dict, fl_ctx: FLContext):
        pass

    @staticmethod
    def _get_persistor(op_description: dict, fl_ctx: FLContext):
        pass

    def operate(
        self,
        op_description: dict,
        controller: ControllerSpec,
        task_name: str,
        task_data: Shareable,
        abort_signal: Signal,
        fl_ctx: FLContext,
    ) -> Union[None, Shareable]:
        pass

    def _process_relay_result(self, client_task: ClientTask, fl_ctx: FLContext):
        # submitted shareable is stored in client_task.result
        # we need to update task.data with that shareable so the next target
        # will get the updated shareable
        pass


class HubController(Controller):
    def __init__(
        self,
        pipe_id: str,
        task_wait_time=None,
        task_data_poll_interval: float = 0.1,
    ):
        Controller.__init__(self)

        check_positive_number("task_data_poll_interval", task_data_poll_interval)
        check_str("pipe_id", pipe_id)
        if task_wait_time is not None:
            check_positive_number("task_wait_time", task_wait_time)

        self.pipe_id = pipe_id
        self.operator_descs = None
        self.task_wait_time = task_wait_time
        self.task_data_poll_interval = task_data_poll_interval
        self.pipe = None
        self.pipe_handler = None
        self.run_ended = False
        self.task_abort_signal = None
        self.current_task_name = None
        self.current_task_id = None
        self.current_operator = None
        self.builtin_operators = {OperatorMethod.BROADCAST: BcastOperator(), OperatorMethod.RELAY: RelayOperator()}
        self.project_name = ""

    def start_controller(self, fl_ctx: FLContext) -> None:
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def _abort(self, reason: str, abort_signal: Signal, fl_ctx):
        pass

    def _get_operator(self, task_name: str, op_desc: dict, fl_ctx: FLContext):
        pass

    def control_flow(self, abort_signal: Signal, fl_ctx: FLContext):
        pass

    def _control_flow(self, abort_signal: Signal, fl_ctx: FLContext):
        pass

    def _resolve_op_desc(self, op_desc: dict, fl_ctx: FLContext):
        """
        Determine the correct operation description.

        There may be "operators" in job's config_fed_server.json.
        If present, it describes the operations for tasks, and its descriptions override op_desc that comes from task!
        It may specify a different method than the one in op_desc!
        For example, the op_desc may specify the method 'bcast', but the config could specify 'relay'.
        In this case, the 'relay' method will be used.

        Args:
            op_desc: the op description that comes from the task data

        Returns: None

        """
        pass

    def process_result_of_unknown_task(
        self, client: Client, task_name: str, client_task_id: str, result: Shareable, fl_ctx: FLContext
    ):
        # A late reply is received from client.
        # We'll include the late reply into the aggregation only if it's for the same type of tasks (i.e.
        # same task name). Note that the same task name could be used many times (rounds).
        pass

    def stop_controller(self, fl_ctx: FLContext):
        pass
