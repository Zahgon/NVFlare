# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
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

import grpc

from nvflare.apis.fl_context import FLContext
from nvflare.private.fed.client.admin import RequestProcessor
from nvflare.private.fed.client.client_req_processors import ClientRequestProcessors
from nvflare.private.fed.client.fed_client import FederatedClient


class BaseClientDeployer:
    def __init__(self):
        """To init the BaseClientDeployer."""
        self.multi_gpu = False
        self.outbound_filters = None
        self.inbound_filters = None
        self.federated_client = None
        self.model_validator = None
        self.cross_val_participating = False
        self.model_registry_path = None
        self.cross_val_timeout = None
        self.executors = None

        self.req_processors = ClientRequestProcessors.request_processors

    def build(self, build_ctx):
        pass

    def create_fed_client(self, args, sp_target=None):
        pass

    def finalize(self, fl_ctx: FLContext):
        pass

    def close(self):
        # if self.federated_client:
        #     self.federated_client.model_manager.close()
        pass
