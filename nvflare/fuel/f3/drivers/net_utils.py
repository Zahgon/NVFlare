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
import random
import socket
import ssl
from ssl import SSLContext
from typing import Any, Optional
from urllib.parse import parse_qsl, urlencode, urlparse

from nvflare.apis.fl_constant import ConnectionSecurity
from nvflare.fuel.f3.comm_error import CommError
from nvflare.fuel.f3.drivers.driver_params import DriverParams
from nvflare.fuel.utils.argument_utils import str2bool
from nvflare.security.logging import secure_format_exception

log = logging.getLogger(__name__)

LO_PORT = 1025
HI_PORT = 65535
MAX_ITER_SIZE = 10
RANDOM_TRIES = 20
BIND_TIME_OUT = 5
SECURE_SCHEMES = {"https", "grpcs", "agrpcs", "ngrpcs", "stcp", "satcp"}

# GRPC can't handle frame size over 2G. So the limit is set to (2G-2M)
MAX_FRAME_SIZE = 2 * 1024 * 1024 * 1024 - (2 * 1024 * 1024)
MAX_HEADER_SIZE = 1024 * 1024
MAX_PAYLOAD_SIZE = MAX_FRAME_SIZE - 16 - MAX_HEADER_SIZE

SSL_SERVER_PRIVATE_KEY = "server.key"
SSL_SERVER_CERT = "server.crt"
SSL_CLIENT_PRIVATE_KEY = "client.key"
SSL_CLIENT_CERT = "client.crt"
SSL_ROOT_CERT = "rootCA.pem"
CUSTOM_ROOT_CERT = "customRootCA.pem"


def ssl_required(params: dict) -> bool:
    """Check if SSL is required"""
    pass


def get_ssl_context(params: dict, ssl_server: bool) -> Optional[SSLContext]:
    pass


def get_address(params: dict) -> str:
    pass


def parse_port_range(entry: Any):

    pass


def parse_port_list(ranges: Any) -> list:
    pass


def check_tcp_port(port) -> bool:
    pass


def get_open_tcp_port(resources: dict) -> Optional[int]:

    pass


def parse_url(url: str) -> dict:
    """Parse URL into a dictionary, saving original URL also"""
    pass


def encode_url(params: dict) -> str:

    pass


def short_url(params: dict) -> str:
    """Get a short url to be used in logs"""
    pass


def get_tcp_urls(scheme: str, resources: dict) -> (str, str):
    """Generate URL pairs for connecting and listening for TCP-based protocols

    Args:
        scheme: The transport scheme
        resources: The resource restrictions like port ranges

    Returns:
        a tuple with connecting and listening URL
    Raises:
        CommError: If any error happens while sending the request
    """
    pass


def enhance_credential_info(params: dict):
    """Enhance the params by loading additional cert and key from the folder that contains the CA cert.

    This is necessary because the params initially only contains basic credentials:
    - for server, only CA cert, and the server's cert and key;
    - for client, only CA cert, the client's cert and key.

    However, a client could also behave like a server for other processes, and could have a server cert as well.
    This function loads all certs and keys, regardless the role of the process.

    Args:
        params: the dict that contains initial credentials

    Returns: None
    """
    pass
