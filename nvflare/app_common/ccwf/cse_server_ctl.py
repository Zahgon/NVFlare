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
import os
import time

from nvflare.apis.controller_spec import ClientTask, Task
from nvflare.apis.dxo import from_shareable
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReturnCode, Shareable
from nvflare.apis.signal import Signal
from nvflare.apis.workspace import Workspace
from nvflare.app_common.app_constant import AppConstants, ModelName
from nvflare.app_common.app_event_type import AppEventType
from nvflare.app_common.ccwf.common import Constant, ModelType, make_task_name
from nvflare.app_common.ccwf.eval_gen import parallel_eval_generator
from nvflare.app_common.ccwf.server_ctl import ServerSideController
from nvflare.app_common.ccwf.val_result_manager import EvalResultManager
from nvflare.fuel.utils.validation_utils import (
    DefaultValuePolicy,
    check_non_negative_int,
    check_positive_number,
    check_str,
    validate_candidate,
    validate_candidates,
)


class _TaskPropKey:
    MODEL_NAME = "model_name"
    MODEL_TYPE = "model_type"
    MODEL_READY = "model_ready"


class CrossSiteEvalServerController(ServerSideController):
    def __init__(
        self,
        task_name_prefix=Constant.TN_PREFIX_CROSS_SITE_EVAL,
        start_task_timeout=Constant.START_TASK_TIMEOUT,
        configure_task_timeout=Constant.CONFIG_TASK_TIMEOUT,
        eval_task_timeout=30,
        task_check_period: float = Constant.TASK_CHECK_INTERVAL,
        job_status_check_interval: float = Constant.JOB_STATUS_CHECK_INTERVAL,
        progress_timeout: float = Constant.WORKFLOW_PROGRESS_TIMEOUT,
        private_p2p: bool = True,
        participating_clients=None,
        evaluators=None,
        evaluatees=None,
        global_model_client=None,
        max_status_report_interval: float = Constant.PER_CLIENT_STATUS_REPORT_TIMEOUT,
        eval_result_dir=AppConstants.CROSS_VAL_DIR,
        max_parallel_actions=1,
    ):
        if not evaluatees:
            evaluatees = []

        if not evaluators:
            evaluators = []

        super().__init__(
            num_rounds=1,
            task_name_prefix=task_name_prefix,
            start_task_timeout=start_task_timeout,
            configure_task_timeout=configure_task_timeout,
            task_check_period=task_check_period,
            job_status_check_interval=job_status_check_interval,
            participating_clients=participating_clients,
            starting_client="",
            starting_client_policy=DefaultValuePolicy.EMPTY,
            max_status_report_interval=max_status_report_interval,
            result_clients=None,
            result_clients_policy=DefaultValuePolicy.EMPTY,
            progress_timeout=progress_timeout,
            private_p2p=private_p2p,
        )

        check_str("eval_result_dir", eval_result_dir)
        check_positive_number("eval_task_timeout", eval_task_timeout)
        check_non_negative_int("max_parallel_actions", max_parallel_actions)

        if not global_model_client:
            global_model_client = ""
        self.global_model_client = global_model_client
        self.prep_model_task_name = make_task_name(task_name_prefix, Constant.BASENAME_PREP_MODEL)
        self.eval_task_name = make_task_name(task_name_prefix, Constant.BASENAME_EVAL)
        self.eval_task_timeout = eval_task_timeout
        self.max_parallel_actions = max_parallel_actions
        self.eval_local = False
        self.eval_global = False
        self.evaluators = evaluators
        self.evaluatees = evaluatees
        self.eval_result_dir = eval_result_dir
        self.global_names = {}
        self.eval_manager = None
        self.current_round = 0

    def start_controller(self, fl_ctx: FLContext):
        pass

    def prepare_config(self):
        pass

    def process_config_reply(self, client_name: str, reply: Shareable, fl_ctx: FLContext) -> bool:
        pass

    def _ask_to_eval(self, evals: list, model_type: str, model_name: str, abort_signal: Signal, fl_ctx: FLContext):
        pass

    def _evaluate_global_models(self, abort_signal: Signal, fl_ctx: FLContext):
        pass

    def _ask_to_prepare_model(self, model_type, model_name, owners, abort_signal: Signal, fl_ctx: FLContext) -> bool:
        pass

    def _evaluate_one_global_model(self, model_name, model_owner, abort_signal: Signal, fl_ctx: FLContext):
        # ask model owners to prepare for eval
        pass

    def _do_eval_actions(self, evaluators, evaluatees, model_type, model_name, abort_signal: Signal, fl_ctx: FLContext):
        pass

    def _evaluate_local_models(self, abort_signal: Signal, fl_ctx: FLContext):
        pass

    def sub_flow(self, abort_signal: Signal, fl_ctx: FLContext):
        pass

    def is_sub_flow_done(self, fl_ctx: FLContext) -> bool:
        pass

    def _process_eval_result(self, client_task: ClientTask, fl_ctx: FLContext):
        # Find name of the client sending this
        pass

    def _process_prep_model_result(self, client_task: ClientTask, fl_ctx: FLContext):
        pass

    def _accept_eval_result(self, client_name: str, result: Shareable, fl_ctx: FLContext):
        pass
