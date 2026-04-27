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

import os

from nvflare.apis.fl_constant import FLContextKey, MachineStatus
from nvflare.apis.fl_context import FLContext
from nvflare.apis.workspace import Workspace
from nvflare.private.fed.app.fl_conf import create_privacy_manager
from nvflare.private.fed.runner import Runner
from nvflare.private.fed.server.server_engine import ServerEngine
from nvflare.private.fed.server.server_json_config import ServerJsonConfigurator
from nvflare.private.fed.server.server_status import ServerStatus
from nvflare.private.fed.utils.fed_utils import authorize_build_component
from nvflare.private.privacy_manager import PrivacyService
from nvflare.security.logging import secure_format_exception


def _set_up_run_config(workspace: Workspace, server, conf):
    pass


class ServerAppRunner(Runner):
    def __init__(self, server) -> None:
        super().__init__()
        self.server = server

    def start_server_app(
        self, workspace: Workspace, args, app_root, job_id, snapshot, logger, kv_list=None, event_handlers=None
    ):
        pass

    def sync_up_parents_process(self, args):
        pass

    def update_job_run_status(self):
        pass

    def stop(self):
        pass
