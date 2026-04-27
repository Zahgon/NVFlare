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

import threading
import time

from nvflare.apis.client_engine_spec import ClientEngineSpec
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import EventScope, FedEventHeader, FLContextKey, ReservedKey, ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.server_engine_spec import ServerEngineSpec
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.widgets.widget import Widget

FED_EVENT_TOPIC = "fed.event"


class FedEventRunner(Widget):
    def __init__(self, topic=FED_EVENT_TOPIC, regular_interval=0.01, grace_period=2.0, queue_empty_period=2.0):
        """Init FedEventRunner.

        The FedEventRunner handles posting and receiving of fed events.
        The system will do its best to fire off all events in the queue before shutdown
        using the ABOUT_TO_END_RUN event and a grace period during END_RUN.

        Args:
            topic: the fed event topic to be handled. Defaults to 'fed.event'
        """
        Widget.__init__(self)
        self.topic = topic
        self.abort_signal = None
        self.asked_to_stop = False
        self.regular_interval = regular_interval
        self.grace_period = grace_period
        self.queue_empty_period = queue_empty_period
        self.engine = None
        self.last_timestamps = {}  # client name => last_timestamp
        self.in_events = []
        self.in_lock = threading.Lock()
        self.last_queue_empty_time = time.time()  # last time when the in_events queue became empty
        self.poster = None

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def fire_and_forget_request(self, request: Shareable, fl_ctx: FLContext, targets=None, secure=False):
        pass

    def _receive(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def _post(self):
        """Post an event.

        During ABOUT_TO_END_RUN, sleep_time is 0 and system will flush
         in_events by firing events without delay.

        During END_RUN, system will wait for self.grace_period, even the queue is empty,
        so any new item can be processed.

        However, since the system does not guarantee the receiving side of _post is still
        alive, we catch the exception and show warning messages to users if events can not
        be handled by receiving side.
        """
        pass


class ServerFedEventRunner(FedEventRunner):
    def __init__(self, topic=FED_EVENT_TOPIC, regular_interval=0.01, grace_period=2.0, queue_empty_period=2.0):
        """Init ServerFedEventRunner."""
        FedEventRunner.__init__(self, topic, regular_interval, grace_period, queue_empty_period)

    def fire_and_forget_request(self, request: Shareable, fl_ctx: FLContext, targets=None, secure=False):
        pass


class ClientFedEventRunner(FedEventRunner):
    def __init__(self, topic=FED_EVENT_TOPIC):
        """Init ClientFedEventRunner."""
        FedEventRunner.__init__(self, topic)
        self.ready = False

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def fire_and_forget_request(self, request: Shareable, fl_ctx: FLContext, targets=None, secure=False):
        pass
