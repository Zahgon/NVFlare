# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
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
import concurrent.futures
import threading
import time
import uuid

from nvflare.apis.fl_constant import ConfigVarName, SystemConfigs
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReservedHeaderKey, ReturnCode, Shareable, make_reply
from nvflare.apis.signal import Signal
from nvflare.apis.utils.fl_context_utils import generate_log_message
from nvflare.fuel.utils.config_service import ConfigService
from nvflare.fuel.utils.log_utils import get_module_logger
from nvflare.fuel.utils.msg_root_utils import delete_msg_root
from nvflare.fuel.utils.validation_utils import check_positive_number
from nvflare.security.logging import secure_format_exception, secure_format_traceback

# Operation Types
OP_REQUEST = "req"
OP_QUERY = "query"
OP_REPLY = "reply"

# Reliable Message headers
HEADER_OP = "rm.op"
HEADER_TOPIC = "rm.topic"
HEADER_TX_ID = "rm.tx_id"
HEADER_PER_MSG_TIMEOUT = "rm.per_msg_timeout"
HEADER_TX_TIMEOUT = "rm.tx_timeout"
HEADER_STATUS = "rm.status"

# Status
STATUS_IN_PROCESS = "in_process"
STATUS_IN_REPLY = "in_reply"
STATUS_NOT_RECEIVED = "not_received"
STATUS_REPLIED = "replied"
STATUS_ABORTED = "aborted"
STATUS_DUP_REQUEST = "dup_request"

# Topics for Reliable Message
TOPIC_RELIABLE_REQUEST = "RM.RELIABLE_REQUEST"
TOPIC_RELIABLE_REPLY = "RM.RELIABLE_REPLY"

PROP_KEY_TX_ID = "RM.TX_ID"
PROP_KEY_TOPIC = "RM.TOPIC"
PROP_KEY_OP = "RM.OP"
PROP_KEY_DEBUG_INFO = "RM.DEBUG_INFO"


def _extract_result(reply: dict, target: str):
    pass


def _status_reply(status: str):
    pass


def _error_reply(rc: str, error: str):
    pass


class _RequestReceiver:
    """This class handles reliable message request on the receiving end"""

    def __init__(self, topic, request_handler_f, executor, per_msg_timeout, tx_timeout):
        """The constructor

        Args:
            topic: The topic of the reliable message
            request_handler_f: The callback function to handle the request in the form of
                request_handler_f(topic: str, request: Shareable, fl_ctx:FLContext)
            executor: A ThreadPoolExecutor
        """
        self.topic = topic
        self.request_handler_f = request_handler_f
        self.executor = executor
        self.per_msg_timeout = per_msg_timeout
        self.tx_timeout = tx_timeout
        self.rcv_time = None
        self.result = None
        self.source = None
        self.tx_id = None
        self.reply_time = None
        self.replying = False
        self.lock = threading.Lock()

    def process(self, request: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def _try_reply(self, fl_ctx: FLContext):
        pass

    def _do_request(self, request: Shareable, fl_ctx: FLContext):
        pass


class _ReplyReceiver:
    """This class handles reliable message replies on the sending end"""

    def __init__(self, tx_id: str, per_msg_timeout: float, tx_timeout: float):
        self.tx_id = tx_id
        self.tx_start_time = time.time()
        self.tx_timeout = tx_timeout
        self.per_msg_timeout = per_msg_timeout
        self.result = None
        self.result_ready = threading.Event()

    def process(self, reply: Shareable) -> Shareable:
        pass


class ReliableMessage:

    _topic_to_handle = {}
    _req_receivers = {}  # tx id => receiver
    _req_completed = {}  # tx id => expiration
    _enabled = False
    _executor = None
    _query_interval = 1.0
    _max_retries = 5
    _reply_receivers = {}  # tx id => receiver
    _tx_lock = threading.Lock()
    _shutdown_asked = False
    _logger = get_module_logger(__module__, __qualname__)

    @classmethod
    def register_request_handler(cls, topic: str, handler_f, fl_ctx: FLContext):
        """Register a handler for the reliable message with this topic

        Args:
            topic: The topic of the reliable message
            handler_f: The callback function to handle the request in the form of
                handler_f(topic, request, fl_ctx)
            fl_ctx: FL Context
        """
        pass

    @classmethod
    def _get_or_create_receiver(cls, topic: str, request: Shareable, handler_f) -> _RequestReceiver:
        pass

    @classmethod
    def _receive_request(cls, topic: str, request: Shareable, fl_ctx: FLContext):
        pass

    @classmethod
    def _receive_reply(cls, topic: str, request: Shareable, fl_ctx: FLContext):
        pass

    @classmethod
    def release_request_receiver(cls, receiver: _RequestReceiver, fl_ctx: FLContext):
        """Release the specified _RequestReceiver from the receiver table.
        This is to be called after the received request is finished.

        Args:
            receiver: the _RequestReceiver to be released
            fl_ctx: the FL Context

        Returns: None

        """
        pass

    @classmethod
    def enable(cls, fl_ctx: FLContext):
        """Enable ReliableMessage. This method can be called multiple times, but only the 1st call has effect.

        Args:
            fl_ctx: FL Context

        Returns:

        """
        pass

    @classmethod
    def _monitor_req_receivers(cls):
        pass

    @classmethod
    def shutdown(cls):
        """Shutdown ReliableMessage.

        Returns:

        """
        pass

    @classmethod
    def _log_msg(cls, fl_ctx: FLContext, msg: str):
        pass

    @classmethod
    def info(cls, fl_ctx: FLContext, msg: str):
        pass

    @classmethod
    def warning(cls, fl_ctx: FLContext, msg: str):
        pass

    @classmethod
    def error(cls, fl_ctx: FLContext, msg: str):
        pass

    @classmethod
    def is_available(cls):
        """Return whether the ReliableMessage service is available

        Returns:

        """
        pass

    @classmethod
    def debug(cls, fl_ctx: FLContext, msg: str):
        pass

    @classmethod
    def send_request(
        cls,
        target: str,
        topic: str,
        request: Shareable,
        per_msg_timeout: float,
        tx_timeout: float,
        abort_signal: Signal,
        fl_ctx: FLContext,
    ) -> Shareable:
        """Send a request reliably.

        Args:
            target: The target cell of this request.
            topic: The topic of the request.
            request: The request to be sent.
            per_msg_timeout (float): Number of seconds to wait for each message before timing out.
            tx_timeout (float): Timeout for the entire transaction.
            abort_signal (Signal): Signal to abort the request.
            fl_ctx (FLContext): Context for federated learning.

        Returns:
            The reply from the peer.

        Note:
            If `tx_timeout` is not specified or is less than or equal to `per_msg_timeout`,
            the request will be sent only once without retrying.

        """
        pass

    @classmethod
    def _send_request(
        cls,
        target: str,
        request: Shareable,
        abort_signal: Signal,
        fl_ctx: FLContext,
        receiver: _ReplyReceiver,
    ) -> Shareable:
        pass

    @classmethod
    def _query_result(
        cls,
        target: str,
        abort_signal: Signal,
        fl_ctx: FLContext,
        receiver: _ReplyReceiver,
    ) -> Shareable:
        pass

    @classmethod
    def _register_completed_req(cls, tx_id, tx_timeout):
        # Remove expired entries, need to use a copy of the keys
        pass
