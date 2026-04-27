# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
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
import queue
import threading

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.abstract.aggregator import Aggregator
from nvflare.fuel.utils.validation_utils import check_positive_number, check_str
from nvflare.fuel.utils.waiter_utils import WaiterRC, conditional_wait
from nvflare.security.logging import secure_format_exception

_SHORT_WAIT = 0.1


class _AcceptWaitRC(WaiterRC):
    END_RUN = 10


class _Contribution:

    def __init__(self, data: Shareable, fl_ctx: FLContext):
        self.data = data

        # We need to make a copy of the fl_ctx since it could be used for multiple contributions and its
        # content could be overwritten.
        self.fl_ctx = fl_ctx.clone()


class LazyAggregator(Aggregator):

    def __init__(self, aggregator_id: str, accept_timeout: float = 600.0):
        """Constructor of LazyAggregator.
        LazyAggregator is a wrapper for other aggregators to do accept processing in a separate thread.

        During a typical SAG-based training, updates from clients are processed by the aggregator's "accept" method.
        To ensure the integrity of training task, The SAG workflow processes client updates sequentially.
        If the "accept" method is time-consuming and there are many clients, then the update processing will
        become bottleneck.

        Using the LazyAggregator, the updates from clients are simply added to a queue quickly.
        The actual "accept" processing is done in a separate thread that processes the queued updates sequentially.

        Args:
            aggregator_id: component ID of the real aggregator
            accept_timeout: max amount of time to wait for accept to finish
        """
        Aggregator.__init__(self)
        check_str("aggregator_id", aggregator_id)
        check_positive_number("accept_timeout", accept_timeout)

        self.aggregator_id = aggregator_id
        self.accept_timeout = accept_timeout
        self.aggregator = None
        self.contributions = queue.Queue()
        self._q_lock = threading.Lock()
        self.aggregating = False
        self.run_ended = False
        self.accept_done = threading.Event()
        self.register_event_handler(EventType.START_RUN, self._lazy_aggr_start_run)
        self.register_event_handler(EventType.END_RUN, self._lazy_aggr_end_run)

    def _clear_contributions(self):
        pass

    def _add_contribution(self, contrib: Shareable, fl_ctx: FLContext):
        pass

    def _lazy_aggr_start_run(self, event_type: str, fl_ctx: FLContext):
        pass

    def _lazy_aggr_end_run(self, event_type: str, fl_ctx: FLContext):
        pass

    def accept(self, shareable: Shareable, fl_ctx: FLContext) -> bool:
        pass

    def _do_accept(self):
        # This thread monitors the contribution queue.
        # It takes contributions from the queue and processes them one by one.
        pass

    def aggregate(self, fl_ctx: FLContext) -> Shareable:
        pass

    def _reset(self, fl_ctx: FLContext):
        pass

    def _check_end_run(self):
        pass

    def reset(self, fl_ctx: FLContext):
        pass
