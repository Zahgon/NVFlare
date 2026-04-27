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

import multiprocessing
import os

from nvflare.apis.client import Client
from nvflare.apis.controller_spec import Task
from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.impl.controller import Controller
from nvflare.apis.shareable import Shareable
from nvflare.apis.signal import Signal
from nvflare.apis.workspace import Workspace
from nvflare.fuel.utils.import_utils import optional_import
from nvflare.fuel.utils.network_utils import get_open_ports
from nvflare.security.logging import secure_format_exception, secure_format_traceback

from .constants import XGB_TRAIN_TASK, XGBShareableHeader


class XGBFedController(Controller):
    def __init__(self, train_timeout: int = 300, port: int = None):
        """Federated XGBoost training controller for histogram-base collaboration.

        It starts the XGBoost federated server and kicks off all the XGBoost job on
        each NVFlare client. The configuration is generic for this component and
        no modification is needed for most training jobs.

        Args:
            train_timeout (int, optional): Time to wait for clients to do local training in seconds.
            port (int, optional): the port to open XGBoost FL server

        Raises:
            TypeError: when any of input arguments does not have correct type
            ValueError: when any of input arguments is out of range
        """
        super().__init__()

        if not isinstance(train_timeout, int):
            raise TypeError("train_timeout must be int but got {}".format(type(train_timeout)))

        self._port = port
        self._xgb_fl_server = None
        self._participate_clients = None
        self._rank_map = None
        self._secure = False
        self._train_timeout = train_timeout
        self._server_cert_path = None
        self._server_key_path = None
        self._ca_cert_path = None
        self._started = False

    def _get_certificates(self, fl_ctx: FLContext):
        pass

    def start_controller(self, fl_ctx: FLContext):
        pass

    def stop_controller(self, fl_ctx: FLContext):
        pass

    def process_result_of_unknown_task(
        self, client: Client, task_name, client_task_id, result: Shareable, fl_ctx: FLContext
    ):
        pass

    def control_flow(self, abort_signal: Signal, fl_ctx: FLContext):
        pass
