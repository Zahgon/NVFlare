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

import json
from datetime import datetime
from typing import List

from .table import Table

LINE_END = "\x03"  # Indicates the end of the line (end of text)
ALL_END = "\x04"  # Marks the end of a complete transmission (End of Transmission)

MAX_BLOCK_SIZE = 1024


class ProtoKey(object):

    TIME = "time"
    DATA = "data"
    META = "meta"
    TYPE = "type"
    STRING = "string"
    TABLE = "table"
    ROWS = "rows"
    DICT = "dict"
    SUCCESS = "success"
    ERROR = "error"
    SHUTDOWN = "shutdown"
    COMMAND = "command"
    TOKEN = "token"
    DETAILS = "details"
    STATUS = "status"
    APP_DATA = "app_data"  # used by application to add additional data


class MetaKey(object):

    STATUS = "status"
    INFO = "info"
    JOB_ID = "job_id"
    DATA_TYPE = "data_type"
    JOB_META = "job_meta"
    JOB_DATA = "job_data"
    JOB_COMPONENTS = "job_components"
    WORKSPACE = "workspace"
    JOB_DOWNLOAD_URL = "job_download_url"
    APP_NAME = "app_name"
    SERVER_STATUS = "server_status"
    SERVER_START_TIME = "server_start_time"
    CLIENT_NAME = "client_name"
    CLIENT_LAST_CONNECT_TIME = "client_last_conn_time"
    CLIENTS = "clients"
    CLIENT_STATUS = "client_status"
    FQCN = "fqcn"
    JOBS = "jobs"
    JOB_NAME = "job_name"
    SUBMIT_TIME = "submit_time"
    DURATION = "duration"
    CMD_TIMEOUT = "cmd_timeout"
    CUSTOM_PROPS = "custom_props"
    CMD_PROPS = "cmd_props"
    CMD_HEADERS = "cmd_headers"
    FILES = "files"
    CMD_NAME = "cmd_name"
    TX_ID = "tx_id"
    FOLDER_NAME = "folder_name"
    LOCATION = "location"
    SOURCE_FQCN = "source_fqcn"


class MetaStatusValue(object):

    OK = "ok"
    SYNTAX_ERROR = "syntax_error"
    NOT_AUTHORIZED = "not_authorized"
    NOT_AUTHENTICATED = "not_authenticated"
    ERROR = "error"
    INTERNAL_ERROR = "internal_error"
    INVALID_TARGET = "invalid_target"
    INVALID_JOB_DEFINITION = "invalid_job_def"
    INVALID_JOB_ID = "invalid_job_id"
    JOB_RUNNING = "job_running"
    JOB_NOT_RUNNING = "job_not_running"
    CLIENTS_RUNNING = "clients_running"
    NO_JOBS = "no_jobs"
    NO_JOB_COMPONENTS = "no_job_compoents"
    NO_REPLY = "no_reply"
    NO_CLIENTS = "no_clients"


class ReplyKeyword:
    """
    Admin API relies on certain keywords in the server reply to determine command status.
    We define these keywords here to assure that the server and client sides use the keywords consistently.
    """

    NO_CLIENTS = "no clients available"
    SESSION_INACTIVE = "session_inactive"
    WRONG_SERVER = "wrong server"
    COMM_FAILURE = "Failed to communicate"
    INVALID_CLIENT = "invalid client"
    UNKNOWN_SITE = "unknown site"
    NOT_AUTHORIZED = "not authorized"


class InternalCommands(object):

    CERT_LOGIN = "_cert_login"
    LOGOUT = "_logout"
    GET_CMD_LIST = "_commands"
    CHECK_SESSION = "_check_session"
    LIST_SESSIONS = "list_sessions"

    commands = [CERT_LOGIN, LOGOUT, GET_CMD_LIST, CHECK_SESSION, LIST_SESSIONS]

    @classmethod
    def contains_command(cls, command: str):
        pass


class ConfirmMethod(object):

    AUTH = "auth"
    YESNO = "yesno"


class StreamChannel:
    UPLOAD = "hci.upload"
    DOWNLOAD = "hci.download"


class StreamTopic:
    FOLDER = "folder"
    FILE = "file"


class Buffer(object):
    def __init__(self):
        """Buffer to append to for :class:`nvflare.fuel.hci.conn.Connection`."""
        self.meta = {}
        self.data = []
        self.output = {ProtoKey.TIME: f"{format(datetime.now())}", ProtoKey.DATA: self.data, ProtoKey.META: self.meta}

    def append_table(self, headers: List[str], name=None) -> Table:
        pass

    def update_meta(self, meta: dict):
        pass

    def append_string(self, data: str, meta: dict = None):
        pass

    def append_dict(self, data: dict, meta: dict = None):
        pass

    def append_success(self, data: str, meta: dict = None):
        pass

    def append_error(self, data: str, meta: dict = None):
        pass

    def append_command(self, cmd: str):
        pass

    def append_token(self, token: str):
        pass

    def append_shutdown(self, msg: str):
        pass

    def encode(self):
        pass

    def reset(self):
        pass


def make_error(data: str):
    pass


def validate_proto(line: str):
    """Validate that the line being received is of the expected format.

    Args:
        line: str containing a JSON document

    Returns: deserialized JSON document
    """
    pass


def make_meta(status: str, info: str = "", extra: dict = None) -> dict:
    pass
