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
import uuid
from typing import List

from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import EventScope, FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.security.logging import secure_format_exception

# do not use underscore as key name; otherwise it cannot be removed from ctx
_KEY_EVENT_DEPTH = "###event_depth"
_MAX_EVENT_DEPTH = 20


def fire_event_to_components(event: str, components: List[FLComponent], ctx: FLContext):
    """Fires the specified event and invokes the list of handlers.

    Args:
        event: the event to be fired
        components: components to be invoked
        ctx: context for cross-component data sharing

    Returns: N/A

    """
    pass
