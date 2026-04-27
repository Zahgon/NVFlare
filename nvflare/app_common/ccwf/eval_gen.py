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
from enum import Enum
from typing import List

from nvflare.fuel.utils.validation_utils import check_non_negative_int


class EvalInclusionRC(Enum):
    CAN_INCLUDE = 0
    EVALUATOR_CONFLICT = 1
    ENOUGH_ACTIONS_FOR_EVALUATEE = 2
    ENOUGH_ACTIONS_FOR_EVALUATOR = 3


def _check_names(arg_name, names_to_check):
    pass


def parallel_eval_generator(evaluators: List[str], evaluatees: List[str], max_parallel_actions: int):
    """Generates parallel evaluations to be performed.

    Args:
        evaluators: names of evaluators
        evaluatees: names of evaluatees
        max_parallel_actions: max parallel actions per site (evaluator or evaluatee)

    Each time iterated, it generates a list of evaluations that can be performed in parallel.
    An evaluation is expressed as a tuple of (evaluator name, evaluatee name).
    """
    pass


def _can_be_included(evals, target, max_parallel_actions) -> EvalInclusionRC:
    """Determine whether the target evaluation can be included into the set of evals without violating
    parallel evaluation rules.

    Args:
        evals: the set of evaluations already included
        target: the evaluation in question, expressed as a tuple (evaluator name, evaluatee name)
        max_parallel_actions: max parallel actions allowed per actor (evaluator or evaluatee).

    Returns: an EvalInclusionRC

    """
    pass
