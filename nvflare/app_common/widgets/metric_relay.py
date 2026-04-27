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

from typing import Tuple

from nvflare.apis.analytix import ANALYTIC_EVENT_TYPE
from nvflare.apis.dxo import DXO
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_context import FLContext
from nvflare.apis.utils.analytix_utils import send_analytic_dxo
from nvflare.client.config import ConfigKey
from nvflare.fuel.utils.attributes_exportable import AttributesExportable
from nvflare.fuel.utils.constants import PipeChannelName
from nvflare.fuel.utils.pipe.pipe import Message, Pipe
from nvflare.fuel.utils.pipe.pipe_handler import PipeHandler
from nvflare.widgets.widget import Widget


class MetricRelay(Widget, AttributesExportable):
    def __init__(
        self,
        pipe_id: str,
        read_interval=0.1,
        heartbeat_interval=5.0,
        heartbeat_timeout=60.0,
        pipe_channel_name=PipeChannelName.METRIC,
        event_type: str = ANALYTIC_EVENT_TYPE,
        fed_event: bool = True,
    ):
        super().__init__()
        self.pipe_id = pipe_id
        self._read_interval = read_interval
        self._heartbeat_interval = heartbeat_interval
        self._heartbeat_timeout = heartbeat_timeout
        self.pipe_channel_name = pipe_channel_name
        self.pipe = None
        self.pipe_handler = None
        self._fl_ctx = None
        self._event_type = event_type
        self._fed_event = fed_event

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def _create_pipe_handler(self):
        def _bound_status_cb(msg, _h=handler):
            pass
        pass

    def _pipe_msg_cb(self, msg: Message):
        pass

    def export(self, export_mode: str) -> Tuple[str, dict]:
        pass
