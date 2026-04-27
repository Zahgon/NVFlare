# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
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
from collections import defaultdict

from nvflare.apis.dxo import DXO, DataKind, from_shareable
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import ReservedKey, ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable, make_reply
from nvflare.app_opt.p2p.executors.base_dist_opt_executor import BaseDistOptExecutor


class SyncAlgorithmExecutor(BaseDistOptExecutor):
    """An executor to implement synchronous peer-to-peer (P2P) algorithms.

    This executor extends the BaseP2PAlgorithmExecutor to support synchronous execution
    of P2P algorithms. It manages the exchange of values with neighboring clients and ensures
    synchronization at each iteration.

    Args:
        sync_timeout (int): The timeout for waiting for values from neighbors. Defaults to 10 seconds.

    Attributes:
        neighbors_values (defaultdict): A dictionary to store values received from neighbors,
            keyed by iteration and neighbor ID.
        sync_waiter (threading.Event): An event to synchronize the exchange of values.
        lock (threading.Lock): A lock to manage concurrent access to shared data structures.
    """

    def __init__(self, sync_timeout: int = 10):
        super().__init__()

        self.neighbors_values = defaultdict(dict)

        self.sync_timeout = sync_timeout
        self.sync_waiter = threading.Event()
        self.lock = threading.Lock()

    def _exchange_values(self, fl_ctx: FLContext, value: any, iteration: int):
        """Exchanges values with neighbors synchronously.

        Sends the local value to all neighbors and waits for their values for the current iteration.
        Utilizes threading events to synchronize the exchange and ensure all values are received
        before proceeding.

        Args:
            fl_ctx (FLContext): Federated learning context.
            value (any): The local value to send to neighbors.
            iteration (int): The current iteration number of the algorithm.

        Raises:
            SystemExit: If the values from all neighbors are not received within the timeout.
        """
        pass

    def _handle_neighbor_value(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        """Handles incoming values from neighbors.

        Processes the received value from a neighbor, stores it, and signals when all neighbor
        values for the current iteration have been received.

        Args:
            topic (str): Topic of the incoming message.
            request (Shareable): The message containing the neighbor's value.
            fl_ctx (FLContext): Federated learning context.

        Returns:
            Shareable: A reply message indicating successful reception.
        """
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass
