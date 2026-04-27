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
from collections import deque
from typing import Optional

from nvflare.apis.signal import Signal
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.fuel.utils.pipe.pipe import HEARTBEAT_SEND_TIMEOUT, Message, Pipe, Topic
from nvflare.fuel.utils.validation_utils import (
    check_callable,
    check_non_negative_number,
    check_object_type,
    check_positive_number,
)
from nvflare.security.logging import secure_format_exception


class PipeHandler(object):
    """Monitors a pipe for messages from the peer.

    PipeHandler reads the pipe periodically and puts received data
    in a message queue in the order the data is received.

    If the received data indicates a peer status change (END, ABORT, GONE):

        - The data will be added to the message queue if the status callback is not registered.
        - Otherwise, the data will NOT be added to the message queue, the status callback will
          be called with the data.

    The PipeHandler should be used as follows:
        - The app creates a pipe and then creates the PipeHandler object for the pipe;
        - The app starts the PipeHandler. This step must be performed, or data in the pipe won't be read.
        - The app should call handler.get_next() periodically to process the message in the queue. This method may return
          None if there is no message in the queue. The app also must handle the status change event from the peer if it
          does not set the status callback. The status change event has the special topic value of Topic.END or Topic.ABORT.
        - Optionally, the app can set a status callback and handle the peer's status change immediately.
        - Stop the handler when the app is finished.

    .. note::

        The handler uses a heartbeat mechanism to detect that the peer may be disconnected (gone).
        It sends a heartbeat message to the peer based on configured interval.
        It also expects heartbeats from the peer.
        If peer's heartbeat is not received for configured time, it will be treated as disconnected,
        and a GONE status is generated for the app to handle.

    """

    def __init__(
        self,
        pipe: Pipe,
        read_interval=0.1,
        heartbeat_interval=5.0,
        heartbeat_timeout=30.0,
        resend_interval=2.0,
        max_resends=5,
        default_request_timeout=5.0,
    ):
        """Constructor of the PipeHandler.

        Args:
            pipe (Pipe): the pipe to be monitored.
            read_interval (float): how often to read from the pipe.
            heartbeat_interval (float): how often to send a heartbeat to the peer.
            heartbeat_timeout (float): how long to wait for a heartbeat from the peer before treating the peer as gone,
                0 means DO NOT check for heartbeat.
            resend_interval (float): how often to resend a message if failing to send. None means no resend.
                Note that if the pipe does not support resending, then no resend.
            max_resends (int, optional): max number of resends. None means no limit.
            default_request_timeout (float): default timeout for request if timeout not specified.
        """
        check_positive_number("read_interval", read_interval)
        check_positive_number("heartbeat_interval", heartbeat_interval)
        check_non_negative_number("heartbeat_timeout", heartbeat_timeout)
        check_object_type("pipe", pipe, Pipe)

        if 0 < heartbeat_timeout <= heartbeat_interval:
            raise ValueError(f"heartbeat_interval {heartbeat_interval} must < heartbeat_timeout {heartbeat_timeout}")

        self.logger = get_obj_logger(self)
        self.pipe = pipe
        self.read_interval = read_interval
        self.heartbeat_interval = heartbeat_interval
        self.heartbeat_timeout = heartbeat_timeout
        self.default_request_timeout = default_request_timeout
        self.resend_interval = resend_interval
        self.max_resends = max_resends
        self.messages = deque([])
        self.reader = threading.Thread(target=self._read)
        self.reader.daemon = True
        self.asked_to_stop = False
        self.lock = threading.Lock()
        self.status_cb = None
        self.cb_args = None
        self.cb_kwargs = None
        self.msg_cb = None
        self.msg_cb_args = None
        self.msg_cb_kwargs = None
        self.peer_is_up_or_dead = threading.Event()
        self._pause = False
        self._last_heartbeat_received_time = None
        self._check_interval = 0.01
        self.heartbeat_sender = threading.Thread(target=self._heartbeat)
        self.heartbeat_sender.daemon = True

    def set_status_cb(self, cb, *args, **kwargs):
        """Sets a callback function for status handling.

        When the peer status is changed (ABORT, END, GONE), this callback is called.
        If callback is not set, the handler simply adds the status change event (topic) to the message queue.

        The callback function must conform to this signature:

        .. code-block: python

            cb(msg, *args, **kwargs)

        where the *args and *kwargs are ones passed to this call.
        The cb is called from the thread that reads from the pipe, hence it should be short-lived.
        Do not put heavy processing logic in the cb.

        Args:
            cb: the callback function.
            *args: the args to be passed to the cb
            **kwargs: the kwargs to be passed to the cb

        Returns: None

        """
        pass

    def set_message_cb(self, cb, *args, **kwargs):
        """Sets a callback function for message handling.

        When a regular message is received, this cb is called.
        If the cb is not set, the handler simply adds the received msg to the message queue.
        If the cb is set, the received msg will NOT be added to the message queue.

        The cb must conform to this signature:

        .. code-block: python

            cb(msg, *args, **kwargs)

        where the *args and *kwargs are ones passed to this call.

        The cb is called from the thread that reads from the pipe, hence it should be short-lived.
        Do not put heavy processing logic in the CB.

        Args:
            cb: the callback func
            *args: the args to be passed to the cb
            **kwargs: the kwargs to be passed to the cb

        Returns: None

        """
        pass

    def _send_to_pipe(self, msg: Message, timeout=None, abort_signal: Signal = None):
        pass

    def _is_stopped_or_aborted(self, abort_signal: Optional[Signal] = None):
        pass

    def start(self):
        """Starts the PipeHandler.

        Note:
            Before calling this method, the pipe managed by this PipeHandler must have been opened.
        """
        pass

    def stop(self, close_pipe=True):
        """Stops the handler and optionally close the monitored pipe.

        Args:
            close_pipe: whether to close the monitored pipe.
        """
        pass

    @staticmethod
    def _make_event_message(topic: str, data):
        pass

    def send_to_peer(self, msg: Message, timeout=None, abort_signal: Signal = None) -> bool:
        """Sends a message to peer.

        Args:
            msg: message to be sent
            timeout: how long to wait for the peer to read the data.
                If not specified, will use ``self.default_request_timeout``.
            abort_signal:

        Returns:
            Whether the peer has read the data.
        """
        pass

    def notify_end(self, data):
        """Notifies the peer that the communication is ended normally."""
        pass

    def notify_abort(self, data):
        """Notifies the peer that the communication is aborted."""
        pass

    def _add_message(self, msg: Message):
        pass

    def _read(self):
        pass

    def _try_read(self):
        pass

    def _heartbeat(self):
        pass

    def get_next(self) -> Optional[Message]:
        """Gets the next message from the message queue.

        Returns:
            A Message at the top of the message queue.
            If the queue is empty, returns None.
        """
        pass

    def pause(self):
        """Stops heartbeat checking and sending."""
        pass

    def resume(self):
        """Resumes heartbeat checking and sending."""
        pass
