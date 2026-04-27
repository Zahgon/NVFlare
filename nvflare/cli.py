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

import argparse
import json
import os
import sys
import traceback

from pyhocon import ConfigFactory as CF

from nvflare.cli_exception import CLIException
from nvflare.cli_unknown_cmd_exception import CLIUnknownCmdException
from nvflare.dashboard.cli import define_dashboard_parser, handle_dashboard
from nvflare.fuel.flare_api.api_spec import AuthenticationError, AuthorizationError, NoConnection
from nvflare.fuel.hci.tools.authz_preview import define_authz_preview_parser, run_command
from nvflare.lighter.provision import define_provision_parser, handle_provision
from nvflare.private.fed.app.simulator.simulator import define_simulator_parser, run_simulator
from nvflare.private.fed.app.utils import version_check
from nvflare.tool.cert.cert_cli import def_cert_cli_parser, handle_cert_cmd
from nvflare.tool.job.job_cli import def_job_cli_parser, handle_job_cli_cmd
from nvflare.tool.package.package_cli import def_package_cli_parser, handle_package_cmd
from nvflare.tool.poc.poc_commands import def_poc_parser, handle_poc_cmd
from nvflare.tool.preflight_check import check_packages, define_preflight_check_parser
from nvflare.tool.recipe.recipe_cli import def_recipe_parser, handle_recipe_cmd
from nvflare.tool.study.study_cli import def_study_cli_parser, handle_study_cmd
from nvflare.tool.system.system_cli import def_system_cli_parser, handle_system_cmd
from nvflare.utils.cli_utils import (
    TARGET_POC,
    TARGET_PROD,
    backup_hidden_config_file,
    create_job_template_config,
    create_poc_workspace_config,
    create_startup_kit_config,
    ensure_hidden_config_migrated,
    load_hidden_config_state,
    print_hidden_config_migration_notice,
    save_config,
)

CMD_POC = "poc"
CMD_PROVISION = "provision"
CMD_PREFLIGHT_CHECK = "preflight-check"
CMD_SIMULATOR = "simulator"
CMD_DASHBOARD = "dashboard"
CMD_AUTHZ_PREVIEW = "authz-preview"
CMD_JOB = "job"
CMD_RECIPE = "recipe"
CMD_CONFIG = "config"
CMD_CERT = "cert"
CMD_PACKAGE = "package"
CMD_SYSTEM = "system"
CMD_STUDY = "study"


def def_provision_parser(sub_cmd):
    pass


def def_dashboard_parser(sub_cmd):
    pass


def def_preflight_check_parser(sub_cmd):
    pass


def def_simulator_parser(sub_cmd):
    pass


def handle_simulator_cmd(simulator_args):
    pass


def def_authz_preview_parser(sub_cmd):
    pass


def handle_authz_preview(args):
    pass


_config_parser = None


def def_config_parser(sub_cmd):
    pass


def handle_config_cmd(args):
    pass


def _get_subcommand_choices(parser):
    pass


def _emit_argparse_error_json(parser, message):
    pass


def _emit_argparse_error_human(parser, message, exit_code: int = 4):
    pass


def _patch_help_on_error(parser, json_mode: bool = False):
    """Recursively patch every parser in the tree to print help before error-exit.

    When argparse detects a missing required argument it calls parser.error(),
    which prints a terse usage line and exits 2.  By wrapping error() we ensure
    the full help is printed first so users see the complete syntax.
    """
    def _error_with_help(message):
        pass
    pass


def _build_global_arg_parser():
    pass


def _normalize_global_args(argv, global_parser):
    """Move supported global options ahead of the subcommand without parsing them.

    This keeps argparse as the single source of truth while preserving the CLI's
    existing behavior of accepting global flags after the subcommand.
    """
    pass


def parse_args(prog_name: str):
    pass


handlers = {
    CMD_POC: handle_poc_cmd,
    CMD_PROVISION: handle_provision,
    CMD_PREFLIGHT_CHECK: check_packages,
    CMD_SIMULATOR: handle_simulator_cmd,
    CMD_DASHBOARD: handle_dashboard,
    CMD_AUTHZ_PREVIEW: handle_authz_preview,
    CMD_JOB: handle_job_cli_cmd,
    CMD_RECIPE: handle_recipe_cmd,
    CMD_CONFIG: handle_config_cmd,
    CMD_CERT: handle_cert_cmd,
    CMD_PACKAGE: handle_package_cmd,
    CMD_STUDY: handle_study_cmd,
    CMD_SYSTEM: handle_system_cmd,
}


def _auth_hint_from_detail(detail: str, auth_code: str = None) -> str:
    pass


def run(prog_name):
    pass


def _suppress_cli_connector_noise():
    """Reduce noisy connector retry logs for CLI invocations only."""
    pass


def print_nvflare_version():
    pass


def main():
    pass


if __name__ == "__main__":
    main()
