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

import copy
import logging
import os
import random
import threading
import time
import uuid
from typing import Dict, List, Tuple, Union
from urllib.parse import urlparse

from nvflare.apis.fl_constant import ConnectionSecurity
from nvflare.fuel.f3.cellnet.connector_manager import ConnectorManager
from nvflare.fuel.f3.cellnet.credential_manager import CredentialManager
from nvflare.fuel.f3.cellnet.defs import (
    AbortRun,
    AuthenticationError,
    CellPropertyKey,
    InvalidRequest,
    InvalidSession,
    MessageHeaderKey,
    MessagePropKey,
    MessageType,
    ReturnCode,
    ReturnReason,
    ServiceUnavailable,
)
from nvflare.fuel.f3.cellnet.fqcn import FQCN, FqcnInfo, same_family
from nvflare.fuel.f3.cellnet.registry import Callback, Registry
from nvflare.fuel.f3.cellnet.utils import decode_payload, encode_payload, format_log_message, make_reply
from nvflare.fuel.f3.comm_config import CommConfigurator
from nvflare.fuel.f3.communicator import Communicator, MessageReceiver
from nvflare.fuel.f3.connection import Connection
from nvflare.fuel.f3.drivers.driver_params import DriverParams
from nvflare.fuel.f3.drivers.net_utils import enhance_credential_info
from nvflare.fuel.f3.endpoint import Endpoint, EndpointMonitor, EndpointState
from nvflare.fuel.f3.message import Message
from nvflare.fuel.f3.mpm import MainProcessMonitor
from nvflare.fuel.f3.stats_pool import StatsPoolManager
from nvflare.fuel.utils.fobs import FOBSContextKey
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.security.logging import secure_format_exception, secure_format_traceback

_CHANNEL = "cellnet.channel"
_TOPIC_BULK = "bulk"
_TOPIC_BYE = "bye"
_SM_CHANNEL = "credential_manager"
_SM_TOPIC = "key_exchange"

_ONE_MB = 1024 * 1024


class TargetMessage:
    def __init__(
        self,
        target: str,
        channel: str,
        topic: str,
        message: Message,
    ):
        self.target = target
        self.channel = channel
        self.topic = topic
        self.message = message
        message.add_headers(
            {
                MessageHeaderKey.TOPIC: topic,
                MessageHeaderKey.CHANNEL: channel,
                MessageHeaderKey.DESTINATION: target,
            }
        )

    def to_dict(self):
        pass

    @staticmethod
    def from_dict(d: dict):
        pass


class CellAgent:
    """A CellAgent represents a cell in another cell."""

    def __init__(self, fqcn: str, endpoint: Endpoint):
        """

        Args:
            fqcn: FQCN of the cell represented
        """
        err = FQCN.validate(fqcn)
        if err:
            raise ValueError(f"Invalid FQCN '{fqcn}': {err}")

        self.info = FqcnInfo(FQCN.normalize(fqcn))
        self.endpoint = endpoint

    def get_fqcn(self):
        pass


class _Waiter(threading.Event):
    def __init__(self, targets: List[str]):
        super().__init__()
        self.targets = [x for x in targets]
        self.reply_time = {}  # target_id => reply recv timestamp
        self.send_time = time.time()
        self.id = str(uuid.uuid4())
        self.received_replies = {}


def log_messaging_error(
    logger, log_text: str, cell, msg: Union[Message, None], log_except=False, log_level=logging.ERROR
):
    pass


class _BulkSender:
    def __init__(self, cell, target: str, max_queue_size, secure=False):
        self.cell = cell
        self.target = target
        self.max_queue_size = max_queue_size
        self.secure = secure
        self.messages = []
        self.last_send_time = 0
        self.lock = threading.Lock()
        self.logger = get_obj_logger(self)

    def queue_message(self, channel: str, topic: str, message: Message):
        pass

    def send(self):
        pass


def _validate_url(url: str) -> bool:
    pass


class _CounterName:

    LATE = "late"
    SENT = "sent"
    RETURN = "return"
    FORWARD = "forward"
    RECEIVED = "received"
    REPLIED = "replied"
    REPLY_NONE = "no_reply:none"
    NO_REPLY_LATE = "no_reply:late"
    REPLY_NOT_EXPECTED = "no_reply_expected"
    REQ_FILTER_ERROR = "req_filter_error"
    REP_FILTER_ERROR = "rep_filter_error"


