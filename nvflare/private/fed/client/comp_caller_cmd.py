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

from nvflare.private.admin_defs import Message
from nvflare.private.defs import ComponentCallerTopic, RequestHeader
from nvflare.private.fed.client.admin import RequestProcessor
from nvflare.private.fed.client.client_engine_internal_spec import ClientEngineInternalSpec
from nvflare.widgets.comp_caller import ComponentCaller
from nvflare.widgets.widget import WidgetID


class ComponentCallerProcessor(RequestProcessor):
    def get_topics(self) -> [str]:
        pass

    def process(self, req: Message, app_ctx) -> Message:
        pass
