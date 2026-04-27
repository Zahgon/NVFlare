# Copyright (c) 2023, NVIDIA CORPORATION.  All rights reserved.
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


from . import utils


class Template:
    def __init__(self, template):
        self.template = template
        self.supported_csps = ("azure", "aws")

    def get_cloud_script_header(self):
        pass

    def get_azure_server_start_sh(self, entity):
        pass

    def get_aws_server_start_sh(self, entity):
        pass

    def get_azure_client_start_sh(self, entity):
        pass

    def get_aws_client_start_sh(self, entity):
        pass

    def get_azure_start_svr_header_sh(self):
        pass

    def get_azure_start_cln_header_sh(self):
        pass

    def get_azure_start_common_sh(self):
        pass

    def get_sub_start_sh(self):
        pass

    def get_azure_svr_sh(self):
        pass

    def get_azure_cln_sh(self):
        pass

    def get_start_sh(self, csp, type, entity):
        pass
