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
import gc
import time

from nvflare.apis.controller_spec import Task
from nvflare.apis.fl_constant import FLContextKey, ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable, make_copy, make_reply
from nvflare.apis.signal import Signal
from nvflare.app_common.abstract.model import model_learnable_to_dxo
from nvflare.app_common.abstract.model_persistor import ModelPersistor
from nvflare.app_common.app_constant import AppConstants, ValidateType
from nvflare.app_common.ccwf.client_ctl import ClientSideController
from nvflare.app_common.ccwf.common import Constant, ModelType, make_task_name
from nvflare.fuel.utils.validation_utils import check_non_empty_str, check_positive_number
from nvflare.security.logging import secure_format_exception


class CrossSiteEvalClientController(ClientSideController):
    def __init__(
        self,
        task_name_prefix=Constant.TN_PREFIX_CROSS_SITE_EVAL,
        submit_model_task_name=AppConstants.TASK_SUBMIT_MODEL,
        validation_task_name=AppConstants.TASK_VALIDATION,
        persistor_id=AppConstants.DEFAULT_PERSISTOR_ID,
        get_model_timeout=Constant.GET_MODEL_TIMEOUT,
    ):
        check_positive_number("get_model_timeout", get_model_timeout)
        check_non_empty_str("submit_model_task_name", submit_model_task_name)
        check_non_empty_str("validation_task_name", validation_task_name)
        check_non_empty_str("persistor_id", persistor_id)

        super().__init__(
            task_name_prefix=task_name_prefix,
            learn_task_name="",
            shareable_generator_id="",
            persistor_id=persistor_id,
        )
        self.eval_task_name = make_task_name(task_name_prefix, Constant.BASENAME_EVAL)
        self.prep_model_task_name = make_task_name(task_name_prefix, Constant.BASENAME_PREP_MODEL)
        self.ask_for_model_task_name = make_task_name(task_name_prefix, Constant.BASENAME_ASK_FOR_MODEL)
        self.submit_model_task_name = submit_model_task_name  # this is for the learner executor
        self.validation_task_name = validation_task_name
        self.my_local_model = None
        self.global_model_inventory = None
        self.submit_model_executor = None
        self.validate_executor = None
        self.inventory = None
        self.get_model_timeout = get_model_timeout
        self.prepared_models = {}  # model key => model shareable

    def start_run(self, fl_ctx: FLContext):
        pass

    def execute(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def process_config(self, fl_ctx: FLContext):
        pass

    def start_workflow(self, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    @staticmethod
    def _model_key(model_type: str, model_name: str):
        pass

    def _get_prepared_model(self, model_type: str, model_name: str):
        pass

    def _set_prepared_model(self, model_type: str, model_name: str, model):
        pass

    def _clear_prepared_models(self):
        pass

    def _do_eval(self, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def _prepare_global_model(self, model_name, fl_ctx: FLContext):
        # get it from model inventory
        pass

    def _prepare_local_model(self, model_name, fl_ctx: FLContext, abort_signal: Signal):
        """Prepare the local (client-trained) model for cross-site evaluation.

        Tries the persistor first, then falls back to submit_model_executor.

        Persistor-first is necessary for external-process executors
        (``launch_external_process=True``): the training subprocess has already
        exited when CSE runs, so calling submit_model_executor.execute() launches
        a *fresh* subprocess with no trained model state.  The best model was
        already saved to disk by PTFileModelPersistor during _process_final_result(),
        so loading from the persistor is both correct and efficient (RC12 Bug 2).

        Inventory key selection: the server sends model_name="best_model" (a semantic
        label from ModelName.BEST_MODEL), but PTFileModelPersistor keys are
        filesystem-derived ("FL_global_model", "best_FL_global_model").
        persistor.get("best_model") always returns None, so we scan the inventory.
        When model_name contains "best", we prefer an inventory key containing "best".
        We take the LAST such key (not the first) because PTFileModelPersistor adds
        the source/initial checkpoint first — if it happens to contain "best" in its
        name (e.g. "best_initial_model"), we must not mistake it for the trained best.
        """
        pass

    def _prepare_model(self, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def _process_get_model_request(self, request: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def do_learn_task(self, name: str, task_data: Shareable, fl_ctx: FLContext, abort_signal: Signal):
        pass
