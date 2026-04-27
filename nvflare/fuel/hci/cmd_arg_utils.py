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
import io
import os
import re
import shlex
from typing import List

from nvflare.apis.utils.format_check import type_pattern_mapping


def _split_unquoted_args(line: str) -> List[str]:
    pass


def _has_quotes(line: str) -> bool:
    pass


def _split_quoted_args(line: str) -> List[str]:
    """Split HCI command args for quoted input, honoring shell quotes.

    Fall back to the unquoted whitespace splitter for malformed quoting so we
    don't turn previously accepted inputs into parse errors.
    """
    pass


def split_to_args(line: str) -> List[str]:
    pass


def parse_command_line(line: str) -> (str, List[str], str):
    """Parse the command line and extract command args and command props, if any

    Args:
        line:

    Returns:

    """
    pass


def join_args(segs: List[str]) -> str:
    pass


class ArgValidator(argparse.ArgumentParser):
    def __init__(self, name):
        """Validator for admin shell commands that uses argparse to check arguments and get usage through print_help.

        Args:
            name: name of the program to pass to ArgumentParser
        """
        argparse.ArgumentParser.__init__(self, prog=name, add_help=False)
        self.err = ""

    def error(self, message):
        pass

    def validate(self, args):
        pass

    def get_usage(self) -> str:
        pass


def process_targets_into_str(targets: List[str]) -> str:
    pass


def validate_required_target_string(target: str) -> str:
    """Returns the target string if it exists and is valid."""
    pass


def validate_options_string(options: str) -> str:
    """Returns the options string if it is valid."""
    pass


def validate_path_string(path: str) -> str:
    """Returns the path string if it is valid."""
    pass


def get_file_extension(file: str) -> str:
    """Get extension part of the specified file name.
    If the file's name is ended with number, then the extension is before it.

    Args:
        file: the file name

    Returns: extension part of the file name

    """
    pass


def validate_text_file_name(file_name: str) -> str:
    """Check the specified file name whether it is acceptable.

    Args:
        file_name: file name to be checked.

    Returns: error string if invalid; or empty string if valid

    """
    pass


def validate_file_string(file: str) -> str:
    """Returns the file string if it is valid."""
    pass


def validate_sp_string(sp_string) -> str:
    pass
