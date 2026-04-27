# Copyright (c) 2021-2026, NVIDIA CORPORATION.  All rights reserved.
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
import json
import logging
import os
import pkgutil
import subprocess
import sys
import warnings
from typing import List, Optional, Union

from nvflare.apis.app_validation import AppValidator
from nvflare.apis.client import Client
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_component import FLContext
from nvflare.apis.fl_constant import ConfigVarName, FLContextKey, FLMetaKey, JobConstants, SiteType, WorkspaceConstants
from nvflare.apis.fl_exception import UnsafeComponentError
from nvflare.apis.job_def import JobMetaKey
from nvflare.apis.job_launcher_spec import JobLauncherSpec
from nvflare.apis.utils.decomposers import flare_decomposers
from nvflare.apis.workspace import Workspace
from nvflare.app_common.decomposers import common_decomposers
from nvflare.fuel.f3.stats_pool import CsvRecordHandler, StatsPoolManager
from nvflare.fuel.sec.audit import AuditService
from nvflare.fuel.sec.authz import AuthorizationService
from nvflare.fuel.sec.security_content_service import LoadResult, SecurityContentService
from nvflare.fuel.utils import fobs
from nvflare.fuel.utils.fobs.fobs import register_custom_folder
from nvflare.private.defs import RequestHeader, SSLConstants
from nvflare.private.event import fire_event
from nvflare.private.fed.utils.decomposers import private_decomposers
from nvflare.private.privacy_manager import PrivacyManager, PrivacyService
from nvflare.security.logging import secure_format_exception
from nvflare.security.security import EmptyAuthorizer, FLAuthorizer
from nvflare.security.study_registry import StudyRegistry, StudyRegistryService

from ..simulator.simulator_const import SimulatorConstants
from .app_authz import AppAuthzService

# Distributed provisioning produces startup kits whose certs are signed by a site-local CA
# rather than the project CA.  The server therefore cannot verify __nvfl_sig.json using its
# own CA chain, so require_signed_jobs() lets an operator opt out of signature enforcement
# via fed_server.json.  _warn_once suppresses repeated log noise for the same condition.
_SIGNED_JOB_WARNINGS_EMITTED = set()


def _warn_once(logger: logging.Logger, cache_key: str, message: str, *args) -> None:
    # Suppress duplicate warnings emitted on every job submission (e.g. TOCTOU advisory).
    pass


def require_signed_jobs(workspace: Workspace) -> bool:
    """Return True if the server requires all submitted jobs to carry __nvfl_sig.json.

    In distributed provisioning each site generates its own private key and gets a cert
    signed by the project CA, but the server's startup kit was provisioned independently
    and may not share the same CA chain used to sign __nvfl_sig.json.  Operators who use
    distributed provisioning can set ``require_signed_jobs: false`` in fed_server.json to
    disable signature enforcement without restarting the server (hot-reload).

    Default: True when rootCA.pem is present (any PKI deployment); False otherwise.
    Explicit "require_signed_jobs" key in fed_server.json overrides the inferred default.
    """
    pass


def _check_secure_content(site_type: str) -> List[str]:
    """To check the security contents.

    Args:
        site_type (str): "server" or "client"

    Returns:
        A list of insecure content.
    """
    pass


def security_init(secure_train: bool, site_org: str, workspace: Workspace, app_validator: AppValidator, site_type: str):
    """To check the security content if running in security mode.

    Args:
       secure_train (bool): if run in secure mode or not.
       site_org: organization of the site
       workspace: the workspace object.
       app_validator: app validator for application validation
       site_type (str): server or client. fed_client.json or fed_server.json
    """
    pass


def security_init_for_job(secure_train: bool, workspace: Workspace, site_type: str, job_id: str):
    """Initialize security processing for a job process (SJ or CJ).

    Args:
       secure_train (bool): if run in secure mode or not.
       workspace: the workspace object.
       site_type (str): server or client. fed_client.json or fed_server.json
    """
    pass


def security_close():
    pass


def get_job_meta_from_workspace(workspace: Workspace, job_id: str) -> dict:
    pass


def create_job_processing_context_properties(workspace: Workspace, job_id: str) -> dict:
    pass


def find_char_positions(s, ch):
    pass


def get_scope_info():
    pass


def fobs_initialize(workspace: Workspace = None, job_id: Optional[str] = None):
    pass


def custom_fobs_initialize(workspace: Workspace = None, job_id: Optional[str] = None):
    pass


def nvflare_fobs_initialize():
    pass


def register_ext_decomposers(decomposer_module: Union[str, List[str]]):
    pass


def register_decomposer_module(decomposer_module):
    pass


def set_stats_pool_config_for_job(workspace: Workspace, job_id: str, prefix=None):
    pass


def create_stats_pool_files_for_job(workspace: Workspace, job_id: str, prefix=None):
    pass


def split_gpus(gpus) -> [str]:
    pass


def authorize_build_component(config_dict, config_ctx, node, fl_ctx: FLContext, event_handlers) -> str:
    pass


def set_message_security_data(request, job, fl_ctx):
    pass


def get_target_names(targets):
    # validate targets
    pass


def get_return_code(job_handle, job_id, workspace, logger):
    pass


def get_simulator_app_root(simulator_root, site_name):
    pass


def extract_participants(participants_list):
    """Extract participant site names from deploy_map forms.

    Supported forms include:
      - ["server", "site-1"]
      - ["@ALL"]
      - {"targets": ["server", "site-1"]}
      - {"sites": ["server", "site-1"]}
      - [{"sites": ["site-1"]}, "site-2"]
      - [{"targets": ["site-1"]}, "site-2"]
    """
    pass


def get_job_launcher(job_meta: dict, fl_ctx: FLContext) -> JobLauncherSpec:
    pass


def execute_command_directly(args: List[str]) -> str:
    """Execute a command directly, without using shell"""
    pass
