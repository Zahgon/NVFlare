# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
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
import threading

from nvflare.fuel.f3.cellnet.core_cell import CoreCell
from nvflare.fuel.f3.cellnet.net_agent import NetAgent
from nvflare.fuel.f3.mpm import MainProcessMonitor


class TwoHeader:
    def __init__(self, root1: str, name1: str, root2: str, name2: str):
        self.waiter = threading.Event()

        self.cell1 = CoreCell(
            fqcn=name1,
            root_url=root1,
            secure=False,
            credentials={},
            create_internal_listener=False,
        )
        self.agent1 = NetAgent(self.cell1, agent_closed_cb=self._agent1_closed)

        self.cell2 = CoreCell(
            fqcn=name2,
            root_url=root2,
            secure=False,
            credentials={},
            create_internal_listener=False,
        )
        self.agent2 = NetAgent(self.cell2, agent_closed_cb=self._agent2_closed)

    def _agent1_closed(self):
        pass

    def _agent2_closed(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def run(self):
        pass


def main():
    pass


if __name__ == "__main__":
    MainProcessMonitor.run(main)
