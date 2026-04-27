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

from typing import List

# version>= 1.0.3
import private_set_intersection.python as psi


class PSIClient:
    """
    Class to represent the psi Client in a two-party client, server PSI model.
    """

    def __init__(self, items: List[str]):
        """
        Args:
            items: the items provided by the client
        """

        if len(items) == 0:
            raise RuntimeError("Client items cannot be empty")
        self.reveal_intersection = True
        self.psi_client = psi.client.CreateWithNewKey(self.reveal_intersection)
        self.items = items
        self.setup = None

    def get_items_size(self) -> int:
        pass

    def receive_setup(self, setup_msg: str):
        """
        Args:
            setup_msg: serialized setup str
        """
        pass

    def get_request(self, items):
        pass

    def get_intersection(self, server_response_msg: str) -> List[str]:
        """Returns the intersection of client and server items.

        Args: server_response_msg (PsiProtoResponse): The server response serialized string
        Returns:
            The intersection set (List[str]) of client and server items
        """
        pass
