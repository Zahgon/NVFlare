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

from abc import ABC, abstractmethod
from threading import Lock
from typing import List, Optional

from nvflare.apis.analytix import ANALYTIC_EVENT_TYPE, AnalyticsDataType, LogWriterName, TrackConst
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import EventScope, FLContextKey, ReservedKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.apis.utils.analytix_utils import create_analytic_dxo, send_analytic_dxo
from nvflare.widgets.widget import Widget


class AnalyticsSender(Widget):
    def __init__(self, event_type=ANALYTIC_EVENT_TYPE, writer_name=LogWriterName.TORCH_TB):
        """Sender for analytics data.

        This class has some legacy methods that implement some common methods following signatures from
        PyTorch SummaryWriter. New code should use :py:class:`TBWriter <nvflare.app_opt.tracking.tb.tb_writer.TBWriter>` instead,
        which contains an AnalyticsSender.

        Args:
            event_type (str): event type to fire (defaults to "analytix_log_stats").
            writer_name: the log writer for syntax information (defaults to LogWriterName.TORCH_TB)
        """
        super().__init__()
        self.engine = None
        self.event_type = event_type
        self.writer = writer_name

    def get_writer_name(self) -> LogWriterName:
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def add(self, tag: str, value, data_type: AnalyticsDataType, global_step: Optional[int] = None, **kwargs):
        """Create and send a DXO by firing an event.

        Args:
            tag (str): Tag name
            value (_type_): Value to send
            data_type (AnalyticsDataType): Data type of the value being sent
            global_step (optional, int): Global step value.

        Raises:
            TypeError: global_step must be an int
        """
        pass

    def close(self):
        """Close resources."""
        pass


class AnalyticsReceiver(Widget, ABC):
    def __init__(self, events: Optional[List[str]] = None):
        """Receives analytic data.

        Args:
            events (optional, List[str]): A list of event that this receiver will handle.
        """
        super().__init__()
        if events is None:
            events = [ANALYTIC_EVENT_TYPE, f"fed.{ANALYTIC_EVENT_TYPE}"]
        self.events = events
        self._initialized = False
        self._save_lock = Lock()
        self._end = False

    @abstractmethod
    def initialize(self, fl_ctx: FLContext):
        """Initializes the receiver.

        Called after EventType.START_RUN.

        Args:
            fl_ctx (FLContext): fl context.
        """
        pass

    @abstractmethod
    def save(self, fl_ctx: FLContext, shareable: Shareable, record_origin: str):
        """Saves the received data.

        Specific implementations of AnalyticsReceiver will implement save in their own way.

        Args:
            fl_ctx (FLContext): fl context.
            shareable (Shareable): the received message.
            record_origin (str): the sender of this message / record.
        """
        pass

    @abstractmethod
    def finalize(self, fl_ctx: FLContext):
        """Finalizes the receiver.

        Called after EventType.END_RUN.

        Args:
            fl_ctx (FLContext): fl context.
        """
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def _handle_start_run_event(self, fl_ctx: FLContext):
        pass

    def _handle_data_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def _handle_end_run_event(self, fl_ctx: FLContext):
        pass

    def _get_record_origin(self, fl_ctx: FLContext, data: Shareable) -> Optional[str]:
        pass
