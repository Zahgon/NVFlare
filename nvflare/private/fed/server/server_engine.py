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

import copy
import os
import re
import shutil
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from typing import Dict, List, Optional, Tuple

from nvflare.apis.client import Client
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import (
    AdminCommandNames,
    ConnPropKey,
    FLContextKey,
    MachineStatus,
    RunProcessKey,
    ServerCommandKey,
    ServerCommandNames,
    SiteType,
    SnapshotKey,
    WorkspaceConstants,
)
from nvflare.apis.fl_context import FLContext
from nvflare.apis.fl_snapshot import RunSnapshot
from nvflare.apis.impl.job_def_manager import JobDefManagerSpec
from nvflare.apis.job_def import Job
from nvflare.apis.job_launcher_spec import JobLauncherSpec, JobProcessArgs
from nvflare.apis.shareable import ReturnCode, Shareable, make_reply
from nvflare.apis.streaming import ConsumerFactory, ObjectProducer, StreamableEngine, StreamContext
from nvflare.apis.utils.fl_context_utils import gen_new_peer_ctx, get_serializable_data
from nvflare.apis.workspace import Workspace
from nvflare.fuel.f3.cellnet.cell import Cell
from nvflare.fuel.f3.cellnet.defs import MessageHeaderKey
from nvflare.fuel.f3.cellnet.defs import ReturnCode as CellMsgReturnCode
from nvflare.fuel.f3.cellnet.fqcn import FQCN
from nvflare.fuel.f3.message import Message as CellMessage
from nvflare.fuel.utils.argument_utils import parse_vars
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.fuel.utils.zip_utils import zip_directory_to_bytes
from nvflare.private.admin_defs import Message, MsgHeader
from nvflare.private.aux_runner import AuxMsgTarget
from nvflare.private.defs import (
    AUTH_CLIENT_NAME_FOR_SJ,
    CellChannel,
    CellMessageHeaderKeys,
    RequestHeader,
    TrainingTopic,
    new_cell_message,
)
from nvflare.private.fed.server.server_json_config import ServerJsonConfigurator
from nvflare.private.fed.utils.fed_utils import (
    get_job_launcher,
    get_return_code,
    security_close,
    set_message_security_data,
)
from nvflare.private.scheduler_constants import ShareableHeader
from nvflare.security.logging import secure_format_exception
from nvflare.widgets.info_collector import InfoCollector
from nvflare.widgets.widget import Widget, WidgetID

from .client_manager import ClientManager
from .job_runner import JobRunner
from .message_send import ClientReply
from .run_info import RunInfo
from .run_manager import RunManager
from .server_commands import ServerCommands
from .server_engine_internal_spec import EngineInfo, ServerEngineInternalSpec
from .server_status import ServerStatus


