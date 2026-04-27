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

from typing import Dict, List, Optional, Union

from nvflare.apis.client import from_dict
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import FLContextKey, ProcessType, ReservedKey, SiteType
from nvflare.apis.fl_context import FLContext, FLContextManager
from nvflare.apis.job_def import JobMetaKey
from nvflare.apis.shareable import Shareable
from nvflare.apis.streaming import ConsumerFactory, ObjectProducer, StreamableEngine, StreamContext
from nvflare.apis.workspace import Workspace
from nvflare.fuel.f3.cellnet.core_cell import FQCN
from nvflare.fuel.f3.cellnet.defs import ReturnCode as CellReturnCode
from nvflare.fuel.utils.job_utils import build_client_hierarchy
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.private.aux_runner import AuxMsgTarget, AuxRunner
from nvflare.private.event import fire_event
from nvflare.private.fed.utils.fed_utils import create_job_processing_context_properties
from nvflare.private.stream_runner import ObjectStreamer
from nvflare.widgets.fed_event import ClientFedEventRunner
from nvflare.widgets.info_collector import InfoCollector
from nvflare.widgets.widget import Widget, WidgetID

from .client_engine_executor_spec import ClientEngineExecutorSpec, TaskAssignment
from .client_json_config import ClientJsonConfigurator
from .client_runner import ClientRunner
from .fed_client import FederatedClient


class ClientRunInfo(object):
    def __init__(self, job_id):
        """To init the ClientRunInfo.

        Args:
            job_id: job id
        """
        self.job_id = job_id
        self.current_task_name = ""
        self.start_time = None


class ClientRunManager(ClientEngineExecutorSpec, StreamableEngine):
    """ClientRunManager provides the ClientEngine APIs implementation running in the child process (CJ)."""

    def __init__(
        self,
        client_name: str,
        job_id: str,
        workspace: Workspace,
        client: FederatedClient,
        components: Dict[str, FLComponent],
        handlers: Optional[List[FLComponent]] = None,
        conf: ClientJsonConfigurator = None,
    ) -> None:
        """To init the ClientRunManager.

        Args:
            client_name: client name
            job_id: job id
            workspace: workspace
            client: FL client object
            components: available FL components
            handlers: available handlers.
            conf: ClientJsonConfigurator object
        """
        super().__init__()

        self.client = client
        self.handlers = handlers
        self.workspace = workspace
        self.components = components
        self.aux_runner = AuxRunner(self)
        self.object_streamer = ObjectStreamer(self.aux_runner)
        self.add_handler(self.aux_runner)
        self.add_handler(self.object_streamer)
        self.conf = conf
        self.cell = None

        self.all_clients = None
        self.name_to_clients = dict()  # client name => Client

        if not components:
            self.components = {}

        if not handlers:
            self.handlers = []

        # get job meta!
        client_config = client.client_args
        fqsn = client_config.get("fqsn", client.client_name)
        is_leaf = client_config.get("is_leaf", True)

        job_ctx_props = self.create_job_processing_context_properties(workspace, job_id)
        job_ctx_props.update(
            {
                FLContextKey.PROCESS_TYPE: ProcessType.CLIENT_JOB,
                FLContextKey.CLIENT_CONFIG: client_config,
            }
        )

        self.fl_ctx_mgr = FLContextManager(
            engine=self,
            identity_name=client_name,
            job_id=job_id,
            public_stickers={
                ReservedKey.FQSN: fqsn,
                ReservedKey.IS_LEAF: is_leaf,
            },
            private_stickers=job_ctx_props,
        )

        self.run_info = ClientRunInfo(job_id=job_id)

        self.widgets = {WidgetID.INFO_COLLECTOR: InfoCollector(), WidgetID.FED_EVENT_RUNNER: ClientFedEventRunner()}
        for _, widget in self.widgets.items():
            self.handlers.append(widget)

        self.logger = get_obj_logger(self)

    def get_task_assignment(self, fl_ctx: FLContext, timeout=None) -> TaskAssignment:
        pass

    def new_context(self) -> FLContext:
        pass

    def send_task_result(self, result: Shareable, fl_ctx: FLContext, timeout=None) -> bool:
        pass

    def get_workspace(self) -> Workspace:
        pass

    def get_run_info(self) -> ClientRunInfo:
        pass

    def show_errors(self) -> ClientRunInfo:
        pass

    def reset_errors(self) -> ClientRunInfo:
        pass

    def dispatch(self, topic: str, request: Shareable, fl_ctx: FLContext) -> Shareable:
        pass

    def add_component(self, component_id: str, component):
        pass

    def get_component(self, component_id: str) -> object:
        pass

    def get_all_components(self) -> dict:
        pass

    def validate_targets(self, inputs) -> ([], []):
        pass

    def get_client_from_name(self, client_name):
        pass

    def get_clients(self):
        pass

    def persist_components(self, fl_ctx: FLContext, completed: bool):
        pass

    def get_widget(self, widget_id: str) -> Widget:
        pass

    def fire_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def add_handler(self, handler: FLComponent):
        pass

    def build_component(self, config_dict):
        pass

    def get_cell(self):
        pass

    def send_aux_request(
        self,
        targets: Union[None, str, List[str]],
        topic: str,
        request: Shareable,
        timeout: float,
        fl_ctx: FLContext,
        optional=False,
        secure=False,
    ) -> dict:
        pass

    def _get_aux_msg_target(self, name: str):
        pass

    def _to_aux_msg_targets(self, target_names: List[str]):
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

    def get_job_clients(self, fl_ctx: FLContext):
        """Get participating clients of the job.
        We no longer send message to the Server to ask this info.
        Instead, job clients are included in the meta of the job when Server started the job!

        Args:
            fl_ctx: The FLContext object

        Returns:

        """
        pass

    def register_aux_message_handler(self, topic: str, message_handle_func):
        pass

    def fire_and_forget_aux_request(
        self, topic: str, request: Shareable, fl_ctx: FLContext, optional=False, secure=False
    ) -> dict:
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

    def abort_app(self, job_id: str, fl_ctx: FLContext):
        pass

    def create_job_processing_context_properties(self, workspace, job_id):
        pass
