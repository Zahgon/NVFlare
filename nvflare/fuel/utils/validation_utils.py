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

import random

SYMBOL_ALL = "@all"
SYMBOL_NONE = "@none"


class DefaultValuePolicy:
    """
    Defines policy for how to determine default value
    """

    DISALLOW = "disallow"
    ANY = "any"
    RANDOM = "random"
    EMPTY = "empty"
    ALL = "all"

    @classmethod
    def valid_policy(cls, p: str):
        pass


def check_positive_int(name, value):
    pass


def check_non_negative_int(name, value):
    pass


def check_positive_number(name, value):
    pass


def check_number_range(name, value, min_value=None, max_value=None):
    pass


def check_non_negative_number(name, value):
    pass


def check_str(name, value):
    pass


def check_non_empty_str(name, value):
    pass


def check_object_type(name, value, obj_type):
    pass


def check_callable(name, value):
    pass


def _determine_candidates_value(var_name: str, candidates, base: list):
    pass


def validate_candidates(var_name: str, candidates, base: list, default_policy: str, allow_none: bool):
    """Validate specified candidates against the items in the "base" list, based on specified policy
    and returns determined value for the candidates.

    The value of candidates could have the following cases:
    1. Not explicitly specified (Python object None or empty list [])
    In this case, the default_policy decides the final result:
    - ANY: returns a list that contains a single item from the base
    - RANDOM: returns a list that contains a random item from the base
    - EMPTY: returns an empty list
    - ALL: returns the base list
    - DISALLOW: raise exception - candidates must be explicitly specified

    2. A list of string items
    In this case, each item in the candidates list must be in the "base". Duplicates are removed.

    3. A string with special value "@all" to mean "all items from the base"
    Returns the base list.

    4. A string with special value "@none" to mean "no items"
    If allow_none is True, then returns an empty list; otherwise raise exception.

    5. A string that is not a special value
    If it is in the "base", return a list that contains this item; otherwise raise exception.

    Args:
        var_name: the name of the "candidates" var from the caller
        candidates: the candidates to be validated
        base: the base list that contains valid items
        default_policy: policy for how to handle default value when "candidates" is not explicitly specified.
        allow_none: whether "none" is allowed for candidates.

    Returns:

    """
    pass


def _determine_candidate_value(var_name: str, candidate, base: list):
    pass


def validate_candidate(var_name: str, candidate, base: list, default_policy: str, allow_none: bool):
    """Validate specified candidate against the items in the "base" list, based on specified policy
    and returns determined value for the candidate.

    The value of candidate could have the following cases:
    1. Not explicitly specified (Python object None or empty string)
    In this case, the default_policy decides the final result:
    - ANY: returns the first item from the base
    - RANDOM: returns a random item from the base
    - EMPTY: returns an empty str
    - ALL or DISALLOW: raise exception - candidate must be explicitly specified

    2. A string with special value "@none" to mean "nothing"
    If allow_none is True, then returns an empty str; otherwise raise exception.

    3. A string that is not a special value
    If it is in the "base", return it; otherwise raise exception.

    All other cases, raise exception.

    NOTE: the final value is normalized (leading and trailing white spaces are removed).

    Args:
        var_name: the name of the "candidate" var from the caller
        candidate: the candidate to be validated
        base: the base list that contains valid items
        default_policy: policy for how to handle default value when "candidates" is not explicitly specified.
        allow_none: whether "none" is allowed for candidates.

    Returns:

    """
    pass


def normalize_config_arg(value):
    pass
