# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
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
import copy
import logging
import os
import sys

from nvflare.apis.fl_constant import FLContextKey, SystemVarName
from nvflare.apis.job_def import JobMetaKey
from nvflare.apis.job_launcher_spec import JobProcessArgs


def _job_args_str(job_args, arg_names) -> str:
    pass


def get_client_job_args(include_exe_module=True, include_set_options=True):
    pass


def generate_client_command(fl_ctx) -> str:
    pass


def get_server_job_args(include_exe_module=True, include_set_options=True):
    pass


def generate_server_command(fl_ctx) -> str:
    pass


_LAUNCHER_MODE_KEYS = {"process", "docker", "k8s"}


def get_site_launcher_spec(site_spec, mode):
    """Extract the launcher-mode portion of a single site's resource spec.

    New nested format: ``{mode: {...}}`` — returns the inner dict for *mode*.
    Legacy flat format: ``{num_of_gpus: ...}`` — treated as process mode for
    backward compatibility; Docker and K8s modes receive an empty spec.
    """
    pass


def get_launcher_resource_spec(job_meta, site_name, mode):
    """Extract the launcher-mode resource spec for a site from full job meta."""
    pass


_LAUNCHER_SPEC_DEFAULT_KEY = "default"

# "default" is the only reserved top-level key in launcher_spec. Every other
# top-level key is treated as a site name. A typo such as "defaults" would be
# silently accepted as a site name and never matched during resolution.
_LAUNCHER_SPEC_RESERVED_KEYS = {_LAUNCHER_SPEC_DEFAULT_KEY}


def _validate_launcher_spec(launcher_spec: dict) -> list:
    """Return top-level keys that look like misspellings of a reserved token.

    Reserved keys (_LAUNCHER_SPEC_RESERVED_KEYS) are skipped. All other keys
    are treated as site names. A key whose sub-keys are all valid launcher modes
    but whose name closely resembles a reserved token is flagged so callers can
    warn the user before resolution silently ignores it.
    """
    pass


def get_job_launcher_spec(job_meta, site_name, mode):
    """Get launcher-specific config for a site/mode.

    Resolution order:
    1. Merge launcher_spec["default"][mode] with launcher_spec[site][mode] (site wins).
    2. Fall back to get_launcher_resource_spec (nested resource_spec backward compat) when
       neither launcher_spec["default"][mode] nor launcher_spec[site][mode] is present —
       even if launcher_spec exists for other sites or modes.

    Returns a dict for the given mode, or an empty dict if not specified.
    """
    pass


def add_custom_dir_to_path(app_custom_folder, new_env):
    """Util method to add app_custom_folder into the sys.path and carry into the child process."""
    pass
