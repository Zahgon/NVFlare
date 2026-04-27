# Copyright (c) 2026, NVIDIA CORPORATION.  All rights reserved.
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

import importlib
import inspect
import pkgutil
import sys

from nvflare.tool.cli_output import output_usage_error

_RECIPE_PACKAGE_ROOTS = [
    {"package": "nvflare.recipe", "framework": "core"},
    {"package": "nvflare.app_opt.pt.recipes", "framework": "pytorch"},
    {"package": "nvflare.app_opt.tf.recipes", "framework": "tensorflow"},
    {"package": "nvflare.app_opt.sklearn.recipes", "framework": "sklearn"},
    {"package": "nvflare.app_opt.xgboost.recipes", "framework": "xgboost"},
]


def _framework_install_hint(framework: str = None) -> list[str]:
    pass


def _framework_install_hint_text(framework: str = None) -> str:
    pass


def _recipe_cli_name(module_name: str, framework: str) -> str:
    pass


def _recipe_description(recipe_cls) -> str:
    pass


def _iter_recipe_classes(module):
    pass


def _select_recipe_class(module):
    """Select the single CLI-exposed recipe class for a module.

    Recipe discovery is module-oriented: the CLI name comes from the module name, so a
    module contributes at most one catalog entry. If a module defines both a reusable base
    recipe and a concrete subclass, prefer the leaf subclass.
    """
    pass


def _load_catalog(framework: str = None) -> list:
    """Return available recipes, filtered by framework if given.

    Recipes whose optional dependencies are not installed are silently skipped.
    """
    pass


def cmd_recipe_list(cmd_args):
    pass


_recipe_parser = None
_recipe_root_parser = None


def def_recipe_parser(sub_cmd):
    pass


def handle_recipe_cmd(args):
    pass
