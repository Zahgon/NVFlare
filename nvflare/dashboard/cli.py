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

import argparse
import os
import signal
import subprocess
import sys

import docker
import nvflare
from nvflare.apis.utils.format_check import name_check
from nvflare.dashboard.utils import EnvVar
from nvflare.lighter import tplt_utils, utils

supported_csp = ("azure", "aws")


def start(args):
    pass


def start_local(env):
    pass


def stop():
    pass


def cloud(args):
    pass


def has_no_arguments() -> bool:
    pass


def main():
    pass


def define_dashboard_parser(parser):
    pass


def handle_dashboard(args):
    pass


if __name__ == "__main__":
    main()
