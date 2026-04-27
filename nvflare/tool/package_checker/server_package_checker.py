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

import json
import os
import shutil
import sys

from .check_rule import CheckAddressBinding, CheckWriting
from .package_checker import PackageChecker
from .utils import NVFlareConfig, get_communication_scheme

SERVER_SCRIPT = "nvflare.private.fed.app.server.server_train"


def _get_server_fed_config(package_path: str):
    pass


def _get_snapshot_storage_root(package_path: str) -> str:
    pass


def _get_job_storage_root(package_path: str) -> str:
    pass


def _get_fl_host_and_port(package_path: str) -> (str, int):
    """Get federated learning service host and port.

    This is the main communication port for FL, which could use GRPC, TCP, or HTTP scheme.
    """
    pass


def _get_admin_host_and_port(package_path: str) -> (str, int):
    pass


class ServerPackageChecker(PackageChecker):
    def __init__(self):
        super().__init__()
        self.snapshot_storage_root = None
        self.job_storage_root = None

    def init_rules(self, package_path):
        pass

    def should_be_checked(self) -> bool:
        pass

    def get_dry_run_command(self) -> str:
        pass

    def stop_dry_run(self, force=True):
        pass
