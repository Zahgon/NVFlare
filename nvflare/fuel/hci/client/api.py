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

from __future__ import annotations

import os
import shutil
import sys
import threading
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import nvflare.fuel.f3.streaming.file_downloader as downloader
from nvflare.apis.fl_constant import ConnectionSecurity, FLContextKey, ProcessType, ReservedKey, ReturnCode
from nvflare.apis.fl_context import FLContext, FLContextManager
from nvflare.apis.job_def import DEFAULT_STUDY
from nvflare.apis.shareable import Shareable
from nvflare.apis.signal import Signal
from nvflare.apis.streaming import ConsumerFactory, ObjectProducer, StreamableEngine, StreamContext
from nvflare.apis.utils.decomposers import flare_decomposers
from nvflare.app_common.streamers.file_streamer import FileStreamer
from nvflare.fuel.common.excepts import ConfigError
from nvflare.fuel.f3.cellnet.cell import Cell
from nvflare.fuel.f3.cellnet.defs import CellChannel, MessageHeaderKey
from nvflare.fuel.f3.cellnet.defs import ReturnCode as CellReturnCode
from nvflare.fuel.f3.cellnet.fqcn import FQCN
from nvflare.fuel.f3.cellnet.net_agent import NetAgent
from nvflare.fuel.f3.drivers.driver_params import DriverParams
from nvflare.fuel.f3.message import Message as CellMessage
from nvflare.fuel.hci.client.event import EventContext, EventHandler, EventPropKey, EventType
from nvflare.fuel.hci.cmd_arg_utils import split_to_args
from nvflare.fuel.hci.conn import Connection
from nvflare.fuel.hci.proto import (
    ConfirmMethod,
    InternalCommands,
    MetaKey,
    ProtoKey,
    ReplyKeyword,
    StreamChannel,
    StreamTopic,
    make_error,
    validate_proto,
)
from nvflare.fuel.hci.reg import CommandEntry, CommandModule, CommandRegister
from nvflare.fuel.hci.table import Table
from nvflare.fuel.sec.authn import set_add_auth_headers_filters
from nvflare.fuel.utils.admin_name_utils import new_admin_client_name
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.private.aux_runner import AuxMsgTarget, AuxRunner
from nvflare.private.defs import ClientType
from nvflare.private.fed.authenticator import Authenticator, validate_auth_headers
from nvflare.private.fed.utils.identity_utils import IdentityAsserter, TokenVerifier, get_cn_from_cert, load_cert_file
from nvflare.private.stream_runner import HeaderKey, ObjectStreamer
from nvflare.security.logging import secure_format_exception, secure_log_traceback

from .api_spec import (
    AdminAPISpec,
    AdminConfigKey,
    CommandContext,
    CommandCtxKey,
    CommandInfo,
    ReplyProcessor,
    UidSource,
)
from .api_status import APIStatus

_CMD_TYPE_UNKNOWN = 0
_CMD_TYPE_CLIENT = 1
_CMD_TYPE_SERVER = 2

MAX_AUTO_LOGIN_TRIES = 300
AUTO_LOGIN_INTERVAL = 1.5


class FileWaiter(threading.Event):

    def __init__(self, tx_id):
        super().__init__()
        self.tx_id = tx_id
        self.stream_ctx = None
        self.last_progress_time = time.time()

    def get_stream_ctx(self):
        pass


class ResultKey(object):

    STATUS = ProtoKey.STATUS
    DETAILS = ProtoKey.DETAILS
    META = ProtoKey.META
    AUTH_CODE = "auth_code"


def _print_hci_message(msg: str):
    pass


class _ServerReplyJsonProcessor(object):
    def __init__(self, ctx: CommandContext):
        if not isinstance(ctx, CommandContext):
            raise TypeError(f"ctx is not an instance of CommandContext. but get {type(ctx)}")
        self.ctx = ctx

    def process_server_reply(self, resp):
        """Process the server reply and store the status/details into API's `command_result`
        NOTE: this func is used for receive_and_process(), which is defined by conn!
        This method does not tale CommandContext!

        Args:
            resp: The raw response that returns by the server.
        """
        pass


class _DefaultReplyProcessor(ReplyProcessor):
    def process_shutdown(self, ctx: CommandContext, msg: str):
        pass


