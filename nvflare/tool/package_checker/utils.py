# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
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

import json
import os
import shlex
import shutil
import socket
import ssl
import subprocess
import tempfile

import grpc
from requests import Response


class NVFlareConfig:
    SERVER = "fed_server.json"
    CLIENT = "fed_client.json"
    ADMIN = "fed_admin.json"


class NVFlareRole:
    SERVER = "server"
    CLIENT = "client"
    ADMIN = "admin"


def try_write_dir(path: str):
    pass


def try_bind_address(host: str, port: int):
    """Tries to bind to address."""
    pass


def parse_overseer_agent_args(overseer_agent_conf: dict, required_args: list) -> dict:
    pass


def construct_dummy_overseer_response(overseer_agent_conf: dict, role: str) -> Response:
    pass


def get_required_args_for_overseer_agent(overseer_agent_class: str, role: str) -> list:
    """Gets required argument list for a specific overseer agent class."""
    pass


def _prepare_data(args: dict):
    pass


def _get_ca_cert_file_name():
    pass


def _get_cert_file_name(role: str):
    pass


def _get_prv_key_file_name(role: str):
    pass


def split_by_len(item, max_len):
    pass


def _get_conn_sec(startup: str):
    # get connection security
    # first try to see whether this is a client config.
    pass


def check_grpc_server_running(startup: str, host: str, port: int, token=None) -> bool:

    pass


def check_socket_server_running(startup: str, host: str, port: int, scheme: str = "https") -> bool:
    """Check if socket-based server (HTTP/HTTPS/TCP/STCP) is running and accessible.

    This function performs a socket connection test with optional SSL/TLS.
    It's used for HTTP/WebSocket and TCP-based FL servers.

    Args:
        startup: Path to startup directory containing certificates
        host: Server hostname or IP address
        port: Server port number
        scheme: URL scheme ("http", "https", "tcp", "stcp")

    Returns:
        True if server is accessible, False otherwise
    """
    pass


def run_command_in_subprocess(command):
    pass


def get_communication_scheme(package_path: str, config_name: str, default_scheme: str = "http") -> str:
    """Read the communication scheme from package configuration files.

    This function checks multiple sources to determine the communication scheme:
    1. For servers: fed_server.json (service.scheme)
    2. For all packages: comm_config.json in local/ or startup/ directories

    Args:
        package_path: Path to the package directory
        config_name: Name of the configuration file (fed_server.json, fed_client.json, fed_admin.json)
        default_scheme: Default scheme to return if no scheme is found

    Returns:
        The communication scheme (e.g., "grpc", "http")
    """
    pass
