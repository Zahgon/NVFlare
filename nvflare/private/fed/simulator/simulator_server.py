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
from typing import Dict, List, Optional

from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import FLContextKey, ReservedKey, ReservedTopic, ServerCommandKey, SiteType
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReturnCode, Shareable, make_reply
from nvflare.apis.workspace import Workspace
from nvflare.fuel.f3.message import Message
from nvflare.private.fed.server.run_manager import RunManager
from nvflare.private.fed.server.server_state import HotState

from ..server.fed_server import FederatedServer
from ..server.server_engine import ServerEngine
from ..utils.identity_utils import IdentityAsserter


class SimulatorServerEngine(ServerEngine):
    def persist_components(self, fl_ctx: FLContext, completed: bool):
        pass

    def sync_clients_from_main_process(self):
        pass

    def update_job_run_status(self):
        pass

    def fire_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def send_aux_request(
        self,
        targets: [],
        topic: str,
        request: Shareable,
        timeout: float,
        fl_ctx: FLContext,
        optional=False,
        secure=False,
    ) -> dict:
        pass

    def multicast_aux_requests(
        self,
        topic: str,
        target_requests: Dict[str, Shareable],
        timeout: float,
        fl_ctx: FLContext,
        optional: bool = False,
        secure: bool = False,
    ) -> dict:
        pass


class SimulatorRunManager(RunManager):
    def create_job_processing_context_properties(self, workspace, job_id):
        pass


class SimulatorIdentityAsserter(IdentityAsserter):
    def __init__(self, private_key_file: str, cert_file: str):
        self.private_key_file = private_key_file
        self.cert_file = cert_file

    def sign_common_name(self, nonce: str) -> str:
        pass

    def sign(self, content, return_str: bool) -> str:
        pass

    def verify_signature(self, content, signature) -> bool:
        pass


class SimulatorServer(FederatedServer):
    def __init__(
        self,
        project_name=None,
        min_num_clients=2,
        max_num_clients=10,
        cmd_modules=None,
        heart_beat_timeout=600,
        handlers: Optional[List[FLComponent]] = None,
        args=None,
        secure_train=False,
        enable_byoc=False,
        snapshot_persistor=None,
        overseer_agent=None,
    ):
        super().__init__(
            project_name,
            min_num_clients,
            max_num_clients,
            cmd_modules,
            heart_beat_timeout,
            handlers,
            args,
            secure_train,
            # enable_byoc,
            snapshot_persistor,
            overseer_agent,
        )

        self.job_cell = None
        self.server_state = HotState()

    def _process_task_request(self, client, fl_ctx, shared_fl_ctx: FLContext):
        pass

    def _submit_update(self, data, shared_fl_context):
        pass

    def _aux_communicate(self, fl_ctx, shareable, shared_fl_context, topic):
        pass

    def _create_server_engine(self, args, snapshot_persistor):
        pass

    def _get_id_asserter(self):
        pass

    def deploy(self, args, grpc_args=None, secure_train=False):
        pass

    def stop_training(self):
        pass

    def create_run_manager(self, workspace, job_id):
        pass

    def stop_run_engine_cell(self):
        pass
        # self.job_cell.stop()
        # super().stop_run_engine_cell()

    def authentication_check(self, request: Message, state_check):
        pass

    def client_cleanup(self):
        pass
