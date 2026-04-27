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

import os
import re
import sys

from .check_rule import CheckServerAvailable
from .package_checker import PackageChecker
from .utils import NVFlareConfig, NVFlareRole

CLIENT_SCRIPT = "nvflare.private.fed.app.client.client_train"


class ClientPackageChecker(PackageChecker):
    NVF_CONFIG = NVFlareConfig.CLIENT
    NVF_ROLE = NVFlareRole.CLIENT

    def should_be_checked(self) -> bool:
        """Check if this package should be checked by this checker."""
        pass

    def init_rules(self, package_path):
        """Initialize preflight check rules.

        The CheckServerAvailable rule automatically detects the communication scheme
        (GRPC, HTTP, etc.) and uses the appropriate connectivity check method.
        """
        pass

    def get_uid_from_startup_script(self) -> str:
        """Extract uid from sub_start.sh"""
        pass

    def get_dry_run_command(self) -> str:
        pass
