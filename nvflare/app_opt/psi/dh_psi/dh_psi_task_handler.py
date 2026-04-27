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


import collections
from typing import List, Optional

from nvflare.apis.fl_constant import ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.apis.signal import Signal
from nvflare.app_common.abstract.task_handler import TaskHandler
from nvflare.app_common.app_constant import PSIConst
from nvflare.app_common.psi.psi_spec import PSI
from nvflare.app_opt.psi.dh_psi.dh_psi_client import PSIClient
from nvflare.app_opt.psi.dh_psi.dh_psi_server import PSIServer


def check_items_uniqueness(items):
    pass


class DhPSITaskHandler(TaskHandler):
    """Executor for Diffie-Hellman-based Algorithm PSI.

    It handles the communication and FLARE server task delegation
    User will write an interface local component : PSI to provide client items and  get intersection
    """

    def __init__(self, local_psi_id: str):
        super().__init__(local_psi_id, PSI)
        self.bloom_filter_fpr = None
        self.psi_client = None
        self.psi_server = None
        self.intersects: Optional[List[str]] = None
        self.local_psi_handler: Optional[PSI] = None
        self.client_name = None
        self.items = None
        # needed by JobAPI, add the following line to the constructor
        self.local_psi_id = local_psi_id

    def initialize(self, fl_ctx: FLContext):
        pass

    def execute_task(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def create_request(self, shareable: Shareable):
        pass

    def setup(self, shareable: Shareable, client_name: str):
        pass

    def get_items_size(self):
        pass

    def process_request(self, shareable: Shareable):
        pass

    def calculate_intersection(self, shareable: Shareable):
        pass

    def get_items(self):
        pass
