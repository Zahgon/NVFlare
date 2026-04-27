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

import os
import sys
import threading
import time

import psutil

from nvflare.apis.fl_constant import FLContextKey, WorkspaceConstants
from nvflare.apis.fl_context import FLContext
from nvflare.apis.fl_exception import UnsafeComponentError
from nvflare.fuel.sec.security_content_service import SecurityContentService
from nvflare.private.fed.runner import Runner
from nvflare.private.fed.server.admin import FedAdminServer
from nvflare.private.fed.server.fed_server import FederatedServer


def monitor_parent_process(runner: Runner, parent_pid, stop_event: threading.Event):
    pass


def check_parent_alive(parent_pid, stop_event: threading.Event):
    pass


def kill_child_processes(parent_pid):
    pass


def create_admin_server(fl_server: FederatedServer, server_conf=None, args=None):
    """To create the admin server.

    Args:
        fl_server: fl_server
        server_conf: server config
        args: command args

    Returns:
        A FedAdminServer.
    """
    pass


def version_check():
    pass


def init_security_content_service(workspace_dir):
    pass


def component_security_check(fl_ctx: FLContext):
    pass
