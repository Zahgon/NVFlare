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
from typing import Any, List, Union

from nvflare.apis.utils.fl_context_utils import generate_log_message
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.security.logging import secure_format_traceback

from .analytix import AnalyticsData, AnalyticsDataType
from .event_type import EventType
from .fl_constant import EventScope, FedEventHeader, FLContextKey, LogMessageTag
from .fl_context import FLContext
from .persistable import StatePersistable
from .shareable import Shareable


class FLComponent(StatePersistable):
    def __init__(self):
        """Init FLComponent.

        The FLComponent is the base class of all FL Components.
        (executors, controllers, responders, filters, aggregators, and widgets are all FLComponents)

        FLComponents have the capability to handle and fire events and contain various methods for logging.
        """
        self._name = self.__class__.__name__
        self.logger = get_obj_logger(self)
        self._event_handlers = {}

    def _self_check(self):
        # This is used to dynamically construct all required elements of FLComponent.
        # We try to make it work for subclasses that fail to call super().__init__(), due to bad programming.
        pass

    @property
    def name(self):
        pass

    def _fire(self, event_type: str, fl_ctx: FLContext):
        pass

    def fire_event(self, event_type: str, fl_ctx: FLContext):
        """Fires an event.

        Args:
            event_type (str): The type of event.
            fl_ctx (FLContext): FLContext information.
        """
        pass

    def fire_event_with_data(self, event_type: str, fl_ctx: FLContext, key: str, data: Any):
        """
        Set the data for the event and clean it up afterward
        """
        pass

    def fire_fed_event(self, event_type: str, event_data: Shareable, fl_ctx: FLContext, targets=None):
        """Fires a federation event.

        A federation event means that the event will be sent to different sites.
        For example, if fire a federation event on the server side, one can decide what clients to send via the
        parameter `targets`.
        If fire a federation event on the client side, the event will be sent to the server.

        Args:
            event_type (str): The type of event.
            event_data (Shareable): The data of this fed event.
            fl_ctx (FLContext): FLContext information.
            targets: The targets to send to. It is only used when fire federation event from server side.
        """
        pass

    def system_panic(self, reason: str, fl_ctx: FLContext):
        """Signals a fatal condition that could cause the RUN to end.

        Args:
            reason (str): The reason for panic.
            fl_ctx (FLContext): FLContext information.
        """
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        """Handles events.

        Args:
            event_type (str): event type fired by workflow.
            fl_ctx (FLContext): FLContext information.
        """
        pass

    def log_info(self, fl_ctx: FLContext, msg: str, fire_event=False):
        """Logs a message with logger.info.

        These log_XXX methods are implemented because we want to have a unified way of logging messages.
        For example, in this method, we are using generate_log_message to add the FLContext information
        into the message. And we can decide whether to fire a log event afterwards.

        Args:
            fl_ctx (FLContext): FLContext information.
            msg (str): The message to log.
            fire_event (bool): Whether to fire a log event.
        """
        pass

    def log_warning(self, fl_ctx: FLContext, msg: str, fire_event=True):
        """Logs a message with logger.warning.

        Args:
            fl_ctx (FLContext): FLContext information.
            msg (str): The message to log.
            fire_event (bool): Whether to fire a log event.
        """
        pass

    def log_error(self, fl_ctx: FLContext, msg: str, fire_event=True):
        """Logs a message with logger.error.

        Args:
            fl_ctx (FLContext): FLContext information.
            msg (str): The message to log.
            fire_event (bool): Whether to fire a log event.
        """
        pass

    def log_debug(self, fl_ctx: FLContext, msg: str, fire_event=False):
        """Logs a message with logger.debug.

        Args:
            fl_ctx (FLContext): FLContext information.
            msg (str): The message to log.
            fire_event (bool): Whether to fire a log event.
        """
        pass

    def log_critical(self, fl_ctx: FLContext, msg: str, fire_event=True):
        """Logs a message with logger.critical.

        Args:
            fl_ctx (FLContext): FLContext information.
            msg (str): The message to log.
            fire_event (bool): Whether to fire a log event.
        """
        pass

    def log_exception(self, fl_ctx: FLContext, msg: str, fire_event=False):
        """Logs exception message with logger.error.

        Args:
            fl_ctx (FLContext): FLContext information.
            msg (str): The message to log.
            fire_event (bool): Whether to fire a log event. Unused.
        """
        pass

    def _fire_log_event(self, event_type: str, log_tag: str, log_msg: str, fl_ctx: FLContext):
        pass

    def register_event_handler(self, event_types: Union[str, List[str]], handler, **kwargs):
        pass

    def get_event_handlers(self):
        pass
