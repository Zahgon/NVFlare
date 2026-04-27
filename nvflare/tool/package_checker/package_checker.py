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
import signal
from abc import ABC, abstractmethod
from collections import defaultdict
from subprocess import TimeoutExpired

from nvflare.tool.package_checker.check_rule import CHECK_PASSED, CheckResult, CheckRule
from nvflare.tool.package_checker.utils import run_command_in_subprocess, split_by_len


class PackageChecker(ABC):
    def __init__(self):
        self.report = defaultdict(list)
        self.check_len = len("Checks")
        self.problem_len = 80
        self.fix_len = len("How to fix")
        self.dry_run_timeout = 5
        self.package_path = None
        self.rules = []

    @abstractmethod
    def init_rules(self, package_path: str):
        pass

    def init(self, package_path: str):
        pass

    @abstractmethod
    def should_be_checked(self) -> bool:
        """Check if this package should be checked by this checker."""
        pass

    @abstractmethod
    def get_dry_run_command(self) -> str:
        """Returns dry run command."""
        pass

    def get_dry_run_inputs(self):
        pass

    def stop_dry_run(self, force: bool = True):
        pass

    def check(self) -> int:
        """Checks if the package is runnable on the current system.

        Returns:
            0: if no dry-run process started.
            1: if the dry-run process is started and return code is 0.
            2: if the dry-run process is started and return code is not 0.
        """
        pass

    def check_dry_run(self) -> int:
        """Runs dry run command.

        Returns:
            0: if no process started.
            1: if the process is started and return code is 0.
            2: if the process is started and return code is not 0.
        """
        pass

    def add_report(self, check_name, problem_text: str, fix_text: str):
        pass

    def _print_line(self):
        pass

    def _print_row(self, check, problem, fix):
        pass

    def print_report(self):
        pass
