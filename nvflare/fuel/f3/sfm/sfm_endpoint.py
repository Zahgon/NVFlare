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
from typing import List, Optional

from nvflare.fuel.f3.endpoint import Endpoint
from nvflare.fuel.f3.sfm.sfm_conn import SfmConnection

# Hard-coded stream ID to be used by packets before handshake
RESERVED_STREAM_ID = 16
MAX_CONN_PER_ENDPOINT = 1

log = logging.getLogger(__name__)


class SfmEndpoint:
    """An endpoint wrapper to keep SFM internal data"""

    def __init__(self, endpoint: Endpoint):
        self.endpoint = endpoint
        self.stream_id: int = RESERVED_STREAM_ID
        self.lock = threading.Lock()
        self.connections: List[SfmConnection] = []

    def add_connection(self, sfm_conn: SfmConnection):

        pass

    def remove_connection(self, sfm_conn: SfmConnection):

        pass

    def get_connection(self, stream_id: int) -> Optional[SfmConnection]:
        pass

    def next_stream_id(self) -> int:
        """Get next stream_id for the endpoint
        stream_id is used to assemble fragmented data
        """
        pass
