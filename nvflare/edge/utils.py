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
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReturnCode, Shareable, make_reply
from nvflare.edge.constants import EdgeTaskHeaderKey
from nvflare.security.logging import secure_format_exception

TOPIC_PREFIX = "SAGE"


def message_topic_for_task_update(task_name: str) -> str:
    pass


def message_topic_for_task_end(task_name: str) -> str:
    pass


def _make_update_reply(rc: str, seq: int, data: Shareable = None) -> Shareable:
    pass


def process_update_from_child(
    processor: FLComponent,
    update: Shareable,
    current_task_seq: int,
    fl_ctx: FLContext,
    update_f,
    **kwargs,
) -> (bool, Shareable):
    """Process aggregation report sent from a child client.

    Args:
        processor: the component that received the update report from the child.
        update: the report request
        current_task_seq: sequence number of the current task
        fl_ctx: FLContext object
        update_f: the function to be called to process the update report
        **kwargs: args to be passed to update_f

    Returns: a tuple of (whether the report is accepted, reply to be sent back to the reporter).

    """
    pass
