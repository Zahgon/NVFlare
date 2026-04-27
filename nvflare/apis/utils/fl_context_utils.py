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
from typing import Optional

from nvflare.apis.client import Client
from nvflare.apis.fl_constant import FLContextKey, NonSerializableKeys
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.fuel.sec.audit import AuditService
from nvflare.fuel.utils import fobs
from nvflare.fuel.utils.log_utils import get_module_logger
from nvflare.security.logging import secure_format_exception

logger = get_module_logger()


def get_serializable_data(fl_ctx: FLContext):
    pass


def gen_new_peer_ctx(fl_ctx: FLContext, need_deep_copy=False):
    pass


def generate_log_message(fl_ctx: FLContext, msg: str):
    pass


def add_job_audit_event(fl_ctx: FLContext, ref: str = "", msg: str = "") -> str:
    pass


def get_client(client_name, fl_ctx: FLContext) -> Optional[Client]:
    """Get the Client object for the specified client name

    Args:
        client_name: name of the client to be found
        fl_ctx: the FLContext object

    Returns: a Client object or None if not found

    """
    pass
