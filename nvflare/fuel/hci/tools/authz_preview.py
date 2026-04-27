# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
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
import sys

from nvflare.fuel.hci.cmd_arg_utils import split_to_args
from nvflare.fuel.hci.table import Table
from nvflare.fuel.sec.authz import AuthzContext, Person, Policy, parse_policy_config
from nvflare.security.security import COMMAND_CATEGORIES


class Commander(cmd.Cmd):
    def __init__(self, policy: Policy):
        """Command line prompt helper tool for getting information for authorization configurations.

        Args:
            policy: authorization policy object
        """
        cmd.Cmd.__init__(self)
        self.policy = policy
        self.intro = "Type help or ? to list commands.\n"
        self.prompt = "> "

    def do_bye(self, arg):
        """Exits from the client."""
        pass

    def emptyline(self):
        pass

    def _split_to_args(self, arg):
        pass

    def do_show_rights(self, arg):
        pass

    def do_show_roles(self, arg):
        pass

    def do_show_config(self, arg):
        pass

    def do_show_role_rights(self, arg):
        pass

    def _parse_person(self, spec: str):
        pass

    def do_eval_right(self, arg):
        pass

    def write_string(self, data: str):
        pass

    def write_table(self, table: Table):
        pass

    def write_error(self, err: str):
        pass


def define_authz_preview_parser(parser):
    pass


def load_policy(policy_file_path):
    pass


def run_command(args):
    pass


def main():
    """Tool to help preview and see the details of an authorization policy with command line commands."""
    pass


if __name__ == "__main__":
    main()
