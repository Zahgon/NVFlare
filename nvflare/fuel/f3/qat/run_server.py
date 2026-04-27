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

import argparse
import logging

from nvflare.fuel.f3.mpm import MainProcessMonitor
from nvflare.fuel.f3.qat.server import Server
from nvflare.fuel.utils.config_service import ConfigService


def main():
    """
    Script to launch the admin client to issue admin commands to the server.
    """
    pass


if __name__ == "__main__":
    MainProcessMonitor.run(main)
