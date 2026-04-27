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
import atexit
import copy
import logging
import os
import weakref
from typing import Optional

from nvflare.fuel.f3 import drivers
from nvflare.fuel.f3.comm_config import CommConfigurator
from nvflare.fuel.f3.comm_error import CommError
from nvflare.fuel.f3.drivers.driver import Driver
from nvflare.fuel.f3.drivers.driver_manager import DriverManager
from nvflare.fuel.f3.drivers.driver_params import DriverParams
from nvflare.fuel.f3.drivers.net_utils import parse_url
from nvflare.fuel.f3.endpoint import Endpoint, EndpointMonitor
from nvflare.fuel.f3.message import Message, MessageReceiver
from nvflare.fuel.f3.sfm.conn_manager import ConnManager, Mode

log = logging.getLogger(__name__)
_running_instances = weakref.WeakSet()
driver_mgr = DriverManager()
driver_loaded = False


def load_comm_drivers():
    pass


class Communicator:
    """FCI (Flare Communication Interface) main communication API"""

    def __init__(self, local_endpoint: Endpoint):
        self.local_endpoint = local_endpoint
        self.monitors = []
        self.conn_manager = ConnManager(local_endpoint)
        self.stopped = False

    def start(self):
        """Start the communicator and establishing all the connections

        Raises:
            CommError: If any error encountered while starting up
        """
        pass

    def stop(self):
        """Stop the communicator and shutdown all the connections

        Raises:
            CommError: If any error encountered while shutting down
        """
        pass

    def register_monitor(self, monitor: EndpointMonitor):
        """Register a monitor for endpoint lifecycle changes

        This monitor is notified for any state changes of all the endpoints.
        Multiple monitors can be registered.

        Args:
            monitor: The class that receives the endpoint state change notification

        Raises:
            CommError: If any error happens while sending the request
        """
        pass

    def find_endpoint(self, name: str) -> Optional[Endpoint]:
        """Find endpoint by name

        Args:
            name: Endpoint name

        Returns:
            The endpoint if found. None if not found

        """
        pass

    def remove_endpoint(self, name: str):
        """Remove endpoint and close all the connections associated with it

        Args:
            name: Endpoint name

        """
        pass

    def send(self, endpoint: Endpoint, app_id: int, message: Message):
        """Send a message to endpoint for app_id, no response is expected

        Args:
            endpoint: An endpoint to send the request to
            app_id: Application ID
            message: Message to send

        Raises:
            CommError: If any error happens while sending the data
        """
        pass

    def register_message_receiver(self, app_id: int, receiver: MessageReceiver):
        """Register a receiver to process FCI message for the app

        Args:
            app_id: Application ID
            receiver: The receiver to process the message

        Raises:
            CommError: If duplicate endpoint/app or receiver is of wrong type
        """
        pass

    def add_connector(self, url: str, mode: Mode, secure: bool = False, resources=None) -> (str, dict):
        """Load a connector. The driver is selected based on the URL

        Args:
            url: The url to listen on or connect to, like "https://0:443". Use 0 for empty host
            mode: Active for connecting, Passive for listening
            secure: True if SSL is required.
            resources: extra resources for creating connection

        Returns:
            A tuple of (A handle that can be used to delete connector, connector params)

        Raises:
            CommError: If any errors
        """
        pass

    def start_listener(self, scheme: str, resources: dict) -> (str, str, dict):
        """Add and start a connector in passive mode on an address selected by the driver.

        Args:
            scheme: Connection scheme, e.g. http, https
            resources: User specified resources like host and port ranges

        Returns:
            A tuple with connector handle and connect url, and connection params

        Raises:
            CommError: If any errors like invalid host or port not available
        """
        pass

    def add_connector_advanced(
        self, driver: Driver, mode: Mode, params: dict, secure: bool, start: bool = False
    ) -> str:
        """Add a connector using a specific driver instance.

        Args:
            driver: A transport driver instance
            mode: Active or passive
            params: Driver parameters
            secure: SSL is required if true
            start: Start the connector if true

        Returns:
            A handle that can be used to delete the connector

        Raises:
            CommError: If any errors
        """
        pass

    def remove_connector(self, handle: str):
        """Remove the connector

        Args:
            handle: The connector handle

        Raises:
            CommError: If any errors
        """
        pass


def _exit_func():
    pass


atexit.register(_exit_func)
