# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
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
import time

import jwt
import requests

from nvflare.app_opt.confidential_computing.cc_authorizer import CCAuthorizer

ACI_NAMESPACE = "x-az-aci"


class ACIAuthorizer(CCAuthorizer):
    def __init__(self, maa_endpoint="sharedeus2.eus2.attest.azure.net", retry_count=5, retry_sleep=2):
        self.maa_endpoint = maa_endpoint
        self.retry_count = retry_count
        self.retry_sleep = retry_sleep

    def generate(self):
        pass

    def verify(self, token):
        pass

    def get_namespace(self) -> str:
        pass
