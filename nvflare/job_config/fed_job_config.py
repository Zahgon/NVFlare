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
import builtins
import inspect
import json
import os
import shlex
import shutil
import subprocess
import sys
from enum import Enum
from tempfile import TemporaryDirectory
from typing import Dict, List

from nvflare.fuel.utils.class_utils import get_component_init_parameters
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.fuel.utils.validation_utils import check_object_type
from nvflare.job_config.base_app_config import BaseAppConfig
from nvflare.job_config.fed_app_config import FedAppConfig
from nvflare.private.fed.app.fl_conf import FL_PACKAGES
from nvflare.private.fed.app.utils import kill_child_processes

CONFIG = "config"
CUSTOM = "custom"
FED_SERVER_JSON = "config_fed_server.json"
FED_CLIENT_JSON = "config_fed_client.json"
META_JSON = "meta.json"


class FedJobConfig:
    """FedJobConfig represents the job in the NVFlare."""

    def __init__(self, job_name, min_clients, mandatory_clients=None, meta_props=None) -> None:
        """FedJobConfig uses the job_name,  min_clients and optional mandatory_clients to create the object.
        It also provides the method to add in the FedApp, the deployment map of the FedApp and participants,
        and the resource _spec requirements of the participants if needed.

        Args:
            job_name: the name of the NVFlare job
            min_clients: the minimum number of clients for the job
            mandatory_clients: mandatory clients to run the job (optional)
            meta_props: additional meta properties for the job (optional)
        """
        super().__init__()

        if meta_props:
            check_object_type("meta_props", meta_props, dict)

        self.job_name = job_name
        self.min_clients = min_clients
        self.mandatory_clients = mandatory_clients
        self.meta_props = meta_props
        self.app_packages = []

        self.fed_apps: Dict[str, FedAppConfig] = {}
        self.deploy_map: Dict[str, str] = {}
        self.resource_specs: Dict[str, Dict] = {}

        self.custom_modules = []
        self.logger = get_obj_logger(self)

    def set_app_packages(self, app_packages: List[str]):
        """Set app packages.
        When generating job config, code from these packages will not be included into "custom" folder.

        Args:
            app_packages: app packages

        Returns: None

        """
        pass

    def add_fed_app(self, app_name: str, fed_app: FedAppConfig):
        pass

    def set_site_app(self, site_name: str, app_name: str):
        """assign an app to a certain site.

        Args:
            site_name: The target site name.
            app_name: The app name.

        Returns:

        """
        pass

    def add_resource_spec(self, site_name: str, resource_spec: Dict):
        pass

    def _generate_meta(self, job_dir):
        """generate the job meta.json

        Returns:

        """
        pass

    def generate_job_config(self, job_root):
        """generate the job config

        Returns:

        """
        pass

    def simulator_run(self, workspace, clients=None, n_clients=None, threads=None, gpu=None, log_config=None):
        pass

    def _get_server_app(self, config_dir, custom_dir, fed_app):
        pass

    def _copy_file_sources(self, config_dir, custom_dir, file_sources):
        pass

    def _copy_ext_scripts(self, custom_dir, ext_scripts):
        pass

    def _copy_ext_dirs(self, custom_dir, app_config: BaseAppConfig):
        pass

    def _get_relative_script(self, script):
        pass

    def _get_class_path(self, obj, custom_dir):
        pass

    def _get_custom_file(self, custom_dir, module, source_file):
        pass

    def _copy_source_file(self, custom_dir, module, source_file, dest_file):
        pass

    def _get_client_app(self, config_dir, custom_dir, fed_app):
        pass

    def _get_base_app(self, custom_dir, app, app_config):
        pass

    def _process_filters(self, taskset_filters: list, custom_dir):
        """Process taskset_filters into app filter configuration

        Args:
            taskset_filters: the list of tuples that contain taskset/filters association.
            custom_dir: custom dir of the app.

        Returns: app filter configuration that is a list of dicts, each dict represents a taskset/filters
            association.

        """
        pass

    def _values_differ(self, default_val, attr_val):
        """Check if attribute value differs from default. Returns True if they differ."""
        pass

    def _get_args(self, component, custom_dir):
        pass

    def _get_filters(self, filters, custom_dir):
        pass

    def locate_imports(self, sf, dest_file):
        """Locate all the import statements from the python script, including the imports across multiple lines,
        using the line break continuing.

        Args:
            sf: source file
            dest_file: copy to destination file

        Returns:
            yield all the imports within the source file

        """
        pass

    def _get_deploy_map(self):
        pass

    def _trim_whitespace(self, string: str):
        pass

    @staticmethod
    def _is_valid_job_folder(job_folder: str) -> bool:
        pass

    def _is_partial_export_folder(self, job_folder: str) -> bool:
        """True when a previous export created the directory but did not finish writing meta.json.

        A partial export only contains app-named subdirectories (no foreign files), so it is
        safe to delete and retry.  Any other content means the folder was not created by NVFlare.
        """
        pass
