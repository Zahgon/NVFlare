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
import time

from nvflare.apis.fl_constant import ConfigVarName, FLContextKey, SystemConfigs
from nvflare.apis.fl_context import FLContext
from nvflare.apis.workspace import Workspace
from nvflare.fuel.f3.cellnet.cell import ReturnCode as CellReturnCode
from nvflare.fuel.f3.cellnet.defs import MessageHeaderKey
from nvflare.fuel.f3.cellnet.fqcn import FQCN
from nvflare.fuel.f3.message import Message as CellMessage
from nvflare.fuel.utils.config_service import ConfigService
from nvflare.fuel.utils.log_utils import get_module_logger
from nvflare.private.admin_defs import Message
from nvflare.private.defs import CellChannel, RequestHeader, TrainingTopic, new_cell_message
from nvflare.private.fed.app.fl_conf import create_privacy_manager
from nvflare.private.fed.client.client_json_config import ClientJsonConfigurator
from nvflare.private.fed.client.client_run_manager import ClientRunManager
from nvflare.private.fed.client.client_runner import ClientRunner
from nvflare.private.fed.client.client_status import ClientStatus
from nvflare.private.fed.client.command_agent import CommandAgent
from nvflare.private.fed.runner import Runner
from nvflare.private.fed.utils.fed_utils import authorize_build_component
from nvflare.private.privacy_manager import PrivacyService


class ClientAppRunner(Runner):

    logger = get_module_logger(__module__, __qualname__)

    def __init__(self, time_out=60.0) -> None:
        super().__init__()
        self.command_agent = None
        self.timeout = time_out
        self.client_runner = None

    def start_run(self, app_root, args, config_folder, federated_client, secure_train, sp, event_handlers):
        pass

    @staticmethod
    def _set_fl_context(fl_ctx: FLContext, app_root, args, workspace, secure_train):
        pass

    def create_client_runner(self, app_root, args, config_folder, federated_client, secure_train, event_handlers=None):
        pass

    def create_run_manager(self, args, conf, federated_client, workspace):
        pass

    def start_command_agent(self, args, federated_client, fl_ctx):
        # Start the command agent
        pass

    def sync_up_parents_process(self, federated_client):
        pass

    def notify_job_status(self, federated_client, job_id, status, timeout=5.0, retry_timeout=None):
        """Notify the CP the job status. This is called from CJ.

        Args:
            federated_client: the fed client object.
            job_id: job ID
            status: status of the job.
            timeout: timeout of the notification message
            retry_timeout: max amount of time for retry

        Returns: None

        When the CJ is just started (status=2), it tries to notify the CP. Since this is the very first message from
        CJ to SP, the connection to CP may not have been established. We'll retry until the notification is sent
        successfully, or the retry_timeout has been reached.

        """
        pass

    def close(self):
        pass

    def stop(self):
        pass
