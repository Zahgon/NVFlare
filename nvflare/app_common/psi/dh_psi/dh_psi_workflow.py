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

from typing import Dict, List, NamedTuple, Set

from nvflare.apis.dxo import DXO
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.apis.signal import Signal
from nvflare.app_common.app_constant import PSIConst
from nvflare.app_common.psi.psi_workflow_spec import PSIWorkflow
from nvflare.app_common.workflows.broadcast_operator import BroadcastAndWait
from nvflare.utils.decorators import measure_time


class SiteSize(NamedTuple):
    name: str
    size: int


class DhPSIWorkFlow(PSIWorkflow):
    def __init__(self, bloom_filter_fpr: float = 1e-11):
        super().__init__()
        self.task_name = PSIConst.TASK
        self.bloom_filter_fpr: float = bloom_filter_fpr
        self.wait_time_after_min_received = 0
        self.abort_signal = None
        self.fl_ctx = None
        self.controller = None
        self.ordered_sites: List[SiteSize] = []
        self.forward_processed: Dict[str, int] = {}
        self.backward_processed: Dict[str, int] = {}

    def initialize(self, fl_ctx: FLContext, **kwargs):
        pass

    def pre_process(self, abort_signal: Signal) -> bool:
        # ask client send back their item sizes
        # sort client by ascending order
        pass

    def run(self, abort_signal: Signal):
        pass

    def check_processed_sites(self, last_site: SiteSize, processed_sites: Dict[str, int]):
        pass

    def check_final_intersection_sizes(self, intersect_site: SiteSize):
        pass

    def log_pass_time_taken(self):
        pass

    def post_process(self, abort_signal: Signal):
        pass

    def finalize(self, fl_ctx: FLContext):
        pass

    @staticmethod
    def get_ordered_sites(results: Dict[str, DXO]):
        def compare_fn(e):
            pass
        pass

    @measure_time
    def forward_pass(self, ordered_sites: List[SiteSize], processed: Dict[str, int]) -> SiteSize:
        pass

    def pairwise_setup(self, ordered_sites: List[SiteSize]):
        pass

    def pairwise_requests(self, ordered_sites: List[SiteSize], setup_msgs: Dict[str, str]):
        pass

    def pairwise_responses(self, ordered_sites: List[SiteSize], request_msgs: Dict[str, str]):
        pass

    def pairwise_intersect(self, ordered_sites: List[SiteSize], response_msg: Dict[str, str]):
        pass

    def parallel_forward_pass(self, target_sites, processed: dict):
        pass

    @measure_time
    def backward_pass(self, ordered_clients: list, intersect_site: SiteSize) -> dict:
        pass

    @measure_time
    def parallel_backward_pass(self, ordered_clients: list, intersect_site: SiteSize):
        # parallel version
        pass

    def calculate_intersections(self, response_msg) -> Dict[str, int]:
        pass

    def process_requests(self, s: SiteSize, request_msgs: Dict[str, str]) -> Dict[str, str]:
        pass

    def create_requests(self, site_setup_msgs) -> Dict[str, str]:
        pass

    def get_updated_site_sizes(self, ordered_sites):
        pass

    def prepare_sites(self, abort_signal):

        pass

    def prepare_setup_messages(self, s: SiteSize, other_site_sizes: Set[int]) -> Dict[str, str]:
        pass
