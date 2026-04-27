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

"""Federated Simulator launching script."""

import argparse
import os
import sys
from sys import platform

from nvflare.fuel.utils.log_utils import FL_LOG_LEVEL, LogMode
from nvflare.private.fed.app.simulator.simulator_runner import SimulatorRunner
from nvflare.private.fed.app.utils import version_check


def define_simulator_parser(simulator_parser):
    pass


def run_simulator(simulator_args):
    pass


if __name__ == "__main__":
    """
    This is the main program when running the NVFlare Simulator. Use the Flare simulator API,
    create the SimulatorRunner object, do a setup(), then calls the run().
    """

    # For MacOS, it needs to use 'spawn' for creating multi-process.
    if platform == "darwin":
        # OS X
        import multiprocessing

        multiprocessing.set_start_method("spawn")

    version_check()

    parser = argparse.ArgumentParser()
    define_simulator_parser(parser)
    args = parser.parse_args()
    status = run_simulator(args)
    sys.exit(status)
