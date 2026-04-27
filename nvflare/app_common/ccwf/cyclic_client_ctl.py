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
import random

from nvflare.apis.fl_constant import FLContextKey, ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.ccwf.client_ctl import ClientSideController
from nvflare.app_common.ccwf.common import Constant, CyclicOrder, ResultType, rotate_to_front
from nvflare.fuel.utils.validation_utils import check_non_empty_str


class CyclicClientController(ClientSideController):
    def __init__(
        self,
        task_name_prefix=Constant.TN_PREFIX_CYCLIC,
        learn_task_name=AppConstants.TASK_TRAIN,
        persistor_id=AppConstants.DEFAULT_PERSISTOR_ID,
        shareable_generator_id=AppConstants.DEFAULT_SHAREABLE_GENERATOR_ID,
        learn_task_check_interval=Constant.LEARN_TASK_CHECK_INTERVAL,
        learn_task_abort_timeout=Constant.LEARN_TASK_ABORT_TIMEOUT,
        learn_task_ack_timeout=Constant.LEARN_TASK_ACK_TIMEOUT,
        final_result_ack_timeout=Constant.FINAL_RESULT_ACK_TIMEOUT,
    ):
        check_non_empty_str("learn_task_name", learn_task_name)
        check_non_empty_str("persistor_id", persistor_id)
        check_non_empty_str("shareable_generator_id", shareable_generator_id)

        super().__init__(
            task_name_prefix=task_name_prefix,
            learn_task_name=learn_task_name,
            persistor_id=persistor_id,
            shareable_generator_id=shareable_generator_id,
            learn_task_check_interval=learn_task_check_interval,
            learn_task_abort_timeout=learn_task_abort_timeout,
            learn_task_ack_timeout=learn_task_ack_timeout,
            final_result_ack_timeout=final_result_ack_timeout,
            allow_busy_task=False,
        )

    @staticmethod
    def _set_task_headers(task_data: Shareable, num_rounds, current_round, client_order):
        pass

    def start_workflow(self, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def do_learn_task(self, name: str, data: Shareable, fl_ctx: FLContext, abort_signal: Signal):
        # set status report of starting task
        pass
