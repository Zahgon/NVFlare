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
from typing import List

import psutil

try:
    import pynvml
except ImportError:
    pynvml = None

from nvflare.apis.fl_constant import FLContextKey, SystemComponents
from nvflare.apis.fl_context import FLContext
from nvflare.fuel.utils.log_utils import dynamic_log_config, validate_site_log_config
from nvflare.private.admin_defs import Message, error_reply, ok_reply
from nvflare.private.defs import SysCommandTopic
from nvflare.private.fed.client.admin import RequestProcessor
from nvflare.security.logging import secure_format_exception


class SysInfoProcessor(RequestProcessor):
    def get_topics(self) -> List[str]:
        pass

    def process(self, req: Message, app_ctx) -> Message:
        pass


class ReportEnvProcessor(RequestProcessor):
    def get_topics(self) -> [str]:
        pass

    def process(self, req: Message, app_ctx) -> Message:
        pass


class ConfigureSiteLogProcessor(RequestProcessor):
    def get_topics(self) -> List[str]:
        pass

    def process(self, req: Message, app_ctx) -> Message:
        pass