class CertificateExchanger:
    """This class handles cert-exchange messages"""

    def __init__(self, core_cell, credential_manager: CredentialManager):

        self.core_cell = core_cell
        self.credential_manager = credential_manager
        self.core_cell.register_request_cb(_SM_CHANNEL, _SM_TOPIC, self._handle_cert_request)

    def get_certificate(self, target: str) -> bytes:

        pass

    def exchange_certificate(self, target: str) -> bytes:
        pass

    def _handle_cert_request(self, request: Message):
        pass


class CoreCell(MessageReceiver, EndpointMonitor):

    APP_ID = 1
    ERR_TYPE_MSG_TOO_BIG = "MsgTooBig"
    ERR_TYPE_COMM = "CommErr"

    ALL_CELLS = {}  # cell name => Cell

    SUB_TYPE_CHILD = 1
    SUB_TYPE_CLIENT = 2
    SUB_TYPE_NONE = 0

    def __init__(
        self,
        fqcn: str,
        root_url: str,
        secure: bool,
        credentials: dict,
        create_internal_listener: bool = False,
        parent_url: str = None,
        parent_resources: dict = None,
        max_timeout=3600,
        bulk_check_interval=0.5,
        bulk_process_interval=0.5,
        max_bulk_size=100,
    ):
        """

        Args:
            fqcn: the Cell's FQCN (Fully Qualified Cell Name)
            credentials: credentials for secure connections
            root_url: the URL for backbone external connection
            secure: secure mode or not
            max_timeout: default timeout for send_and_receive
            create_internal_listener: whether to create an internal listener for child cells
            parent_url: url for connecting to parent cell
            parent_resources: extra resources for making connection to parent

        FQCN is the names of all ancestor, concatenated with dots.


        .. note::

            Internal listener is automatically created for root cells.

        .. code-block:: text

            Example:
                server.J12345       (the cell for job J12345 on the server)
                server              (the root cell of server)
                nih_1.J12345        (the cell for job J12345 on client_1's site)
                client_1.J12345.R0  (the cell for rank R0 of J12345 on client_1 site)
                client_1            (he root cell of client_1)

        """
        if fqcn in self.ALL_CELLS:
            raise ValueError(f"there is already a cell named {fqcn}")

        self.fobs_ctx = {FOBSContextKey.CORE_CELL: self}
        comm_configurator = CommConfigurator()
        self._name = self.__class__.__name__
        self.logger = get_obj_logger(self)
        self.max_msg_size = comm_configurator.get_max_message_size()
        self.comm_configurator = comm_configurator

        err = FQCN.validate(fqcn)
        if err:
            raise ValueError(f"Invalid FQCN '{fqcn}': {err}")

        # Determine the value of 'secure' based on configured connection_security in credentials.
        # If configured, use it; otherwise keep the original value of 'secure'.
        conn_security = credentials.get(DriverParams.CONNECTION_SECURITY.value)
        if conn_security:
            if conn_security == ConnectionSecurity.CLEAR:
                secure = False
            else:
                secure = True

        self.logger.debug(f"connection secure: {secure}")
        self.my_info = FqcnInfo(FQCN.normalize(fqcn))
        self.secure = secure
        self.logger.debug(f"{self.my_info.fqcn}: max_msg_size={self.max_msg_size}")

        if not root_url and not parent_url:
            raise ValueError(f"{self.my_info.fqcn}: neither root_url nor parent_url is provided")

        if self.my_info.is_root and self.my_info.is_on_server:
            if not root_url:
                raise ValueError(f"{self.my_info.fqcn}: root_url is required for server-side cells but not provided")

            if isinstance(root_url, list):
                for url in root_url:
                    if not _validate_url(url):
                        raise ValueError(f"{self.my_info.fqcn}: invalid Root URL '{url}'")
            else:
                if not _validate_url(root_url):
                    raise ValueError(f"{self.my_info.fqcn}: invalid Root URL '{root_url}'")
                root_url = [root_url]
        elif root_url:
            if isinstance(root_url, list):
                # multiple urls are available - randomly pick one
                root_url = random.choice(root_url)
                self.logger.info(f"{self.my_info.fqcn}: use Root URL {root_url}")
            if not _validate_url(root_url):
                raise ValueError(f"{self.my_info.fqcn}: invalid Root URL '{root_url}'")

        if parent_url and not _validate_url(parent_url):
            raise ValueError(f"{self.my_info.fqcn}: invalid Parent URL '{parent_url}'")

        self.root_url = root_url
        self.create_internal_listener = create_internal_listener
        self.parent_url = parent_url
        self.parent_resources = parent_resources
        self.bulk_check_interval = bulk_check_interval
        self.max_bulk_size = max_bulk_size
        self.bulk_checker = None
        self.bulk_senders = {}
        self.bulk_process_interval = bulk_process_interval
        self.bulk_messages = []
        self.bulk_processor = None
        self.bulk_lock = threading.Lock()
        self.bulk_msg_lock = threading.Lock()

        self.agents = {}  # cell_fqcn => CellAgent
        self.agent_lock = threading.Lock()

        self.logger.debug(f"Creating Cell: {self.my_info.fqcn}")

        if credentials:
            enhance_credential_info(credentials)
            self.update_fobs_context({FOBSContextKey.SEC_CREDS: credentials})

        ep = Endpoint(
            name=fqcn,
            conn_props=credentials,
            properties={
                CellPropertyKey.FQCN: self.my_info.fqcn,
            },
        )

        self.communicator = Communicator(local_endpoint=ep)

        self.endpoint = ep
        self.connector_manager = ConnectorManager(
            communicator=self.communicator, secure=secure, comm_configurator=comm_configurator
        )

        self.communicator.register_message_receiver(app_id=self.APP_ID, receiver=self)
        self.communicator.register_monitor(monitor=self)
        self.req_reg = Registry()
        self.in_filter_reg = Registry()  # for any incoming messages
        self.in_req_filter_reg = Registry()  # for request received
        self.out_reply_filter_reg = Registry()  # for reply going out
        self.out_req_filter_reg = Registry()  # for request sent
        self.in_reply_filter_reg = Registry()  # for reply received
        self.error_handler_reg = Registry()
        self.cell_connected_cb = None
        self.cell_connected_cb_args = None
        self.cell_connected_cb_kwargs = None
        self.cell_disconnected_cb = None
        self.cell_disconnected_cb_args = None
        self.cell_disconnected_cb_kwargs = None
        self.message_interceptor = None
        self.message_interceptor_args = None
        self.message_interceptor_kwargs = None

        self.waiters = {}  # req_id => req
        self.stats_lock = threading.Lock()
        self.req_hw = 0
        self.num_sar_reqs = 0  # send-and-receive
        self.num_faf_reqs = 0
        self.num_timeout_reqs = 0

        # req_expiry specifies how long we keep requests in "reqs" table if they are
        # not answered or picked up
        if not max_timeout or max_timeout <= 0:
            max_timeout = 3600  # one hour
        self.max_timeout = max_timeout
        self.asked_to_stop = False
        self.running = False
        self.stopping = False

        # add appropriate drivers based on roles of the cell
        # a cell can have at most two listeners: one for external, one for internal
        self.ext_listeners = {}  # external listeners: url => connector object
        self.ext_listener_lock = threading.Lock()
        self.ext_listener_impossible = False

        self.int_listener = None  # backbone internal listener - only for cells with child cells

        # a cell could have any number of connectors: some for backbone, some for ad-hoc
        self.bb_ext_connector = None  # backbone external connector - only for Client cells
        self.bb_int_connector = None  # backbone internal connector - only for non-root cells

        # ad-hoc connectors: currently only support ad-hoc external connectors
        self.adhoc_connectors = {}  # target cell fqcn => connector
        self.adhoc_connector_lock = threading.Lock()
        self.root_change_lock = threading.Lock()

        self.register_request_cb(channel=_CHANNEL, topic=_TOPIC_BULK, cb=self._receive_bulk_message)
        self.register_request_cb(channel=_CHANNEL, topic=_TOPIC_BYE, cb=self._peer_goodbye)

        self.cleanup_waiter = None
        self.msg_stats_pool = StatsPoolManager.add_time_hist_pool(
            "Request_Response", "Request/response time in secs (sender)", scope=self.my_info.fqcn
        )

        self.req_cb_stats_pool = StatsPoolManager.add_time_hist_pool(
            "Request_Processing",
            "Time spent (secs) by request processing callbacks (receiver)",
            scope=self.my_info.fqcn,
        )

        self.msg_travel_stats_pool = StatsPoolManager.add_time_hist_pool(
            "Msg_Travel", "Time taken (secs) to get here (receiver)", scope=self.my_info.fqcn
        )

        self.sent_msg_size_pool = StatsPoolManager.add_msg_size_pool(
            "Sent_Msg_Sizes", "Sizes of messages sent (MBs)", scope=self.my_info.fqcn
        )

        self.received_msg_size_pool = StatsPoolManager.add_msg_size_pool(
            "Received_Msg_Sizes", "Sizes of messages received (MBs)", scope=self.my_info.fqcn
        )

        counter_names = [_CounterName.SENT]
        self.sent_msg_counter_pool = StatsPoolManager.add_counter_pool(
            name="Sent_Msg_Counters",
            description="Result counters of sent messages",
            counter_names=counter_names,
            scope=self.my_info.fqcn,
        )

        counter_names = [_CounterName.RECEIVED]
        self.received_msg_counter_pool = StatsPoolManager.add_counter_pool(
            name="Received_Msg_Counters",
            description="Result counters of received messages",
            counter_names=counter_names,
            scope=self.my_info.fqcn,
        )
        self.ALL_CELLS[fqcn] = self

        self.credential_manager = CredentialManager(self.endpoint)
        self.cert_ex = CertificateExchanger(self, self.credential_manager)

    def update_fobs_context(self, props: dict):
        pass

    def get_fobs_context(self, props: dict = None):
        """Return a new copy of the fobs context

        Returns: a new copy of the fobs context

        """
        pass

    def log_error(self, log_text: str, msg: Union[None, Message], log_except=False):
        pass

    def log_warning(self, log_text: str, msg: Union[None, Message], log_except=False):
        pass

    def get_root_url_for_child(self):
        pass

    def get_fqcn(self) -> str:
        pass

    def is_cell_reachable(self, target_fqcn: str, for_msg=None) -> bool:
        pass

    def is_cell_connected(self, target_fqcn: str) -> bool:
        pass

    def is_backbone_ready(self):
        """Check if backbone is ready.

        Backbone is the preconfigured network connections, like all the connections from clients to server.
        Adhoc connections are not part of the backbone.
        """
        pass

    def _set_bb_for_client_root(self):
        pass

    def _set_bb_for_client_child(self, parent_url: str, create_internal_listener: bool):
        pass

    def _set_bb_for_server_root(self):
        pass

    def _set_bb_for_server_child(self, parent_url: str, create_internal_listener: bool):
        pass

    def change_server_root(self, to_url: str):
        """Change to a different server url

        Args:
            to_url: the new url of the server root

        Returns:

        """
        pass

    def drop_connectors(self):
        # drop connections to all cells on server and their agents
        # drop the backbone connector
        pass

    def drop_agents(self):
        # drop agents
        pass

    def make_internal_listener(self):
        """
        Create the internal listener for child cells of this cell to connect to.

        Returns:

        """
        pass

    def get_internal_listener_url(self) -> Union[None, str]:
        """Get the cell's internal listener url.

        This method should only be used for cells that need to have child cells.
        The url returned is to be passed to child of this cell to create connection

        Returns: url for child cells to connect

        """
        pass

    def get_internal_listener_params(self) -> Union[None, dict]:
        pass

    def _add_adhoc_connector(self, to_cell: str, url: str):
        pass

    def _create_internal_listener(self):
        # internal listener is always backbone
        pass

    def _create_external_listener(self, url: str):
        pass

    def _create_bb_external_connector(self):
        pass

    def _create_internal_connector(self, url: str, resources=None):
        pass

    def set_cell_connected_cb(self, cb, *args, **kwargs):
        """
        Set a callback that is called when an external cell is connected.

        Args:
            cb: the callback function. It must follow the signature of cell_connected_cb_signature.
            *args: args to be passed to the cb.
            **kwargs: kwargs to be passed to the cb

        Returns: None

        """
        pass

    def set_cell_disconnected_cb(self, cb, *args, **kwargs):
        """
        Set a callback that is called when an external cell is disconnected.

        Args:
            cb: the callback function. It must follow the signature of cell_disconnected_cb_signature.
            *args: args to be passed to the cb.
            **kwargs: kwargs to be passed to the cb

        Returns: None

        """
        pass

    def set_message_interceptor(self, cb, *args, **kwargs):
        """
        Set a callback that is called when a message is received or forwarded.

        Args:
            cb: the callback function. It must follow the signature of message_interceptor_signature.
            *args: args to be passed to the cb.
            **kwargs: kwargs to be passed to the cb

        Returns: None

        """
        pass

    def start(self):
        """
        Start the cell after it is fully set up (connectors and listeners are added, CBs are set up)

        Returns:

        """
        pass

    def stop(self):
        """
        Cleanup the cell. Once the cell is stopped, it won't be able to send/receive messages.

        Returns:

        """
        pass

    def register_request_cb(self, channel: str, topic: str, cb, *args, **kwargs):
        """
        Register a callback for handling request. The CB must follow request_cb_signature.

        Args:
            channel: the channel of the request
            topic: topic of the request
            cb:
            *args:
            **kwargs:

        Returns:

        """
        pass

    def encrypt_payload(self, message: Message):

        pass

    def decrypt_payload(self, message: Message):

        pass

    def add_incoming_filter(self, channel: str, topic: str, cb, *args, **kwargs):
        pass

    def add_incoming_request_filter(self, channel: str, topic: str, cb, *args, **kwargs):
        pass

    def add_outgoing_reply_filter(self, channel: str, topic: str, cb, *args, **kwargs):
        pass

    def add_outgoing_request_filter(self, channel: str, topic: str, cb, *args, **kwargs):
        pass

    def add_incoming_reply_filter(self, channel: str, topic: str, cb, *args, **kwargs):
        pass

    def add_error_handler(self, channel: str, topic: str, cb, *args, **kwargs):
        pass

    def _filter_outgoing_request(self, channel: str, topic: str, request: Message) -> Union[None, Message]:
        pass

    def _try_path(self, fqcn_path: List[str]) -> Union[None, Endpoint]:
        pass

    def _find_endpoint(self, target_fqcn: str, for_msg: Message) -> Tuple[str, Union[None, Endpoint]]:
        pass

    def _try_find_ep(self, target_fqcn: str, for_msg: Message) -> Union[None, Endpoint]:
        pass

    def _send_to_endpoint(self, to_endpoint: Endpoint, message: Message) -> str:
        pass

    def _send_direct_message(self, target_cell, message):
        pass

    def _send_target_messages(
        self,
        target_msgs: Dict[str, TargetMessage],
    ) -> Dict[str, str]:
        pass

    def _send_to_targets(
        self,
        channel: str,
        topic: str,
        targets: Union[str, List[str]],
        message: Message,
    ) -> Dict[str, str]:
        pass

    def send_request(
        self, channel: str, topic: str, target: str, request: Message, timeout=None, secure=False, optional=False
    ) -> Message:
        pass

    def broadcast_multi_requests(
        self, target_msgs: Dict[str, TargetMessage], timeout=None, secure=False, optional=False
    ) -> Dict[str, Message]:
        """
        This is the core of the request/response handling. Be extremely careful when making any changes!
        To maximize the communication efficiency, we avoid the use of locks.
        We use a waiter implemented as a Python threading.Event object.
        We create the waiter, send out messages, set up default responses, and set it up to wait for response.
        Once the waiter is triggered from a reply-receiving thread, we process received results.

        HOWEVER, if the network is extremely fast, the response may already be received even before we finish setting
        up the waiter in this thread!

        We had a very mysterious bug that caused a request to be treated as timeout even though the reply is received.
        It was both threads try to set values to "waiter.replies". In case of extremely fast network, the reply
        processing thread set the reply to "waiter.replies", and then overwritten by this thread with a default timeout
        reply.

        To avoid this kind of problems, we now use two sets of values in the waiter object.
        One set is for this thread: targets
        Another set is for the reply processing thread: received_replies, reply_time

        Args:
            target_msgs: messages to be sent
            timeout: timeout value
            secure: End-end encryption
            optional: whether the message is optional

        Returns: a dict of: target name => reply message

        """
        pass

    def broadcast_request(
        self,
        channel: str,
        topic: str,
        targets: Union[str, List[str]],
        request: Message,
        timeout=None,
        secure=False,
        optional=False,
    ) -> Dict[str, Message]:
        """
        Send a message over a channel to specified destination cell(s), and wait for reply

        Args:
            channel: channel for the message
            topic: topic of the message
            targets: FQCN of the destination cell(s)
            request: message to be sent
            timeout: how long to wait for replies
            secure: End-end encryption
            optional: whether the message is optional

        Returns: a dict of: cell_id => reply message

        """
        pass

    def fire_and_forget(
        self, channel: str, topic: str, targets: Union[str, List[str]], message: Message, secure=False, optional=False
    ) -> Dict[str, str]:
        """
        Send a message over a channel to specified destination cell(s), and do not wait for replies.

        Args:
            channel: channel for the message
            topic: topic of the message
            targets: one or more destination cell IDs. None means all.
            message: message to be sent
            secure: End-end encryption of the message
            optional: whether the message is optional

        Returns: None

        """
        pass

    def queue_message(self, channel: str, topic: str, targets: Union[str, List[str]], message: Message, optional=False):
        pass

    def _peer_goodbye(self, request: Message):
        pass

    def _receive_bulk_message(self, request: Message):
        pass

    def _process_bulk_messages(self):
        pass

    def _process_pending_bulks(self):
        pass

    def _process_one_bulk(self, bulk_request: Message):
        pass

    def fire_multi_requests_and_forget(
        self, target_msgs: Dict[str, TargetMessage], optional=False, secure=False
    ) -> Dict[str, str]:
        pass

    def send_reply(self, reply: Message, to_cell: str, for_req_ids: List[str], secure=False, optional=False) -> str:
        """Send a reply to respond to one or more requests.

        This is useful if the request receiver needs to delay its reply as follows:
            - When a request is received, if it's not ready to reply (e.g. waiting for additional requests from
              other cells), simply remember the REQ_ID and returns None;
            - The receiver may queue up multiple such requests
            - When ready, call this method to send the reply for all the queued requests

        Args:
            reply: the reply message
            to_cell: the target cell
            for_req_ids: the list of req IDs that the reply is for
            secure: End-end encryption
            optional: whether the message is optional

        Returns: an error message if any

        """
        pass

    def _try_cb(self, message, cb, *args, **kwargs):
        pass

    def process_message(self, endpoint: Endpoint, connection: Connection, app_id: int, message: Message):
        # this is the receiver callback
        pass

    def _process_request(self, origin: str, message: Message) -> Union[None, Message]:
        pass

    def _add_to_route(self, message: Message):
        pass

    def _forward(self, endpoint: Endpoint, origin: str, destination: str, msg_type: str, message: Message):
        # not for me - need to forward it
        pass

    def _stats_category(self, message: Message):
        pass

    def _process_reply(self, origin: str, message: Message, msg_type: str):
        pass

    @staticmethod
    def _msg_size_mbs(message: Message):
        pass

    def _process_received_msg(self, endpoint: Endpoint, connection: Connection, message: Message):
        pass

    def _send_reply(self, reply: Message, endpoint: Endpoint):
        pass

    def _check_bulk(self):
        pass

    def state_change(self, endpoint: Endpoint):
        pass

    def get_sub_cell_names(self) -> Tuple[List[str], List[str]]:
        """
        Get cell FQCNs of all subs, which are children or top-level client cells (if my cell is server).

        Returns: fqcns of child cells, fqcns of top-level client cells
        """
        pass

    def _is_my_sub(self, candidate_info: FqcnInfo) -> int:
        pass

    def is_secure(self):
        pass
