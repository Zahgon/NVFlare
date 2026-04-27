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
import cmd
import json

from nvflare.fuel.f3.stats_pool import VALID_HIST_MODES, StatsPoolManager, parse_hist_mode
from nvflare.fuel.hci.table import Table


class StatsViewer(cmd.Cmd):
    def __init__(self, pools: dict, prompt: str = "> "):
        cmd.Cmd.__init__(self)
        self.intro = "Type help or ? to list commands.\n"
        self.prompt = prompt
        self.pools = pools
        StatsPoolManager.from_dict(pools)

    def do_list_pools(self, arg):
        pass

    def do_show_pool(self, arg: str):
        pass

    def _show_table(self, headers, rows):
        pass

    def do_bye(self, arg):
        pass

    def emptyline(self):
        pass

    def run(self):
        pass

    def _write(self, content: str):
        pass

    def write_string(self, data: str):
        pass


def main():
    pass


if __name__ == "__main__":
    main()
