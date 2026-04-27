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
import time

from nvflare.apis.fl_context import FLContext
from nvflare.edge.assessor import Assessment
from nvflare.edge.assessors.sgap import SGAPAssessor


class CountAssessor(SGAPAssessor):
    def __init__(
        self,
        shareable_generator_id: str,
        aggregator_id: str,
        persistor_id: str,
        min_count: int,
        max_count: int,
        timeout: float,
    ):
        SGAPAssessor.__init__(self, shareable_generator_id, aggregator_id, persistor_id)
        self.min_count = min_count
        self.max_count = max_count
        self.timeout = timeout
        self._start_time = None

    def start_task(self, fl_ctx: FLContext):
        pass

    def end_task(self, fl_ctx: FLContext):
        pass

    def do_assessment(self, fl_ctx: FLContext) -> Assessment:
        pass
