# Copyright (c) 2026, NVIDIA CORPORATION.  All rights reserved.
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

"""nvflare package subcommand: parser registration and dispatch."""

import argparse
from typing import Optional

_package_parser: Optional[argparse.ArgumentParser] = None

_PACKAGE_EXAMPLES = [
    "nvflare package -e grpc://fl-server:8002 -p ./site.yaml --dir ./certs",
    "nvflare package -e grpc://fl-server:8002 --dir ./hospital-1-kit",
    "nvflare package -n hospital-1 -e grpc://fl-server:8002 --cert ./signed/hospital-1/hospital-1.crt --key ./csr/hospital-1.key --rootca ./signed/hospital-1/rootCA.pem",
]

_PACKAGE_HELP_EXAMPLES = """Examples:
  Build kits from a project YAML:
    nvflare package -e grpc://fl-server:8002 -p ./site.yaml --dir ./certs

  Build one kit from a working directory:
    nvflare package -e grpc://fl-server:8002 --dir ./hospital-1-kit

  Build one kit from explicit file paths:
    nvflare package -n hospital-1 -e grpc://fl-server:8002 \\
      --cert ./signed/hospital-1/hospital-1.crt \\
      --key ./csr/hospital-1.key \\
      --rootca ./signed/hospital-1/rootCA.pem
"""


def _add_compat_output_arg(parser: argparse.ArgumentParser) -> None:
    pass


def def_package_cli_parser(sub_cmd) -> dict:
    """Register 'nvflare package' with the top-level sub_cmd parser."""
    pass


def handle_package_cmd(args):
    """Dispatch to package handler."""
    pass
