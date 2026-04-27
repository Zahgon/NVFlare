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
from nvflare.apis.fl_constant import CellMessageAuthHeaderKey
from nvflare.fuel.f3.cellnet.cell import Cell
from nvflare.fuel.f3.message import Message
from nvflare.fuel.utils.validation_utils import check_object_type, check_str


def add_authentication_headers(msg: Message, client_name: str, auth_token, token_signature, ssid=None):
    """Add authentication headers to the specified message.

    Args:
        msg: the message that the headers are added to
        client_name: name of the client
        auth_token: authentication token
        token_signature: token signature
        ssid: optional SSID

    Returns:

    """
    pass


def set_add_auth_headers_filters(cell: Cell, client_name: str, auth_token: str, token_signature: str, ssid=None):
    """Set filters for adding auth headers.

    Args:
        cell: the cell to add the filters to.
        client_name: name of the client
        auth_token: authentication token
        token_signature: token signature
        ssid: SSID, optional

    Returns: None

    """
    pass
