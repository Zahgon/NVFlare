# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
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
from typing import Optional

from nvflare.apis.client import Client
from nvflare.apis.fl_context import FLContext
from nvflare.fuel.f3.cellnet.fqcn import FQCN
from nvflare.private.fed.utils.identity_utils import get_parent_site_name


def determine_parent_name(client_config: dict) -> Optional[str]:
    """Determine the parent site name from the config of a client.

    Args:
        client_config: the config of client

    Returns: the name of parent client or None if the client has no parent

    """
    pass


def determine_parent_fqcn(client_config: dict, fl_ctx: FLContext) -> str:
    """Determine the FQCN of the parent cell based on client config.
    This function is used to determine the endpoint for pulling task, submitting task result, etc. in
    hierarchical client network.

    Args:
        client_config: config of the client
        fl_ctx: FLContext object that contains engine

    Returns: the FQCN of the parent cell

    """
    pass
