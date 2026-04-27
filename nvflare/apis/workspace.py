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

import glob
import os
from typing import List, Union

from nvflare.apis.fl_constant import WorkspaceConstants


class Workspace:
    def __init__(self, root_dir: str, site_name: str = "", config_folder: str = "config"):
        """Define a workspace.

        NOTE::

            Example of client workspace folder structure:

                Workspace ROOT
                    local
                        authorization.json.default
                        resources.json.default
                        custom/
                            custom python code
                        ...
                    startup (optional)
                        provisioned content
                        fed_client.json
                    run_1
                        app
                            config (required)
                                configurations
                            custom (optional)
                                custom python code
                            other_folder (app defined)
                        log.txt
                        job_meta.json
                        ...

        Args:
            root_dir: root directory of the workspace
            site_name: site name of the workspace
            config_folder: where to find required config inside an app
        """
        self.root_dir = root_dir
        self.site_name = site_name
        self.config_folder = config_folder

        # check to make sure the workspace is valid
        if not os.path.isdir(root_dir):
            raise ValueError(f"invalid workspace {root_dir}: it does not exist or not a valid dir")

        startup_dir = self.get_startup_kit_dir()
        if not os.path.isdir(startup_dir):
            raise RuntimeError(
                f"invalid workspace {root_dir}: missing startup folder '{startup_dir}' or not a valid dir"
            )

        site_dir = self.get_site_config_dir()
        if not os.path.isdir(site_dir):
            raise RuntimeError(
                f"invalid workspace {root_dir}: missing site config folder '{site_dir}' or not a valid dir"
            )

        # check env vars for other roots (Result, Log, Audit)
        self.result_root = self._setup_root(WorkspaceConstants.ENV_VAR_RESULT_ROOT)
        self.audit_root = self._setup_root(WorkspaceConstants.ENV_VAR_AUDIT_ROOT)
        self.log_root = self._setup_root(WorkspaceConstants.ENV_VAR_LOG_ROOT)

        # determine defaults
        if not self.log_root:
            if self.audit_root:
                # if audit root is defined, use it for logging too since they are all for output only
                self.log_root = self.audit_root
            else:
                # otherwise we use the result root
                self.log_root = self.result_root

        if not self.audit_root:
            if self.log_root:
                # if log root is defined, use it for auditing too since they are all for output only
                self.audit_root = self.log_root
            else:
                # otherwise we use the result root
                self.audit_root = self.result_root

    def _setup_root(self, env_var: str):
        pass

    def _fallback_path(self, file_names: [str]):
        pass

    def get_authorization_file_path(self):
        pass

    def get_resources_file_path(self):
        pass

    def get_job_resources_file_path(self):
        pass

    def get_log_config_file_path(self):
        pass

    def get_file_path_in_site_config(self, file_basename: Union[str, List[str]]):
        pass

    def get_file_path_in_startup(self, file_basename: str):
        pass

    def get_file_path_in_root(self, file_basename: str):
        pass

    def get_server_startup_file_path(self):
        # this is to get the full path to "fed_server.json"
        pass

    def get_server_app_config_file_path(self, job_id):
        pass

    def get_client_app_config_file_path(self, job_id):
        pass

    def get_client_startup_file_path(self):
        # this is to get the full path to "fed_client.json"
        pass

    def get_admin_startup_file_path(self):
        # this is to get the full path to "fed_admin.json"
        pass

    def get_site_config_dir(self) -> str:
        pass

    def get_site_custom_dir(self) -> str:
        pass

    def get_startup_kit_dir(self) -> str:
        pass

    def get_audit_root(self, job_id=None) -> str:
        pass

    def get_audit_file_path(self, job_id=None) -> str:
        pass

    def _get_site_root_dir(self, root, job_id=None):
        pass

    def get_log_root(self, job_id=None) -> str:
        pass

    def get_root_dir(self) -> str:
        pass

    def get_run_dir(self, job_id: str) -> str:
        pass

    def get_app_dir(self, job_id: str) -> str:
        pass

    def _get_any_app_log_file_path(self, job_id: str, file_name: str):
        pass

    def get_app_error_log_file_path(self, job_id: str) -> str:
        pass

    def get_app_config_dir(self, job_id: str) -> str:
        pass

    def get_app_custom_dir(self, job_id: str) -> str:
        pass

    def get_job_meta_path(self, job_id: str) -> str:
        pass

    def get_site_privacy_file_path(self):
        pass

    def get_client_custom_dir(self) -> str:
        pass

    def get_stats_pool_summary_path(self, job_id: str, prefix=None) -> str:
        pass

    def get_stats_pool_records_path(self, job_id: str, prefix=None) -> str:
        pass

    def get_result_root(self, job_id: str):
        pass

    def get_config_files_for_startup(self, is_server: bool, for_job: bool) -> list:
        """Get all config files to be used for startup of the process (SP, SJ, CP, CJ).

        We first get required config files:
            - the startup file (fed_server.json or fed_client.json) in "startup" folder
            - resource file (resources.json.default or resources.json) in "local" folder

        We then try to get resources files (usually generated by different builders of the Provision system):
            - resources files from the "startup" folder take precedence
            - resources files from the "local" folder are next

        These extra resource config files must be json and follow the following patterns:
        - *__resources.json: these files are for both parent process and job processes
        - *__p_resources.json: these files are for parent process only
        - *__j_resources.json: these files are for job process only

        Args:
            is_server: whether this is for server site or client site
            for_job: whether this is for job process or parent process

        Returns: a list of config file names

        """
        pass

    @staticmethod
    def _add_resource_files(from_dir: str, to_list: list, patterns: [str]):
        pass
