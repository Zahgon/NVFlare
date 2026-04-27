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

import threading
import time
from typing import Optional

from nvflare.apis.event_type import EventType
from nvflare.apis.executor import Executor
from nvflare.apis.fl_constant import FLContextKey, FLMetaKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReturnCode, Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.app_common.app_constant import AppConstants
from nvflare.fuel.utils.constants import PipeChannelName
from nvflare.fuel.utils.pipe.pipe import Message, Pipe
from nvflare.fuel.utils.pipe.pipe_handler import PipeHandler, Topic
from nvflare.fuel.utils.validation_utils import (
    check_non_negative_int,
    check_non_negative_number,
    check_positive_number,
    check_str,
)
from nvflare.security.logging import secure_format_exception


class TaskExchanger(Executor):
    def __init__(
        self,
        pipe_id: str,
        read_interval: float = 0.5,
        heartbeat_interval: float = 5.0,
        heartbeat_timeout: Optional[float] = 60.0,
        resend_interval: float = 2.0,
        max_resends: Optional[int] = None,
        peer_read_timeout: Optional[float] = 60.0,
        task_wait_time: Optional[float] = None,
        result_poll_interval: float = 0.5,
        pipe_channel_name=PipeChannelName.TASK,
    ):
        """Constructor of TaskExchanger.

        Args:
            pipe_id (str): component id of pipe.
            read_interval (float): how often to read from pipe.
            heartbeat_interval (float): how often to send heartbeat to peer.
            heartbeat_timeout (float, optional): how long to wait for a
                heartbeat from the peer before treating the peer as dead,
                0 means DO NOT check for heartbeat.
            resend_interval (float): how often to resend a message if failing to send.
                None means no resend. Note that if the pipe does not support resending,
                then no resend.
            max_resends (int, optional): max number of resend. None means no limit.
                Defaults to None.
            peer_read_timeout (float, optional): time to wait for peer to accept sent message.
            task_wait_time (float, optional): how long to wait for a task to complete.
                None means waiting forever. Defaults to None.
            result_poll_interval (float): how often to poll task result.
                Defaults to 0.5.
            pipe_channel_name: the channel name for sending task requests.
                Defaults to "task".
        """
        Executor.__init__(self)
        check_str("pipe_id", pipe_id)
        check_positive_number("read_interval", read_interval)
        check_positive_number("heartbeat_interval", heartbeat_interval)
        if heartbeat_timeout is not None:
            check_non_negative_number("heartbeat_timeout", heartbeat_timeout)
        check_positive_number("resend_interval", resend_interval)
        if max_resends is not None:
            check_non_negative_int("max_resends", max_resends)
        if peer_read_timeout is not None:
            check_positive_number("peer_read_timeout", peer_read_timeout)
        if task_wait_time is not None:
            check_positive_number("task_wait_time", task_wait_time)
        check_positive_number("result_poll_interval", result_poll_interval)
        check_str("pipe_channel_name", pipe_channel_name)

        self.pipe_id = pipe_id
        self.read_interval = read_interval
        self.heartbeat_interval = heartbeat_interval
        self.heartbeat_timeout = heartbeat_timeout
        self.resend_interval = resend_interval
        self.max_resends = max_resends
        self.peer_read_timeout = peer_read_timeout
        self.task_wait_time = task_wait_time
        self.result_poll_interval = result_poll_interval
        self.pipe_channel_name = pipe_channel_name
        self.pipe = None
        self.pipe_handler = None
        self._executing = threading.Event()
        self._executing_lock = threading.Lock()

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def _create_pipe_handler(self):
        """Create a new PipeHandler for self.pipe with a handler-bound status callback.

        Each handler gets its own closure that checks identity before stopping,
        so a late PEER_GONE from a previous handler cannot kill the current one.
        The callback uses close_pipe=False because CellPipe.close() is irreversible.
        """
        def _bound_status_cb(msg, _h=handler):
            pass
        pass

    def execute(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        """
        The TaskExchanger always sends the Shareable to the peer, and expects to receive a Shareable object from the
        peer. The peer can convert the Shareable object to whatever format that is best for its applications (e.g.
        DXO or FLModel object). Similarly, when submitting result, the peer must convert its result object to a
        Shareable object before sending it back to the TaskExchanger.

        This "late-binding" (binding of the Shareable object to an application-friendly object) strategy makes the
        TaskExchanger generic and can be reused for any applications (e.g. Shareable based, DXO based, or any custom
        data based).
        """
        pass

    def _do_execute(self, task_name: str, shareable: Shareable, fl_ctx: FLContext, abort_signal: Signal) -> Shareable:
        pass

    def check_input_shareable(self, task_name: str, shareable: Shareable, fl_ctx: FLContext) -> bool:
        """Checks input shareable before execute.

        Returns:
            True, if input shareable looks good; False, otherwise.
        """
        pass

    def check_output_shareable(self, task_name: str, shareable: Shareable, fl_ctx: FLContext) -> bool:
        """Checks output shareable after execute.

        Returns:
            True, if output shareable looks good; False, otherwise.
        """
        pass

    def ask_peer_to_end(self, fl_ctx: FLContext) -> bool:
        pass

    def peer_is_up_or_dead(self) -> bool:
        pass

    def reset_peer_is_up_or_dead(self):
        pass

    def pause_pipe_handler(self):
        """Stops pipe_handler heartbeat."""
        pass

    def resume_pipe_handler(self):
        """Resumes pipe_handler heartbeat."""
        pass

    def get_pipe(self):
        """Gets pipe."""
        pass

    def get_pipe_channel_name(self):
        """Gets pipe_channel_name."""
        pass