class ServerEngine(ServerEngineInternalSpec, StreamableEngine):
    def __init__(self, server, args, client_manager: ClientManager, snapshot_persistor, workers=3):
        """Server engine.

        Args:
            server: server
            args: arguments
            client_manager (ClientManager): client manager.
            workers: number of worker threads.
        """
        # TODO:: clean up the server function / requirement here should be BaseServer
        self.server = server
        self.args = args
        self.run_processes = {}
        self.exception_run_processes = {}
        self.run_manager = None
        self.conf = None
        self.cell = None
        self.client_manager = client_manager

        self.widgets = {
            WidgetID.INFO_COLLECTOR: InfoCollector(),
            # WidgetID.FED_EVENT_RUNNER: ServerFedEventRunner()
        }

        self.engine_info = EngineInfo()

        if not workers >= 1:
            raise ValueError("workers must >= 1 but got {}".format(workers))

        self.executor = ThreadPoolExecutor(max_workers=workers)
        self.lock = Lock()
        self.logger = get_obj_logger(self)

        self.asked_to_stop = False
        self.snapshot_persistor = snapshot_persistor
        self.job_runner = None
        self.job_def_manager = None

        self.kv_list = parse_vars(args.set)

    def has_relays(self):
        pass

    def _get_run_folder(self, job_id):
        pass

    def get_engine_info(self) -> EngineInfo:
        pass

    def get_run_info(self) -> Optional[RunInfo]:
        pass

    def delete_job_id(self, num):
        pass

    def get_clients(self) -> [Client]:
        pass

    def validate_targets(self, client_names: List[str]) -> Tuple[List[Client], List[str]]:
        pass

    def start_app_on_server(self, fl_ctx: FLContext, job: Job = None, job_clients=None, snapshot=None) -> str:
        pass

    def remove_exception_process(self, job_id):
        pass

    def wait_for_complete(self, workspace, job_id, process):
        pass

    def _start_runner_process(self, job, job_clients, snapshot, fl_ctx: FLContext):
        pass

    def get_job_clients(self, client_sites):
        pass

    def remove_custom_path(self):
        pass

    def abort_app_on_clients(self, clients: List[str]) -> str:
        pass

    def abort_app_on_server(self, job_id: str, turn_to_cold: bool = False) -> str:

        pass

    def _remove_run_processes(self, job_id):
        # wait for the run process to gracefully terminated, and ensure to remove from run_processes.
        pass

    def check_app_start_readiness(self, job_id: str) -> str:
        pass

    def shutdown_server(self) -> str:
        pass

    def restart_server(self) -> str:
        pass

    def get_widget(self, widget_id: str) -> Widget:
        pass

    def get_client_name_from_token(self, token: str) -> str:
        pass

    def get_client_from_name(self, client_name):
        pass

    def get_app_data(self, app_name: str) -> Tuple[str, object]:
        pass

    def get_app_run_info(self, job_id) -> Optional[RunInfo]:
        pass

    def send_app_command(self, job_id: str, topic: str, cmd_data, timeout: float) -> Shareable:
        pass

    def set_run_manager(self, run_manager: RunManager):
        pass

    def get_cell(self):
        pass

    def initialize_comm(self, cell: Cell):
        """This is called when the communication cell has been created.
        We will set up aux message handler here.

        Args:
            cell:

        Returns:

        """
        pass

    def _handle_aux_message(self, request: CellMessage) -> CellMessage:
        pass

    def set_job_runner(self, job_runner: JobRunner, job_manager: JobDefManagerSpec):
        pass

    def set_configurator(self, conf: ServerJsonConfigurator):
        pass

    def build_component(self, config_dict):
        pass

    def new_context(self) -> FLContext:
        pass

    def add_component(self, component_id: str, component):
        pass

    def get_component(self, component_id: str) -> object:
        pass

    def fire_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def get_staging_path_of_app(self, app_name: str) -> str:
        pass

    def deploy_app_to_server(self, run_destination: str, app_name: str, app_staging_path: str) -> str:
        pass

    def get_workspace(self) -> Workspace:
        pass

    def ask_to_stop(self):
        pass

    def deploy_app(self, job_id, src, dst):
        pass

    def remove_clients(self, clients: List[str]) -> str:
        pass

    def _remove_dead_client(self, token):
        pass

    def register_aux_message_handler(self, topic: str, message_handle_func):
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

    def _get_aux_msg_target(self, name: str):
        pass

    def _to_aux_msg_targets(self, target_names: List[str]):
        pass

    def send_aux_to_targets(self, targets, topic, request, timeout, fl_ctx, optional, secure):
        pass

    def stream_objects(
        self,
        channel: str,
        topic: str,
        stream_ctx: StreamContext,
        targets: List[str],
        producer: ObjectProducer,
        fl_ctx: FLContext,
        optional=False,
        secure=False,
    ):
        pass

    def register_stream_processing(
        self,
        channel: str,
        topic: str,
        factory: ConsumerFactory,
        stream_done_cb=None,
        consumed_cb=None,
        **cb_kwargs,
    ):
        pass

    def shutdown_streamer(self):
        pass

    def sync_clients_from_main_process(self):
        # repeatedly ask the parent process to get participating clients until we receive the result
        # or timed out after 30 secs (already tried 30 times).
        pass

    def get_participating_clients(self):
        # called from server's job cell
        pass

    def _retrieve_clients_data(self, job_id):
        pass

    def update_job_run_status(self):
        pass

    def notify_dead_job(self, job_id: str, client_name: str, reason: str):
        pass

    def send_command_to_child_runner_process(
        self, job_id: str, command_name: str, command_data, timeout=5.0, optional=False
    ):
        pass

    def persist_components(self, fl_ctx: FLContext, completed: bool):
        pass

    def restore_components(self, snapshot: RunSnapshot, fl_ctx: FLContext):
        pass

    def dispatch(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def show_stats(self, job_id) -> dict:
        pass

    def get_errors(self, job_id) -> dict:
        pass

    def reset_errors(self, job_id) -> str:
        pass

    def configure_job_log(self, job_id, data) -> str:
        pass

    def _send_admin_requests(self, requests, fl_ctx: FLContext, timeout_secs=10) -> List[ClientReply]:
        pass

    def check_client_resources(self, job: Job, resource_reqs, fl_ctx: FLContext) -> Dict[str, Tuple[bool, str]]:
        pass

    def _make_message_for_check_resource(self, job, resource_requirements, fl_ctx):
        pass

    def cancel_client_resources(
        self, resource_check_results: Dict[str, Tuple[bool, str]], resource_reqs: Dict[str, dict], fl_ctx: FLContext
    ):
        pass

    def start_client_job(self, job, client_sites, fl_ctx: FLContext):
        pass

    def register_app_command(self, topic: str, cmd_func, *args, **kwargs):
        pass

    def stop_all_jobs(self):
        pass

    def pause_server_jobs(self):
        pass

    def close(self):
        pass


def server_shutdown(server, touch_file):
    pass
        # sys.exit(2)
