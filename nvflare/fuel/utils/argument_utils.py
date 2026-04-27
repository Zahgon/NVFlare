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

_true_set = {"yes", "true", "t", "y", "1"}
_false_set = {"no", "false", "f", "n", "0"}


def str2bool(value, raise_exc=False):
    pass


def parse_var(s):
    """Parse string variable into key-value tuple.

    Returns (key, value) tuple from string with equals sign with the portion before the first equals sign as the key
    and the rest as the value.

    Args:
        s: string to parse

    Returns: Tuple of key and value
    """
    pass


def parse_vars(items):
    """Converts a list of key value pairs into a dictionary.

    Args:
        items: list like ['a=1', 'b=2', 'c=3']

    Returns: dictionary like {'a': '1', 'b': '2', 'c': '3'}

    """
    pass


class SafeArgumentParser(argparse.ArgumentParser):
    """Safe version of ArgumentParser which doesn't exit on error"""

    def __init__(self, **kwargs):
        kwargs["add_help"] = False
        super().__init__(**kwargs)

    def error(self, message):
        pass
