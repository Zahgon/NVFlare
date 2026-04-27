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
import threading
from abc import ABC
from typing import Dict, Optional

from nvflare.fuel.f3.comm_error import CommError
from nvflare.fuel.f3.connection import Connection, ConnState
from nvflare.fuel.f3.drivers.driver import ConnectorInfo, Driver

log = logging.getLogger(__name__)


class BaseDriver(Driver, ABC):
    """Common base class for all drivers
    It contains all the common connection management code
    """

    def __init__(self):
        super().__init__()
        self.connections: Dict[str, Connection] = {}
        self.connector: Optional[ConnectorInfo] = None
        self.conn_lock = threading.Lock()

    def add_connection(self, conn: Connection):
        pass

    def close_connection(self, conn: Connection):
        pass

    def close_all(self):
        pass

    def _notify_monitor(self, conn: Connection):
        pass
