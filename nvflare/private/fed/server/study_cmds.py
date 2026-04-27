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

import json
import os
import tempfile
from copy import deepcopy
from typing import Dict, List

from nvflare.apis.client import ClientPropKey
from nvflare.apis.fl_constant import AdminCommandNames
from nvflare.apis.job_def import JobMetaKey
from nvflare.apis.job_def_manager_spec import JobDefManagerSpec
from nvflare.apis.utils.format_check import name_check
from nvflare.fuel.hci.conn import Connection
from nvflare.fuel.hci.proto import ConfirmMethod, MetaStatusValue, make_meta
from nvflare.fuel.hci.reg import CommandModule, CommandModuleSpec, CommandSpec
from nvflare.fuel.hci.server.authz import PreAuthzReturnCode
from nvflare.fuel.hci.server.constants import ConnProps
from nvflare.fuel.utils.argument_utils import SafeArgumentParser
from nvflare.private.fed.server.server_engine import ServerEngine
from nvflare.security.study_registry import StudyRegistry, StudyRegistryService

from .cmd_utils import CommandUtil

_LOCK_TIMEOUT_SECS = 30.0


class _InvalidArgsError(ValueError):
    pass


class _InvalidSiteError(ValueError):
    pass


class _InvalidStudyNameError(ValueError):
    pass


def _study_parser(
    cmd_name: str,
    include_sites: bool = False,
    include_site_org: bool = False,
    include_user: bool = False,
):
    pass


class StudyCommandModule(CommandModule, CommandUtil):
    def get_spec(self):
        pass

    def authorize_study_admin(self, conn: Connection, args: List[str]):
        pass

    @staticmethod
    def _reply(conn: Connection, payload: dict):
        pass

    def _error(self, conn: Connection, error_code: str, message: str, hint: str = "", exit_code: int = 1):
        pass

    @staticmethod
    def _parse_sites(sites_arg: str) -> List[str]:
        pass

    @staticmethod
    def _parse_site_orgs(site_org_args: List[str]) -> Dict[str, List[str]]:
        pass

    def _validate_study_name(self, study: str):
        pass

    def _validate_site_names(self, sites: List[str]):
        pass

    def _validate_site_orgs(self, site_orgs: Dict[str, List[str]]):
        pass

    @staticmethod
    def _study_payload(study: str, study_def: dict):
        pass

    @staticmethod
    def _registry_path(engine: ServerEngine) -> str:
        pass

    @staticmethod
    def _load_registry_config(path: str) -> dict:
        pass

    @staticmethod
    def _write_registry_config(path: str, config: dict):
        pass

    @staticmethod
    def _caller_name(conn: Connection) -> str:
        pass

    @staticmethod
    def _caller_role(conn: Connection) -> str:
        pass

    @staticmethod
    def _caller_org(conn: Connection) -> str:
        pass

    @staticmethod
    def _validate_sites_for_org(engine: ServerEngine, sites: List[str], expected_org: str) -> List[str]:
        """Returns sites that are unknown to the server or whose cert org does not match expected_org."""
        pass

    def _is_visible_to_caller(self, conn: Connection, study_def: dict) -> bool:
        pass

    @staticmethod
    def _normalize_admins(study_def: dict) -> List[str]:
        pass

    @staticmethod
    def _normalize_site_orgs(study_def: dict) -> Dict[str, List[str]]:
        pass

    def _requested_site_orgs(self, conn: Connection, parsed) -> Dict[str, List[str]]:
        pass

    def _site_mutation_payload(
        self, study: str, study_def: dict, added=None, already_enrolled=None, removed=None, not_enrolled=None
    ):
        pass

    def _with_mutation(self, conn: Connection, mutation_cb):
        pass

    def _study_not_found(self, conn: Connection, study: str):
        pass

    def cmd_register_study(self, conn: Connection, args: List[str]):
        def _mutate(_engine, working):
            pass
        pass

    def cmd_add_study_site(self, conn: Connection, args: List[str]):
        def _mutate(_engine, working):
            pass
        pass

    def cmd_remove_study_site(self, conn: Connection, args: List[str]):
        def _mutate(_engine, working):
            pass
        pass

    def cmd_remove_study(self, conn: Connection, args: List[str]):
        def _mutate(engine, working):
            pass
        pass

    def cmd_list_studies(self, conn: Connection, args: List[str]):
        pass

    def cmd_show_study(self, conn: Connection, args: List[str]):
        pass

    def cmd_add_study_user(self, conn: Connection, args: List[str]):
        def _mutate(_engine, working):
            pass
        pass

    def cmd_remove_study_user(self, conn: Connection, args: List[str]):
        def _mutate(_engine, working):
            pass
        pass
