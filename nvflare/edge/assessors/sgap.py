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
import threading
from typing import Optional

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.abstract.aggregator import Aggregator
from nvflare.app_common.abstract.learnable_persistor import LearnablePersistor
from nvflare.app_common.abstract.model import ModelLearnable, make_model_learnable
from nvflare.app_common.abstract.shareable_generator import ShareableGenerator
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.app_event_type import AppEventType
from nvflare.app_common.shareablegenerators.passthru import PassthroughShareableGenerator
from nvflare.edge.assessor import Assessment, Assessor
from nvflare.fuel.utils.validation_utils import check_str
from nvflare.security.logging import secure_format_exception


class SGAPAssessor(Assessor):

    def __init__(self, shareable_generator_id: str, aggregator_id: str, persistor_id: str):
        """This assessor implements its required logic by using a Shareable Generator, an Aggregator, and a
        Persistor (SGAP).

        Args:
            shareable_generator_id: component ID of the Shareable Generator. If empty, the PassthroughShareableGenerator
                will be used.
            aggregator_id: component ID of the Aggregator.
            persistor_id: component ID of the Persistor. If not specified, the Persistor will load initial model
                and save the final model.
        """
        Assessor.__init__(self)
        check_str("persistor_id", persistor_id)
        check_str("shareable_generator_id", shareable_generator_id)
        check_str("aggregator_id", aggregator_id)

        self.aggregator_id = aggregator_id
        self.shareable_generator_id = shareable_generator_id
        self.persistor_id = persistor_id
        self._global_weights = make_model_learnable({}, {})
        self._aggr_lock = threading.Lock()

        self.shareable_gen = None
        self.aggregator = None
        self.persistor = None

        self.register_event_handler(EventType.START_RUN, self._handle_start_run)

    def _handle_start_run(self, event_type: str, fl_ctx: FLContext):
        pass

    def start_task(self, fl_ctx: FLContext) -> Shareable:
        # Use the Shareable Generator to generate task data
        pass

    def process_child_update(self, data: Shareable, fl_ctx: FLContext) -> (bool, Optional[Shareable]):
        # Process update from child.
        pass

    def end_task(self, fl_ctx: FLContext):
        pass

    def do_assessment(self, fl_ctx: FLContext):
        pass

    def assess(self, fl_ctx: FLContext) -> Assessment:
        pass
