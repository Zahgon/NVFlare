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
import os
from typing import List

from nvflare.apis.job_def import JobMetaKey
from nvflare.apis.workspace import Workspace
from nvflare.fuel.hci.proto import MetaStatusValue, make_meta
from nvflare.lighter.tool_consts import NVFLARE_SIG_FILE
from nvflare.lighter.utils import verify_folder_signature
from nvflare.private.admin_defs import Message, error_reply, ok_reply
from nvflare.private.defs import RequestHeader, ScopeInfoKey, TrainingTopic
from nvflare.private.fed.client.admin import RequestProcessor
from nvflare.private.fed.client.client_engine_internal_spec import ClientEngineInternalSpec
from nvflare.private.fed.utils.fed_utils import get_scope_info


class AbortAppProcessor(RequestProcessor):
    def get_topics(self) -> List[str]:
        pass

    def process(self, req: Message, app_ctx) -> Message:
        pass


class AbortTaskProcessor(RequestProcessor):
    def get_topics(self) -> List[str]:
        pass

    def process(self, req: Message, app_ctx) -> Message:
        pass


class ShutdownClientProcessor(RequestProcessor):
    def get_topics(self) -> List[str]:
        pass

    def process(self, req: Message, app_ctx) -> Message:
        pass


class RestartClientProcessor(RequestProcessor):
    def get_topics(self) -> List[str]:
        pass

    def process(self, req: Message, app_ctx) -> Message:
        pass


class DeployProcessor(RequestProcessor):
    def get_topics(self) -> List[str]:
        pass

    def process(self, req: Message, app_ctx) -> Message:
        # Note: this method executes in the Main process of the client
        pass


class DeleteRunNumberProcessor(RequestProcessor):
    def get_topics(self) -> List[str]:
        pass

    def process(self, req: Message, app_ctx) -> Message:
        pass


class ConfigureJobLogProcessor(RequestProcessor):
    def get_topics(self) -> List[str]:
        pass

    def process(self, req: Message, app_ctx) -> Message:
        pass


class ClientStatusProcessor(RequestProcessor):
    def get_topics(self) -> List[str]:
        pass

    def process(self, req: Message, app_ctx) -> Message:
        pass


class ScopeInfoProcessor(RequestProcessor):
    def get_topics(self) -> List[str]:
        pass

    def process(self, req: Message, app_ctx) -> Message:
        pass


class NotifyJobStatusProcessor(RequestProcessor):
    def get_topics(self) -> [str]:
        pass

    def process(self, req: Message, app_ctx) -> Message:
        pass
