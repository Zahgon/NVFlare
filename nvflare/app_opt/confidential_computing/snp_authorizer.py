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

import base64
import logging
import os
import re
import secrets
import shutil
import subprocess
import time
import uuid

from filelock import FileLock

from nvflare.app_opt.confidential_computing.cc_authorizer import CCAuthorizer

from .utils import NonceHistory

SNP_NAMESPACE = "x-snp"
REPORT_PATH = "report.bin"
REQUEST_PATH = "request.bin"

AMD_ARK = "ark.pem"
AMD_ASK = "ask.pem"
AMD_VCEK = "vcek.pem"


def parse_chip_id(report_text: str) -> str:
    # Find the block starting with "Chip ID:" followed by multiple lines of hex bytes
    pass


def parse_reported_tcb(report_text: str) -> dict:
    # Match the entire Reported TCB block after the line "Reported TCB:"
    pass


class SNPAuthorizer(CCAuthorizer):
    """AMD SEV-SNP Authorizer"""

    def __init__(
        self,
        max_nonce_history=1000,
        amd_certs_dir="/opt/certs",
        snpguest_binary="snpguest",
        cpu_model="milan",
        max_retries=5,
        retry_interval=10,
        cmd_timeout=60,
    ):
        """
        Initialize the SNPAuthorizer instance.

        Args:
            max_nonce_history (int, optional): Maximum number of nonces to keep in history for replay protection.
                Defaults to 1000.
            amd_certs_dir (str, optional): Directory path where AMD certificates are stored.
                Defaults to "/opt/certs".
            snpguest_binary (str, optional): Path to the `snpguest` binary used for generating and verifying reports.
                Defaults to "/host/bin/snpguest".
            cpu_model (str, optional): CPU model identifier used when fetching certificates.
                Defaults to "milan".
            max_retries (int): Max number of retries on transient failures.
            retry_interval (int): Wait time (seconds) between retries.
            cmd_timeout (int): SNPGuest command timeout.
        """
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.my_nonce_history = NonceHistory(max_nonce_history)
        self.seen_nonce_history = NonceHistory(max_nonce_history)
        self.amd_certs_dir = amd_certs_dir
        self.snpguest_binary = snpguest_binary
        self.cpu_model = cpu_model
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.cmd_timeout = cmd_timeout

    def _run_with_retry(self, cmd: list[str], action_name: str) -> subprocess.CompletedProcess:
        pass

    def generate(self):
        pass

    def verify(self, token):
        pass

    def _ensure_amd_ca_certs(self):
        """Ensures AMD CA certs are inside the amd_certs_dir."""
        pass

    def _ensure_amd_vcek(self, vcek_cache_key, report_bin_file, timeout=60):
        """Ensures AMD VCEK is inside the amd_certs_dir."""
        pass

    def _parse_report(self, report_bin_file):
        """Parses the Reported TCB and Chip ID info.

        This method is used to generate a unique id to cache VCEK.
        Because AMD KDS has rate limitation, we should avoid keep polling.
        """
        pass

    def _check_nonce(self, report_bin_file):
        """Parses nonce from the Report Data section and checks if it is fresh."""
        pass

    def get_namespace(self) -> str:
        pass
