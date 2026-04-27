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
import logging
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional

import msgpack

from nvflare.fuel.f3.comm_error import CommError
from nvflare.fuel.f3.connection import BytesAlike, Connection, ConnState, FrameReceiver
from nvflare.fuel.f3.drivers.connector_info import ConnectorInfo, Mode
from nvflare.fuel.f3.drivers.driver import ConnMonitor, Driver
from nvflare.fuel.f3.drivers.driver_params import DriverCap, DriverParams
from nvflare.fuel.f3.drivers.net_utils import ssl_required
from nvflare.fuel.f3.endpoint import Endpoint, EndpointMonitor, EndpointState
from nvflare.fuel.f3.message import Message, MessageReceiver
from nvflare.fuel.f3.sfm.constants import HandshakeKeys, Types
from nvflare.fuel.f3.sfm.heartbeat_monitor import HeartbeatMonitor
from nvflare.fuel.f3.sfm.prefix import PREFIX_LEN, Prefix
from nvflare.fuel.f3.sfm.sfm_conn import SfmConnection
from nvflare.fuel.f3.sfm.sfm_endpoint import SfmEndpoint
from nvflare.fuel.f3.stats_pool import StatsPoolManager
from nvflare.fuel.utils.buffer_list import BufferList
from nvflare.security.logging import secure_format_exception, secure_format_traceback

FRAME_THREAD_POOL_SIZE = 100
CONN_THREAD_POOL_SIZE = 16
INIT_WAIT = 1
MAX_WAIT = 10
SILENT_RECONNECT_TIME = 5
SELF_ADDR = "0.0.0.0:0"

log = logging.getLogger(__name__)

handle_lock = threading.Lock()
handle_count = 0


def get_handle():
    pass


class ConnManager(ConnMonitor):
    """SFM connection manager
    The class is responsible for maintaining state of SFM connections and pumping data through them
    """

    def __init__(self, local_endpoint: Endpoint):
        self.local_endpoint = local_endpoint

        # Active connectors
        self.connectors: Dict[str, ConnectorInfo] = {}

        # A dict of SFM connections, key is connection name
        self.sfm_conns: Dict[str, SfmConnection] = {}

        # A dict of SfmEndpoint for finding endpoint by name
        self.sfm_endpoints: Dict[str, SfmEndpoint] = {}

        # A list of Endpoint monitors
        self.monitors: List[EndpointMonitor] = []

        # App/receiver mapping
        self.receivers: Dict[int, MessageReceiver] = {}

        self.started = False
        self.stopped = False
        self.conn_mgr_executor = ThreadPoolExecutor(CONN_THREAD_POOL_SIZE, "conn_mgr")
        self.frame_mgr_executor = ThreadPoolExecutor(FRAME_THREAD_POOL_SIZE, "frame_mgr")
        self.lock = threading.Lock()
        self.null_conn = NullConnection()
        stats = StatsPoolManager.get_pool("sfm_send_frame")
        if not stats:
            stats = StatsPoolManager.add_time_hist_pool(
                "sfm_send_frame", "SFM send_frame time in secs", scope=local_endpoint.name
            )
        self.send_frame_stats = stats
        self.heartbeat_monitor = HeartbeatMonitor(self.sfm_conns)

    def add_connector(self, driver: Driver, params: dict, mode: Mode) -> str:

        # Validate parameters
        pass

    def remove_connector(self, handle: str):
        pass

    def start(self):
        pass

    def stop(self):

        pass

    def find_endpoint(self, name: str) -> Optional[Endpoint]:

        pass

    def remove_endpoint(self, name: str):

        pass

    def get_connections(self, name: str) -> Optional[List[SfmConnection]]:

        pass

    def send_message(self, endpoint: Endpoint, app_id: int, headers: Optional[dict], payload: BytesAlike):
        """Send a message to endpoint for app

        The message is asynchronous, no response is expected.

        Args:
            endpoint: An endpoint to send the message to
            app_id: Application ID
            headers: headers, optional
            payload: message payload, optional

        Raises:
            CommError: If any error happens while sending the data
        """
        pass

    def register_message_receiver(self, app_id: int, receiver: MessageReceiver):
        pass

    def add_endpoint_monitor(self, monitor: EndpointMonitor):
        pass

    # Internal methods

    def start_connector(self, connector: ConnectorInfo):
        """Start connector in a new thread"""
        pass

    @staticmethod
    def start_connector_task(connector: ConnectorInfo):
        """Start connector in a new thread
        This function will loop as long as connector is not stopped
        """
        pass

    def state_change(self, connection: Connection):
        pass

    def process_frame_task(self, sfm_conn: SfmConnection, frame: BytesAlike):

        pass

    def process_frame(self, sfm_conn: SfmConnection, frame: BytesAlike):
        pass

    def update_endpoint(self, sfm_conn: SfmConnection, data: dict):

        pass

    def notify_monitors(self, endpoint: Endpoint):

        pass

    @staticmethod
    def get_dict_payload(prefix, frame):
        pass

    def handle_new_connection(self, connection: Connection):

        pass

    def close_connection(self, connection: Connection):

        pass

    def send_loopback_message(self, endpoint: Endpoint, app_id: int, headers: Optional[dict], payload: BytesAlike):
        """Send message to itself"""
        pass

    def loopback_message_task(self, endpoint: Endpoint, app_id: int, headers: Optional[dict], payload: BytesAlike):

        pass


class SfmFrameReceiver(FrameReceiver):
    def __init__(self, conn_manager: ConnManager, conn: SfmConnection):
        self.conn_manager = conn_manager
        self.conn = conn

    def process_frame(self, frame: BytesAlike):
        pass


class NullConnection(Connection):
    """A mock connection used for loopback messages"""

    def __init__(self):
        connector = ConnectorInfo("Null", None, {}, Mode.ACTIVE, 0, 0, False, threading.Event())
        super().__init__(connector)

    def get_conn_properties(self) -> dict:
        pass

    def close(self):
        pass

    def send_frame(self, frame: BytesAlike):
        pass
