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

import os
import subprocess

from nvflare.app_opt.confidential_computing.cc_authorizer import CCAuthorizer

TDX_NAMESPACE = "x-tdx"
TDX_CLI_CONFIG = "config.json"
TOKEN_FILE = "token.txt"
VERIFY_FILE = "verify.txt"
ERROR_FILE = "error.txt"


class TDXAuthorizer(CCAuthorizer):
    """Intel TDX Authorizer"""

    def __init__(self, tdx_cli_command: str, config_dir: str) -> None:
        """Initialize the TDXAuthorizer

        Args:
            tdx_cli_command (str): The command to run the TDX CLI
            config_dir (str): The directory to store the TDX CLI configuration and token
        """
        super().__init__()
        self.tdx_cli_command = tdx_cli_command
        self.config_dir = config_dir

        self.config_file = os.path.join(self.config_dir, TDX_CLI_CONFIG)

    def generate(self) -> str:
        pass

    def verify(self, token: str) -> bool:
        pass

    def get_namespace(self) -> str:
        pass
