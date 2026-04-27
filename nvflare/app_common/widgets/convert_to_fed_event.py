# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
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

from typing import List

from nvflare.apis.fl_constant import EventScope, FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.widgets.widget import Widget

FED_EVENT_PREFIX = "fed."


class ConvertToFedEvent(Widget):
    def __init__(self, events_to_convert: List[str], fed_event_prefix=FED_EVENT_PREFIX):
        """Converts local event to federated events.

        Args:
            events_to_convert (List[str]): A list of event names to be converted.
            fed_event_prefix (str): The prefix that will be added to the converted event's name.
        """
        super().__init__()
        self.events_to_convert = events_to_convert
        self.fed_event_prefix = fed_event_prefix

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass
