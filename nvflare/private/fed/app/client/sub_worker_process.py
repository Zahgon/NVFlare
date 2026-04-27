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

"""Sub_worker process to start the multi-processes client."""

import argparse
import copy
import os
import threading
import time

from nvflare.apis.event_type import EventType
from nvflare.apis.executor import Executor
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.signal import Signal
from nvflare.apis.utils.fl_context_utils import get_serializable_data
from nvflare.apis.workspace import Workspace
from nvflare.app_common.executors.multi_process_executor import WorkerComponentBuilder
from nvflare.fuel.common.multi_process_executor_constants import (
    CommunicateData,
    CommunicationMetaData,
    MultiProcessCommandNames,
)
from nvflare.fuel.f3.cellnet.cell import Cell
from nvflare.fuel.f3.cellnet.core_cell import Message as CellMessage
from nvflare.fuel.f3.cellnet.core_cell import MessageHeaderKey, make_reply
from nvflare.fuel.f3.cellnet.defs import ReturnCode
from nvflare.fuel.f3.cellnet.fqcn import FQCN
from nvflare.fuel.f3.cellnet.net_agent import NetAgent
from nvflare.fuel.f3.mpm import MainProcessMonitor as mpm
from nvflare.fuel.sec.audit import AuditService
from nvflare.fuel.sec.security_content_service import SecurityContentService
from nvflare.fuel.utils.log_utils import configure_logging, get_obj_logger, get_script_logger
from nvflare.private.defs import CellChannel, CellChannelTopic, new_cell_message
from nvflare.private.fed.app.fl_conf import create_privacy_manager
from nvflare.private.fed.app.utils import monitor_parent_process
from nvflare.private.fed.client.client_run_manager import ClientRunManager
from nvflare.private.fed.runner import Runner
from nvflare.private.fed.simulator.simulator_app_runner import SimulatorClientRunManager
from nvflare.private.fed.utils.fed_utils import (
    create_stats_pool_files_for_job,
    fobs_initialize,
    register_ext_decomposers,
    set_stats_pool_config_for_job,
)
from nvflare.private.privacy_manager import PrivacyService


class EventRelayer(FLComponent):
    """To relay the event from the worker_process."""

    def __init__(self, cell, parent_fqcn, local_rank):
        """To init the EventRelayer.

        Args:
            cell: the local cell.
            parent_fqcn: FQCN of the parent cell
            local_rank: process local rank
        """
        super().__init__()
        self.cell = cell
        self.parent_fqcn = parent_fqcn
        self.local_rank = local_rank

        self.event_lock = threading.Lock()
        self.start_run_fired = False

    def relay_event(self, run_manager, data):
        """To relay the event.

        Args:
            run_manager: Client_Run_Manager
            data: event data

        """
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        """To handle the event.

        Args:
            event_type: event_type
            fl_ctx: FLContext

        """
        pass


class SubWorkerExecutor(Runner):
    def __init__(self, args, workspace, num_of_processes, local_rank) -> None:
        super().__init__()

        self.args = args
        self.workspace = workspace
        self.components = {}
        self.handlers = []
        self.executor = None
        self.run_manager = None
        self.num_of_processes = num_of_processes
        self.local_rank = local_rank

        self.done = False

        fqcn = FQCN.join([args.client_name, args.job_id, str(local_rank)])
        credentials = {}
        self.cell = Cell(
            fqcn=fqcn,
            root_url=args.root_url,
            secure=False,
            credentials=credentials,
            create_internal_listener=True,
            parent_url=args.parent_url,
        )
        self.cell.start()
        net_agent = NetAgent(self.cell)
        self.cell.register_request_cb(
            channel=CellChannel.CLIENT_SUB_WORKER_COMMAND,
            topic="*",
            cb=self.execute_command,
        )
        mpm.add_cleanup_cb(net_agent.close)
        mpm.add_cleanup_cb(self.cell.stop)

        self.commands = {
            MultiProcessCommandNames.INITIALIZE: self._initialize,
            MultiProcessCommandNames.TASK_EXECUTION: self._execute_task,
            MultiProcessCommandNames.FIRE_EVENT: self._handle_event,
            MultiProcessCommandNames.CLOSE: self._close,
        }

        self.logger = get_obj_logger(self)

    def execute_command(self, request: CellMessage) -> CellMessage:
        pass

    def _initialize(self, data):
        pass

    def _get_client_run_manager(self, job_id):
        pass

    def _execute_task(self, data):
        """To execute the event task and pass to worker_process.

        Args:

        """
        pass

    def _handle_event(self, data):
        """To handle the event.

        Args:

        """
        pass

    def _close(self, data):
        pass

    def run(self):
        pass

    def stop(self):
        pass


def main(args):
    pass


def parse_arguments():
    """Sub_worker process program."""
    pass


if __name__ == "__main__":
    """
    This is the program for running rank processes in multi-process mode.
    """
    # main()
    args = parse_arguments()
    run_dir = os.path.join(args.workspace, args.job_id)
    mpm.run(main_func=main, run_dir=run_dir, args=args)
