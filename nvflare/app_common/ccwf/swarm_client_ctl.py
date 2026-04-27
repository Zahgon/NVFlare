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
import random
import threading
import time

from nvflare.apis.controller_spec import Task
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import FLContextKey, ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReservedHeaderKey, Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.app_common.abstract.aggregator import Aggregator
from nvflare.app_common.abstract.learnable import Learnable
from nvflare.app_common.abstract.metric_comparator import MetricComparator
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.app_event_type import AppEventType
from nvflare.app_common.ccwf.client_ctl import ClientSideController
from nvflare.app_common.ccwf.common import Constant, NumberMetricComparator, ResultType, make_task_name
from nvflare.fuel.utils.validation_utils import check_non_empty_str, check_positive_int, check_positive_number
from nvflare.security.logging import secure_format_traceback


class _TrainerStatus:
    def __init__(self, name: str):
        self.name = name
        self.last_submit_req_time = None  # the last time this trainer requested to submit result
        self.busy = False  # whether this trainer is busy
        self.reply_time = None  # the time this trainer's result is received


class Gatherer(FLComponent):
    def __init__(
        self,
        task_data: Shareable,
        fl_ctx: FLContext,
        for_round: int,
        executor: ClientSideController,
        aggregator: Aggregator,
        metric_comparator: MetricComparator,
        all_clients: list,
        trainers: list,
        min_responses_required: int,
        wait_time_after_min_resps_received: float,
        timeout,
        max_concurrent_submissions: int = 1,
    ):
        FLComponent.__init__(self)
        self.fl_ctx = fl_ctx
        self.executor = executor
        self.aggregator = aggregator
        self.metric_comparator = metric_comparator
        self.all_clients = all_clients
        self.trainers = trainers
        self.for_round = for_round
        self.trainer_statuses = {}
        self.start_time = time.time()
        self.timeout = timeout
        self.max_concurrent_submissions = max_concurrent_submissions

        for t in trainers:
            self.trainer_statuses[t] = _TrainerStatus(t)
        if min_responses_required <= 0 or min_responses_required >= len(trainers):
            min_responses_required = len(trainers)
        self.min_responses_required = min_responses_required
        self.wait_time_after_min_resps_received = wait_time_after_min_resps_received
        self.min_resps_received_time = None
        self.lock = threading.Lock()
        self.perm_lock = threading.Lock()
        self.current_best_client = task_data.get_header(Constant.CLIENT)
        self.current_best_global_metric = task_data.get_header(Constant.METRIC)
        self.current_best_round = task_data.get_header(Constant.ROUND)
        if not self.current_best_client:
            self.log_info(fl_ctx, "gatherer starting from scratch")
        else:
            self.log_info(
                fl_ctx,
                f"gatherer starting with previous best result from client {self.current_best_client} "
                f"with metric {self.current_best_global_metric} "
                f"at round {self.current_best_round}",
            )

    def gather(self, client_name: str, result: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def can_accept_submission(self, client_name: str, result: Shareable, fl_ctx: FLContext) -> str:
        pass

    def _do_gather(self, client_name: str, result: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def aggregate(self):
        pass

    def is_done(self):
        pass


class SwarmClientController(ClientSideController):
    def __init__(
        self,
        task_name_prefix=Constant.TN_PREFIX_SWARM,
        learn_task_name=AppConstants.TASK_TRAIN,
        persistor_id=AppConstants.DEFAULT_PERSISTOR_ID,
        shareable_generator_id=AppConstants.DEFAULT_SHAREABLE_GENERATOR_ID,
        aggregator_id=AppConstants.DEFAULT_AGGREGATOR_ID,
        metric_comparator_id=None,
        learn_task_check_interval=Constant.LEARN_TASK_CHECK_INTERVAL,
        learn_task_abort_timeout=Constant.LEARN_TASK_ABORT_TIMEOUT,
        learn_task_ack_timeout=Constant.LEARN_TASK_ACK_TIMEOUT,
        learn_task_timeout=None,
        final_result_ack_timeout=Constant.FINAL_RESULT_ACK_TIMEOUT,
        min_responses_required: int = 1,
        wait_time_after_min_resps_received: float = 10.0,
        request_to_submit_result_max_wait=None,
        request_to_submit_result_msg_timeout=5.0,
        request_to_submit_result_interval: float = 1.0,
        max_concurrent_submissions: int = 1,
        memory_gc_rounds: int = 1,
        cuda_empty_cache: bool = False,
    ):
        """
        Constructor of a ClientSideController object.

        Args:
            task_name_prefix: prefix of task names. All CCWF task names are prefixed with this.
            learn_task_name: name for the Learning Task (LT)
            persistor_id: ID of the persistor component
            shareable_generator_id: ID of the shareable generator component
            aggregator_id: ID of the aggregator
            metric_comparator_id: ID of metric comparator to be used for determining best model.
                If not specified, the default NumberMetricComparator is used.
            learn_task_check_interval: interval for checking incoming Learning Task (LT)
            learn_task_ack_timeout: timeout for sending the LT to other client(s)
            learn_task_timeout: max time allowed for a training task
            final_result_ack_timeout: timeout for sending final result to participating clients
            learn_task_abort_timeout: time to wait for the LT to become stopped after aborting it
            min_responses_required: minimum number of responses required for the aggregation
            wait_time_after_min_resps_received: how long to wait after min responses (but not all responses)
                are received.
            request_to_submit_result_max_wait: max amount of time to wait for the permission from the
                aggregation client. If the permission is not received within this period of time, the training
                result will not be submitted. If this value is not specified (None), then the training client
                will keep trying forever.
            request_to_submit_result_msg_timeout: the timeout for "submission request" message.
                Since submission req is a tiny message, this timeout value should be small.
            request_to_submit_result_interval: interval between requests to submit result.
            max_concurrent_submissions: max number of concurrent submissions allowed on the aggregation client.
            memory_gc_rounds: run gc.collect() + malloc_trim on the aggregator every N FL rounds.
                Defaults to 1 (every round) to match legacy behavior where gc.collect() was called
                unconditionally after each trainer submission. Set to 0 to disable.
            cuda_empty_cache: also call torch.cuda.empty_cache() during aggregator-side cleanup.
                In swarm learning the aggregator runs on the same client as the trainer, so GPU
                memory may be relevant. Defaults to False.

        Note that if the max_concurrent_submissions is set to 1, it practically means that all training results
        will be submitted to the aggregation client sequentially. This lowers the resource pressure on
        the aggr client, but makes the overall training process longer. The value of request_to_submit_result_max_wait,
        if specified, should be long enough to allow the aggr client sufficient time to process training results.

        """
        check_non_empty_str("learn_task_name", learn_task_name)
        check_non_empty_str("persistor_id", persistor_id)
        check_non_empty_str("shareable_generator_id", shareable_generator_id)
        check_non_empty_str("aggregator_id", aggregator_id)
        check_positive_number("request_to_submit_result_msg_timeout", request_to_submit_result_msg_timeout)
        check_positive_number("request_to_submit_result_interval", request_to_submit_result_interval)
        check_positive_int("max_concurrent_submissions", max_concurrent_submissions)
        if request_to_submit_result_max_wait:
            check_positive_number("request_to_submit_result_max_wait", request_to_submit_result_max_wait)

        if metric_comparator_id:
            check_non_empty_str("metric_comparator_id", metric_comparator_id)

        if learn_task_timeout:
            check_positive_number("learn_task_timeout", learn_task_timeout)

        check_positive_int("min_responses_required", min_responses_required)
        check_positive_number("wait_time_after_min_resps_received", wait_time_after_min_resps_received)

        super().__init__(
            task_name_prefix=task_name_prefix,
            learn_task_name=learn_task_name,
            persistor_id=persistor_id,
            shareable_generator_id=shareable_generator_id,
            learn_task_check_interval=learn_task_check_interval,
            learn_task_ack_timeout=learn_task_ack_timeout,
            learn_task_abort_timeout=learn_task_abort_timeout,
            final_result_ack_timeout=final_result_ack_timeout,
            allow_busy_task=True,
        )
        self.metric_comparator_id = metric_comparator_id
        self.metric_comparator = None
        self.report_learn_result_task_name = make_task_name(task_name_prefix, Constant.BASENAME_REPORT_LEARN_RESULT)
        self.request_to_submit_learn_result_task_name = make_task_name(
            task_name_prefix, Constant.BASENAME_REQUEST_TO_SUBMIT_LEARN_RESULT
        )
        self.max_concurrent_submissions = max_concurrent_submissions
        self.request_to_submit_result_max_wait = request_to_submit_result_max_wait
        self.request_to_submit_result_msg_timeout = request_to_submit_result_msg_timeout
        self.request_to_submit_result_interval = request_to_submit_result_interval
        self.learn_task_timeout = learn_task_timeout
        self.min_responses_required = min_responses_required
        self.wait_time_after_min_resps_received = wait_time_after_min_resps_received
        self.aggregator_id = aggregator_id
        self.aggregator = None
        self.gatherer = None
        self.gatherer_waiter = threading.Event()
        self.trainers = None
        self.aggrs = None
        self.is_trainer = False
        self.is_aggr = False
        self.last_aggr_round_done = -1
        self.memory_gc_rounds = memory_gc_rounds
        self.cuda_empty_cache = cuda_empty_cache
        self._aggr_round_count = 0

    def process_config(self, fl_ctx: FLContext):
        pass

    def execute(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def start_run(self, fl_ctx: FLContext):
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def start_workflow(self, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def _scatter(self, task_data: Shareable, for_round: int, fl_ctx: FLContext) -> bool:
        pass

    def _monitor_gather(self):
        pass

    def _end_gather(self, gatherer: Gatherer):
        pass

    def _ask_to_share_best_result(self, client: str, metric, fl_ctx: FLContext):
        # other client has best model - ask it to distribute its result
        pass

    def _distribute_final_results(self, aggr_result: Shareable, fl_ctx: FLContext):
        pass

    def _process_submission_request(self, topic: str, request: Shareable, fl_ctx: FLContext):
        pass

    @staticmethod
    def _has_lazy_refs(obj) -> bool:
        """Return True if obj (recursively) contains any LazyDownloadRef."""
        pass

    def _resolve_lazy_refs(self, result: Shareable, fl_ctx: FLContext) -> Shareable:
        """Resolve any LazyDownloadRef objects in result by downloading from subprocess.

        When the subprocess sends its result via CellPipe with pass_through_on_send=True,
        Adapter.call() decodes the message with PASS_THROUGH=True and creates
        LazyDownloadRef objects (one per large tensor) instead of downloading the tensors.
        These placeholders carry the subprocess's fqcn and ref_id so that a downstream
        hop can download from the subprocess DownloadService on demand.

        For the remote aggregator path this download is triggered automatically by the
        FOBS encode/decode inside broadcast_and_wait() (Fix 14).  For the local
        aggregation path (aggr == self.me) there is no encode/decode, so we must
        trigger the download explicitly here before the result reaches the gatherer.

        Uses an FOBS round-trip:
          encode: LazyDownloadRefDecomposer.decompose() re-emits the original subprocess
                  datum (fqcn + ref_id) as a TEXT datum — no CELL needed in the encode ctx.
          decode: process_datum() with PASS_THROUGH=False calls _download_from_remote_cell()
                  which downloads real numpy arrays from the subprocess DownloadService.
                  cell.get_fobs_context() supplies the CELL so the download can route to
                  the subprocess via the cell network.
        """
        pass

    def _process_learn_result(self, request: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def do_learn_task(self, name: str, task_data: Shareable, fl_ctx: FLContext, abort_signal: Signal):
        # set status report of starting task
        pass

    def _process_share_result(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        pass
