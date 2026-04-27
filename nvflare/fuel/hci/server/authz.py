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
import enum
import logging
from typing import List

from nvflare.fuel.hci.conn import Connection
from nvflare.fuel.hci.proto import MetaStatusValue, ReplyKeyword, make_meta
from nvflare.fuel.hci.reg import CommandEntry
from nvflare.fuel.sec.authz import AuthorizationService, AuthzContext, Person

from .constants import ConnProps
from .reg import CommandFilter

log = logging.getLogger(__name__)


class PreAuthzReturnCode(enum.Enum):

    OK = 0  # command preprocessed successfully, and no authz needed
    ERROR = 1  # error occurred in command processing
    REQUIRE_AUTHZ = 2  # command preprocessed successfully, further authz required


def command_handler_func_signature(conn: Connection, args: List[str]):
    pass


def command_authz_func_signature(conn: Connection, args: List[str]) -> PreAuthzReturnCode:
    pass


class AuthzFilter(CommandFilter):
    def __init__(self):
        """Filter for authorization of admin commands."""
        CommandFilter.__init__(self)

    def pre_command(self, conn: Connection, args: List[str]):
        pass
