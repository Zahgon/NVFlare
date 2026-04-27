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
from nvflare.app_common.tie.cli_applet import CLIApplet, CommandDescriptor
from nvflare.app_common.tie.py_applet import PyApplet, PyRunner
from nvflare.app_opt.flower.defs import Constant

from .flower_client import train


class MockClientApplet(CLIApplet):
    def __init__(self):
        CLIApplet.__init__(self)

    def get_command(self, app_ctx: dict) -> CommandDescriptor:
        pass


class MockServerApplet(CLIApplet):
    def __init__(self):
        CLIApplet.__init__(self)

    def get_command(self, app_ctx: dict) -> CommandDescriptor:
        pass


class MockClientPyRunner(PyRunner):
    def __init__(self):
        self.stopped = False

    def start(self, app_ctx: dict):
        pass

    def stop(self, timeout: float):
        pass

    def is_stopped(self) -> (bool, int):
        pass


class MockClientPyApplet(PyApplet):
    def __init__(self, in_process=True):
        PyApplet.__init__(self, in_process)

    def get_runner(self, app_ctx: dict) -> PyRunner:
        pass
