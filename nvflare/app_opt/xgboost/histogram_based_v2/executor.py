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

from nvflare.apis.event_type import EventType
from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import FLContextKey, ReservedKey, ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.app_opt.xgboost.histogram_based_v2.adaptors.xgb_adaptor import XGBClientAdaptor
from nvflare.fuel.f3.cellnet.fqcn import FQCN
from nvflare.security.logging import secure_format_exception

from .defs import Constant


class XGBExecutor(Executor):
    def __init__(
        self,
        adaptor_component_id: str,
        configure_task_name=Constant.CONFIG_TASK_NAME,
        start_task_name=Constant.START_TASK_NAME,
        per_msg_timeout=10.0,
        tx_timeout=100.0,
    ):
        """Constructor

        Args:
            adaptor_component_id: the component ID of client target adaptor
            configure_task_name: name of the config task
            start_task_name: name of the start task
            per_msg_timeout: timeout for sending one message
            tx_timeout: transaction timeout
        """
        Executor.__init__(self)
        self.adaptor_component_id = adaptor_component_id
        self.per_msg_timeout = per_msg_timeout
        self.tx_timeout = tx_timeout
        self.configure_task_name = configure_task_name
        self.start_task_name = start_task_name
        self.adaptor = None

        # create the abort signal to be used for signaling the adaptor
        self.abort_signal = Signal()

    def get_adaptor(self, fl_ctx: FLContext):
        """Get adaptor to be used by this executor.
        This is the default implementation that gets the adaptor based on configured adaptor_component_id.
        A subclass of XGBExecutor may get adaptor in a different way.

        Args:
            fl_ctx: the FL context

        Returns: a XGBClientAdaptor object

        """
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def execute(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def _notify_client_done(self, rc, fl_ctx: FLContext):
        """This is called when the XGB client target is done.
        We send a message to the FL server telling it that this client is done.

        Args:
            rc: the return code from the XGB client target
            fl_ctx: FL context

        Returns: None

        """
        pass
