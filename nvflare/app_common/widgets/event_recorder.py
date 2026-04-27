# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
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

import logging
import os
from typing import Dict

from nvflare.apis.client_engine_spec import ClientEngineSpec
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.server_engine_spec import ServerEngineSpec
from nvflare.apis.shareable import Shareable
from nvflare.widgets.widget import Widget


class _CtxPropReq(object):
    """Requirements of a prop in the FLContext.

    Arguments:
        dtype: data type of the prop.
        is_private: if this prop is private.
        is_sticky: if this prop is sticky.
        allow_none: if this prop can be None
    """

    def __init__(self, dtype, is_private, is_sticky, allow_none: bool = False):
        self.dtype = dtype
        self.is_private = is_private
        self.is_sticky = is_sticky
        self.allow_none = allow_none


class _EventReq(object):
    """Requirements for FL and peer context when an event is fired.

    Arguments:
        ctx_reqs: A dictionary that describes the requirements for fl_ctx. It maps property names to _CtxPropReq
        peer_ctx_reqs: A dictionary that describes the requirements for peer_ctx. It maps property names to _CtxPropReq
    """

    def __init__(
        self,
        ctx_reqs: Dict[str, _CtxPropReq],
        peer_ctx_reqs: Dict[str, _CtxPropReq],
        ctx_block_list: [str] = None,
        peer_ctx_block_list: [str] = None,
    ):
        self.ctx_reqs = ctx_reqs  # prop name => _CtxPropReq
        self.peer_ctx_reqs = peer_ctx_reqs

        if ctx_block_list is None:
            ctx_block_list = []

        if peer_ctx_block_list is None:
            peer_ctx_block_list = []

        self.ctx_block_list = ctx_block_list
        self.peer_ctx_block_list = peer_ctx_block_list


class _EventStats(object):
    """Stats of each event."""

    def __init__(self):
        self.call_count = 0
        self.prop_missing = 0
        self.prop_none_value = 0
        self.prop_dtype_mismatch = 0
        self.prop_attr_mismatch = 0
        self.prop_block_list_violation = 0
        self.peer_ctx_missing = 0


class EventRecorder(Widget):

    _KEY_CTX_TYPE = "ctx_type"
    _KEY_EVENT_TYPE = "event_type"
    _KEY_EVENT_STATS = "event_stats"
    _KEY_EVENT_REQ = "event_req"

    def __init__(self, log_file_name=None):
        """A component to record all system-wide events.

        Args:
            log_file_name (str, optional): the log filename to save recorded events. Defaults to None.
        """
        super().__init__()

        all_ctx_reqs = {
            "__run_num__": _CtxPropReq(dtype=str, is_private=False, is_sticky=True),
            "__identity_name__": _CtxPropReq(dtype=str, is_private=False, is_sticky=True),
        }

        run_req = _EventReq(ctx_reqs=all_ctx_reqs, peer_ctx_reqs={})
        self.event_reqs = {EventType.START_RUN: run_req, EventType.END_RUN: run_req}  # event type => _EventReq
        self.event_stats = {}  # event_type => _EventStats
        self._log_handler_added = False
        self.log_file_name = log_file_name if log_file_name else "event_recorded.txt"

    def event_tag(self, fl_ctx: FLContext):
        pass

    def event_error_tag(self, fl_ctx: FLContext):
        pass

    def validate_prop(self, prop_name: str, req: _CtxPropReq, fl_ctx: FLContext):
        pass

    def check_block_list(self, block_list, fl_ctx: FLContext):
        pass

    def check_props(self, fl_ctx: FLContext):
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass


class ServerEventRecorder(EventRecorder):
    def __init__(self):
        """Server-specific event recorder."""
        super().__init__()

        task_data_filter_reqs = _EventReq(
            ctx_reqs={
                "__engine__": _CtxPropReq(dtype=ServerEngineSpec, is_private=True, is_sticky=True),
                FLContextKey.TASK_ID: _CtxPropReq(dtype=str, is_private=True, is_sticky=False),
                FLContextKey.TASK_NAME: _CtxPropReq(dtype=str, is_private=True, is_sticky=False),
                FLContextKey.TASK_DATA: _CtxPropReq(dtype=Shareable, is_private=True, is_sticky=False, allow_none=True),
                "testPrivateServerSticky": _CtxPropReq(dtype=str, is_private=True, is_sticky=True),
                "testPublicServerSticky": _CtxPropReq(dtype=str, is_private=False, is_sticky=True),
            },
            ctx_block_list=[
                "testPrivateServerNonSticky",
                "testPublicServerNonSticky",
                "testPrivateClientNonSticky",
                "testPublicClientNonSticky",
                "testPrivateClientSticky",
                "testPublicClientSticky",
            ],
            peer_ctx_reqs={
                "__run_num__": _CtxPropReq(dtype=str, is_private=None, is_sticky=None),
                "__identity_name__": _CtxPropReq(dtype=str, is_private=None, is_sticky=None),
                "testPublicClientSticky": _CtxPropReq(dtype=str, is_private=None, is_sticky=None),
            },
            peer_ctx_block_list=[
                "__engine__",
                "testPrivateClientSticky",
                "testPrivateClientNonSticky",
                "testPublicClientNonSticky",
            ],
        )
        self.event_reqs.update(
            {
                EventType.BEFORE_TASK_DATA_FILTER: task_data_filter_reqs,
                EventType.AFTER_TASK_DATA_FILTER: task_data_filter_reqs,
            }
        )

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass


class ClientEventRecorder(EventRecorder):
    def __init__(self):
        """Client-specific event recorder."""
        super().__init__()

        task_data_filter_reqs = _EventReq(
            ctx_reqs={
                "__engine__": _CtxPropReq(dtype=ClientEngineSpec, is_private=True, is_sticky=True),
                FLContextKey.TASK_ID: _CtxPropReq(dtype=str, is_private=True, is_sticky=False),
                FLContextKey.TASK_NAME: _CtxPropReq(dtype=str, is_private=True, is_sticky=False),
                FLContextKey.TASK_DATA: _CtxPropReq(dtype=Shareable, is_private=True, is_sticky=False, allow_none=True),
                "testPrivateClientSticky": _CtxPropReq(dtype=str, is_private=True, is_sticky=True),
                "testPublicClientSticky": _CtxPropReq(dtype=str, is_private=False, is_sticky=True),
            },
            ctx_block_list=[
                "testPrivateServerNonSticky",
                "testPublicServerNonSticky",
                "testPrivateClientNonSticky",
                "testPublicClientNonSticky",
                "testPrivateServerSticky",
                "testPublicServerSticky",
            ],
            peer_ctx_reqs={
                "__run_num__": _CtxPropReq(dtype=str, is_private=None, is_sticky=None),
                "__identity_name__": _CtxPropReq(dtype=str, is_private=None, is_sticky=None),
                "testPublicServerSticky": _CtxPropReq(dtype=str, is_private=None, is_sticky=None),
            },
            peer_ctx_block_list=[
                "__engine__",
                "testPrivateServerSticky",
                "testPrivateServerNonSticky",
                "testPublicServerNonSticky",
            ],
        )
        self.event_reqs.update(
            {
                EventType.BEFORE_TASK_DATA_FILTER: task_data_filter_reqs,
                EventType.AFTER_TASK_DATA_FILTER: task_data_filter_reqs,
            }
        )

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass
