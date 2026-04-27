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

import os
import re
import shutil
import sys
import threading
from typing import List

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import FLContextKey, MachineStatus, ProcessType, ReservedKey, SystemComponents
from nvflare.apis.fl_context import FLContext, FLContextManager
from nvflare.apis.shareable import Shareable
from nvflare.apis.streaming import ConsumerFactory, ObjectProducer, StreamableEngine, StreamContext
from nvflare.apis.utils.fl_context_utils import gen_new_peer_ctx
from nvflare.apis.workspace import Workspace
from nvflare.fuel.f3.cellnet.cell import Cell
from nvflare.fuel.f3.cellnet.defs import CellChannel, MessageHeaderKey, ReturnCode
from nvflare.fuel.f3.message import Message as CellMessage
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.private.aux_runner import AuxMsgTarget, AuxRunner
from nvflare.private.defs import ERROR_MSG_PREFIX, ClientStatusKey, new_cell_message
from nvflare.private.event import fire_event
from nvflare.private.fed.server.job_meta_validator import JobMetaValidator
from nvflare.private.fed.utils.app_deployer import AppDeployer
from nvflare.private.fed.utils.fed_utils import security_close
from nvflare.private.stream_runner import ObjectStreamer
from nvflare.security.logging import secure_format_exception, secure_log_traceback
from nvflare.widgets.fed_event import ClientFedEventRunner

from .client_engine_internal_spec import ClientEngineInternalSpec
from .client_executor import JobExecutor
from .client_run_manager import ClientRunInfo
from .client_status import ClientStatus
from .fed_client import FederatedClient


def _remove_custom_path():
    pass