class _LoginReplyProcessor(ReplyProcessor):
    """Reply processor for handling login and setting the token for the admin client."""

    def process_string(self, ctx: CommandContext, item: str):
        pass

    def process_token(self, ctx: CommandContext, token: str):
        pass


class _CmdListReplyProcessor(ReplyProcessor):
    """Reply processor to register available commands after getting back a table of commands from the server."""

    def process_table(self, ctx: CommandContext, table: Table):
        pass


class AdminAPI(AdminAPISpec, StreamableEngine):
    def __init__(
        self,
        user_name: str,
        admin_config: dict,
        cmd_modules: Optional[List] = None,
        debug: bool = False,
        auto_login_max_tries: int = 15,
        event_handlers=None,
        study: str = DEFAULT_STUDY,
    ):
        """API to keep certs, keys and connection information and to execute admin commands through do_command.

        Args:
            cmd_modules: command modules to load and register. Note that FileTransferModule is initialized here with upload_dir and download_dir if cmd_modules is None.
            user_name: Username to authenticate with FL server
            debug: Whether to print debug messages, which can help with diagnosing problems. False by default.
            auto_login_max_tries: maximum number of tries to auto-login.
        """
        super().__init__()
        if cmd_modules is None:
            from .file_transfer import FileTransferModule

            upload_dir = admin_config.get(AdminConfigKey.UPLOAD_DIR, "transfer")
            download_dir = admin_config.get(AdminConfigKey.DOWNLOAD_DIR, "transfer")
            cmd_modules = [FileTransferModule(upload_dir=upload_dir, download_dir=download_dir)]
        elif not isinstance(cmd_modules, list):
            raise TypeError("cmd_modules must be a list, but got {}".format(type(cmd_modules)))
        else:
            for m in cmd_modules:
                if not isinstance(m, CommandModule):
                    raise TypeError(
                        "cmd_modules must be a list of CommandModule, but got element of type {}".format(type(m))
                    )

        if not event_handlers:
            event_handlers = []

        if event_handlers:
            if not isinstance(event_handlers, list):
                raise TypeError(f"event_handlers must be a list but got {type(event_handlers)}")
            for h in event_handlers:
                if not isinstance(h, EventHandler):
                    raise TypeError(f"item in event_handlers must be EventHandler but got {type(h)}")

        for m in cmd_modules:
            if isinstance(m, EventHandler):
                event_handlers.append(m)

        self.logger = get_obj_logger(self)
        self.conn_sec = admin_config.get(AdminConfigKey.CONNECTION_SECURITY)
        self.project_name = admin_config.get(AdminConfigKey.PROJECT_NAME)
        self.server_identity = admin_config.get(AdminConfigKey.SERVER_IDENTITY, "server")
        self.scheme = admin_config.get(AdminConfigKey.CONNECTION_SCHEME, "grpc")
        self.ca_cert = admin_config.get(AdminConfigKey.CA_CERT)
        self.client_cert = admin_config.get(AdminConfigKey.CLIENT_CERT)
        self.client_key = admin_config.get(AdminConfigKey.CLIENT_KEY)
        self.uid_source = admin_config.get(AdminConfigKey.UID_SOURCE, UidSource.USER_INPUT)
        self.host = admin_config.get(AdminConfigKey.HOST, "localhost")
        self.port = admin_config.get(AdminConfigKey.PORT, 8002)
        self.default_login_timeout = admin_config.get(AdminConfigKey.LOGIN_TIMEOUT, 10.0)
        self.file_download_progress_timeout = admin_config.get(AdminConfigKey.FILE_DOWNLOAD_PROGRESS_TIMEOUT, 5.0)
        self.authenticate_msg_timeout = admin_config.get(AdminConfigKey.AUTHENTICATE_MSG_TIMEOUT, 5.0)
        self.user_name = user_name
        self.study = study
        self.event_handlers = event_handlers

        if not self.ca_cert:
            raise ConfigError("missing CA Cert file name")
        if not self.client_cert:
            raise ConfigError("missing Client Cert file name")
        if not self.client_key:
            raise ConfigError("missing Client Key file name")

        if self.uid_source == UidSource.CERT:
            # We'll find the username from the client cert
            cert = load_cert_file(self.client_cert)
            self.user_name = get_cn_from_cert(cert)

        if not self.user_name:
            raise Exception("user_name is required.")

        if debug:
            self._debug = debug
        else:
            self._debug = admin_config.get(AdminConfigKey.WITH_DEBUG, False)

        self.cmd_timeout = None

        # for login
        self.token = None
        self.login_result = None

        self.server_cmd_reg = CommandRegister(app_ctx=self)
        self.client_cmd_reg = CommandRegister(app_ctx=self)
        self.server_cmd_received = False

        self.all_cmds = []
        self.cmd_modules = cmd_modules

        # for shutdown
        self.shutdown_received = False
        self.shutdown_msg = None

        self.server_sess_active = False
        self.shutdown_asked = False

        self.sess_monitor_thread = None
        self.sess_monitor_active = False

        # create the FSM for session monitoring
        if auto_login_max_tries < 0 or auto_login_max_tries > MAX_AUTO_LOGIN_TRIES:
            raise ValueError(f"auto_login_max_tries is out of range: [0, {MAX_AUTO_LOGIN_TRIES}]")
        self.auto_login_max_tries = auto_login_max_tries

        self.closed = False
        self.in_logout = False
        self.cell = None
        self.aux_runner = None
        self.object_streamer = None
        self.fl_ctx_mgr = FLContextManager(
            engine=self,
            identity_name=self.user_name,
            private_stickers={FLContextKey.PROCESS_TYPE: ProcessType.CLIENT_PARENT},
        )
        self.file_download_waiters = {}  # tx_id => Threading.Event

    def new_context(self):
        pass

    def connect(self, timeout=None):
        pass

    def _handle_aux_message(self, request: CellMessage) -> CellMessage:
        pass

    def download_file(self, source_fqcn: str, ref_id: str, file_name: str):
        pass

    def get_cell(self):
        pass

    def _handle_session_expired(self, message: CellMessage):
        pass

    def debug(self, msg):
        pass

    def _print_hci(self, msg: str):
        pass

    def fire_event(self, event_type: str, ctx: EventContext):
        pass

    def set_command_timeout(self, timeout: float):
        pass

    def unset_command_timeout(self):
        pass

    def _new_event_context(self):
        pass

    def fire_session_event(self, event_type: str, msg: str = ""):
        pass

    def _try_login(self):
        pass

    def login(self):
        pass

    def _load_client_cmds_from_modules(self, cmd_modules):
        pass

    def _load_client_cmds_from_module_specs(self, cmd_module_specs):
        pass

    def register_command(self, cmd_entry):
        pass

    def logout(self):
        """Send logout command to server."""
        pass

    def close(self):
        # this method can be called multiple times
        pass

    def _get_command_list_from_server(self) -> bool:
        pass

    def _after_login(self) -> dict:
        pass

    def is_ready(self) -> bool:
        """Whether the API is ready for executing commands."""
        pass

    def _user_login(self):
        """Login user

        Returns:
            A dict of login status and details
        """
        pass

    def _send_to_cell(self, ctx: CommandContext):
        pass

    def _try_command(self, cmd_ctx: CommandContext):
        """Try to execute a command on server side.

        Args:
            cmd_ctx: The command to execute.
        """
        pass

    def _get_command_detail(self, command):
        """Get command details

        Args:
          command (str): command

        Returns: tuple of (cmd_type, cmd_name, args, entries)
        """
        pass

    def check_command(self, command: str) -> CommandInfo:
        """Checks the specified command for processing info

        Args:
            command: command to be checked

        Returns: command processing info

        """
        pass

    def _new_command_context(self, command, args, ent: CommandEntry):
        pass

    def _do_client_command(self, command, args, ent: CommandEntry, props=None):
        pass

    def upload_file(self, file_name: str, conn: Connection):
        pass

    def do_command(self, command: str, props=None):
        """A convenient method to call commands using string.

        Args:
          command (str): command
          props: additional props

        Returns:
            Object containing status and details (or direct response from server, which originally was just time and data)
        """
        pass

    def server_execute(self, command, reply_processor=None, cmd_entry=None, cmd_ctx=None, props=None, headers=None):
        pass

    def _determine_api_status(self, result):
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
            consumed_cb: the callback to be called after a chunk is processed

        Returns: None

        """
        pass

    def shutdown_streamer(self):
        """Shutdown the engine's streamer.

        Returns: None

        """
        pass
