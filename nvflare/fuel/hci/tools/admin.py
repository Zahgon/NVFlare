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

import argparse
import os
import sys

from nvflare.apis.job_def import DEFAULT_STUDY
from nvflare.apis.utils.format_check import name_check
from nvflare.apis.workspace import Workspace
from nvflare.fuel.common.excepts import ConfigError
from nvflare.fuel.hci.client.api_spec import AdminConfigKey
from nvflare.fuel.hci.client.cli import AdminClient
from nvflare.fuel.hci.client.config import secure_load_admin_config
from nvflare.fuel.hci.client.file_transfer import FileTransferModule
from nvflare.security.logging import secure_format_exception

DEFAULT_CLI_HIST_SIZE = 1000


def main():
    """
    Script to launch the admin client to issue admin commands to the server.
    """
    pass


if __name__ == "__main__":
    main()
