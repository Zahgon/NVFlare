# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
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

import time


class ClientPropKey:
    FQCN = "fqcn"  # Fully Qualified Cell Name: position in Cellnet
    FQSN = "fqsn"  # Fully Qualified Site Name: position in client hierarchy
    IS_LEAF = "is_leaf"  # Whether the client is a leaf node in client hierarchy
    ORG = "org"  # Organization extracted from the client's TLS certificate


class ClientDictKey:
    NAME = "name"
    FQCN = "fqcn"
    FQSN = "fqsn"
    IS_LEAF = "is_leaf"


class Client:
    def __init__(self, name, token) -> None:
        """Init Client.

        Represents a client, and is managed by the client manager.
        The token is an uuid used for authorization.

        Args:
            name: client name
            token: client token
        """
        self.name = name
        self.token = token
        self.last_connect_time = time.time()
        self.props = {ClientPropKey.FQCN: name, ClientPropKey.FQSN: name, ClientPropKey.IS_LEAF: True}

    def set_token(self, token):
        pass

    def get_token(self):
        pass

    def set_prop(self, name, value):
        pass

    def get_prop(self, name, default=None):
        pass

    def set_fqcn(self, value: str):
        pass

    def get_fqcn(self):
        pass

    def set_fqsn(self, value: str):
        pass

    def get_fqsn(self):
        pass

    def set_is_leaf(self, value: bool):
        pass

    def get_is_leaf(self):
        pass

    def to_dict(self) -> dict:
        """Convert the Client object to a dict representation.
        This dict could be used included into a job's metadata.

        Returns: dict that contains essential info of the client.

        Note that the client's token is not included in the result since it is authentication data.

        """
        pass


def from_dict(d: dict) -> Client:
    """Create a Client object from the data in the specified dict.

    Args:
        d: the dict that contains Client data. This dict should be the result of to_dict() of a Client object.

    Returns: a Client object

    """
    pass