class ClientEngine(ClientEngineInternalSpec, StreamableEngine):
    """ClientEngine runs in the client parent process (CP)."""

    def __init__(self, client: FederatedClient, args, rank, workers=5):
        """To init the ClientEngine.

        Args:
            client: FL client object
            args: command args
            rank: local process rank
            workers: number of workers
        """
        super().__init__()
        self.client = client
        self.client_name = client.client_name
        self.args = args
        self.rank = rank
        self.client_executor = JobExecutor(client, os.path.join(args.workspace, "startup"))
        self.admin_agent = None
        self.aux_runner = AuxRunner(self)
        self.object_streamer = ObjectStreamer(self.aux_runner)
        self.cell = None

        client_config = client.client_args
        fqsn = client_config.get("fqsn", client.client_name)
        is_leaf = client_config.get("is_leaf", True)

        self.fl_ctx_mgr = FLContextManager(
            engine=self,
            identity_name=self.client_name,
            job_id="",
            public_stickers={
                ReservedKey.FQSN: fqsn,
                ReservedKey.IS_LEAF: is_leaf,
            },
            private_stickers={
                SystemComponents.DEFAULT_APP_DEPLOYER: AppDeployer(),
                SystemComponents.JOB_META_VALIDATOR: JobMetaValidator(),
                SystemComponents.FED_CLIENT: client,
                FLContextKey.SECURE_MODE: self.client.secure_train,
                FLContextKey.WORKSPACE_ROOT: args.workspace,
                FLContextKey.PROCESS_TYPE: ProcessType.CLIENT_PARENT,
            },
        )

        self.status = MachineStatus.STOPPED

        if workers < 1:
            raise ValueError("workers must >= 1")
        self.logger = get_obj_logger(self)
        self.fl_components = [x for x in self.client.components.values() if isinstance(x, FLComponent)]

        self.fl_components.append(ClientFedEventRunner())

    def fire_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def get_cell(self):
        """Get the communication cell.
        This method must be implemented since AuxRunner calls to get cell.

        Returns:

        """
        pass

    def initialize_comm(self, cell: Cell):
        """This is called when communication cell has been created.
        We will set up aux message handler here.

        Args:
            cell:

        Returns:

        """
        pass

    def _handle_aux_message(self, request: CellMessage) -> CellMessage:
        pass

    def register_aux_message_handler(self, topic: str, message_handle_func):
        """Register aux message handling function with specified topics.

        Exception is raised when:
            a handler is already registered for the topic;
            bad topic - must be a non-empty string
            bad message_handle_func - must be callable

        Implementation Note:
            This method should simply call the ServerAuxRunner's register_aux_message_handler method.

        Args:
            topic: the topic to be handled by the func
            message_handle_func: the func to handle the message. Must follow aux_message_handle_func_signature.

        """
        pass

    def send_aux_request(
        self,
        topic: str,
        request: Shareable,
        timeout: float,
        fl_ctx: FLContext,
        optional=False,
        secure=False,
    ) -> Shareable:
        """Send a request to the Server via the aux channel.

        Implementation: simply calls the AuxRunner's send_aux_request method.

        Args:
            topic: topic of the request.
            request: request to be sent
            timeout: number of secs to wait for replies. 0 means fire-and-forget.
            fl_ctx: FL context
            optional: whether this message is optional
            secure: send the aux request in a secure way

        Returns: a dict of replies (client name => reply Shareable)

        """
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
        """Send a stream of Shareable objects to receivers.

        Args:
            channel: the channel for this stream
            topic: topic of the stream
            stream_ctx: context of the stream
            targets: receiving sites
            producer: the ObjectProducer that can produces the stream of Shareable objects
            fl_ctx: the FLContext object
            optional: whether the stream is optional
            secure: whether to use P2P security

        Returns: result from the generator's reply processing

        """
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
        """Register a ConsumerFactory for specified app channel and topic.
        Once a new streaming request is received for the channel/topic, the registered factory will be used
        to create an ObjectConsumer object to handle the new stream.

        Note: the factory should generate a new ObjectConsumer every time get_consumer() is called. This is because
        multiple streaming sessions could be going on at the same time. Each streaming session should have its
        own ObjectConsumer.

        Args:
            channel: app channel
            topic: app topic
            factory: the factory to be registered
            stream_done_cb: the callback to be called when streaming is done on receiving side
            consumed_cb: the CB to be called after a chunk is consumed

        Returns: None

        """
        pass

    def shutdown_streamer(self):
        pass

    def set_agent(self, admin_agent):
        pass

    def new_context(self) -> FLContext:
        pass

    def add_component(self, component_id: str, component):
        pass

    def get_component(self, component_id: str) -> object:
        pass

    def get_engine_status(self):
        pass

    def start_app(
        self,
        job_id: str,
        job_meta: dict,
        allocated_resource: dict = None,
        token: str = None,
        resource_manager=None,
    ) -> str:
        pass

    def notify_job_status(self, job_id: str, job_status):
        pass

    def get_client_name(self):
        pass

    def abort_app(self, job_id: str) -> str:
        pass

    def send_to_job(
        self,
        job_id,
        channel: str,
        topic: str,
        msg: CellMessage,
        timeout: float,
        optional=False,
    ) -> CellMessage:
        """Send a message to CJ

        Args:
            job_id: id of the job
            channel: message channel
            topic: message topic
            msg: the message to be sent
            timeout: how long to wait for reply
            optional: whether the message is optional

        Returns: reply from CJ

        """
        pass

    def abort_task(self, job_id: str) -> str:
        pass

    def shutdown(self) -> str:
        pass

    def restart(self) -> str:
        pass

    def deploy_app(self, app_name: str, job_id: str, job_meta: dict, client_name: str, app_data) -> str:
        pass

    def delete_run(self, job_id: str) -> str:
        pass

    def get_current_run_info(self, job_id) -> ClientRunInfo:
        pass

    def get_errors(self, job_id):
        pass

    def configure_job_log(self, job_id, config):
        pass

    def reset_errors(self, job_id):
        pass

    def get_all_job_ids(self):
        pass

    def fire_and_forget_aux_request(
        self, topic: str, request: Shareable, fl_ctx: FLContext, optional=False, secure=False
    ) -> dict:
        pass


def shutdown_client(federated_client, touch_file):
    pass
