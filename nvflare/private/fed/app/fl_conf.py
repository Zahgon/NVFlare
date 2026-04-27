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

"""FL Server / Client startup configure."""

import os
import re
import sys

from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import ConnectionSecurity, ConnPropKey, FilterKey, SiteType, SystemConfigs
from nvflare.apis.workspace import Workspace
from nvflare.fuel.data_event.utils import set_scope_property
from nvflare.fuel.f3.cellnet.fqcn import FQCN
from nvflare.fuel.utils.argument_utils import parse_vars
from nvflare.fuel.utils.config_service import ConfigService
from nvflare.fuel.utils.json_scanner import Node
from nvflare.fuel.utils.url_utils import make_url
from nvflare.fuel.utils.wfconf import ConfigContext, ConfigError
from nvflare.private.defs import SSLConstants
from nvflare.private.json_configer import JsonConfigurator
from nvflare.private.privacy_manager import PrivacyManager, Scope

from .deployer.base_client_deployer import BaseClientDeployer
from .deployer.server_deployer import ServerDeployer
from .fl_app_validator import FLAppValidator

FL_PACKAGES = ["nvflare"]
FL_MODULES = ["server", "client", "app_common", "private"]


class FLServerStarterConfiger(JsonConfigurator):
    """FL Server startup configure."""

    def __init__(self, workspace: Workspace, args, kv_list=None):
        """Init the FLServerStarterConfiger.

        Args:
            workspace: the workspace object
            kv_list: key value pair list
        """
        site_custom_folder = workspace.get_site_custom_dir()
        if os.path.isdir(site_custom_folder) and site_custom_folder not in sys.path:
            sys.path.append(site_custom_folder)

        self.args = args

        base_pkgs = FL_PACKAGES
        module_names = FL_MODULES

        if kv_list:
            assert isinstance(kv_list, list), "cmd_vars must be list, but got {}".format(type(kv_list))
            self.cmd_vars = parse_vars(kv_list)
        else:
            self.cmd_vars = {}

        config_files = workspace.get_config_files_for_startup(is_server=True, for_job=True if args.job_id else False)

        JsonConfigurator.__init__(
            self,
            config_file_name=config_files,
            base_pkgs=base_pkgs,
            module_names=module_names,
            exclude_libs=True,
        )

        self.components = {}  # id => component
        self.handlers = []

        self.workspace = workspace
        self.server_config_file_names = config_files

        self.deployer = None
        self.app_validator = None
        self.snapshot_persistor = None
        self.overseer_agent = None
        self.site_org = ""

    def start_config(self, config_ctx: ConfigContext):
        """Start the config process.

        Args:
            config_ctx: config context

        """
        pass

    def build_component(self, config_dict):
        pass

    def process_config_element(self, config_ctx: ConfigContext, node: Node):
        """Process the config element.

        Args:
            config_ctx: config context
            node: element node

        """
        pass

    def finalize_config(self, config_ctx: ConfigContext):
        """Finalize the config process.

        Args:
            config_ctx: config context

        """
        pass


class FLClientStarterConfiger(JsonConfigurator):
    """FL Client startup configure."""

    def __init__(self, workspace: Workspace, args, kv_list=None):
        """Init the FLClientStarterConfiger.

        Args:
            workspace: the workspace object
            kv_list: key value pair list
        """
        site_custom_folder = workspace.get_site_custom_dir()
        if os.path.isdir(site_custom_folder) and site_custom_folder not in sys.path:
            sys.path.append(site_custom_folder)

        self.args = args

        base_pkgs = FL_PACKAGES
        module_names = FL_MODULES

        if kv_list:
            assert isinstance(kv_list, list), "cmd_vars must be list, but got {}".format(type(kv_list))
            self.cmd_vars = parse_vars(kv_list)
        else:
            self.cmd_vars = {}

        config_files = workspace.get_config_files_for_startup(is_server=False, for_job=True if args.job_id else False)

        JsonConfigurator.__init__(
            self,
            config_file_name=config_files,
            base_pkgs=base_pkgs,
            module_names=module_names,
            exclude_libs=True,
        )

        self.components = {}  # id => component
        self.handlers = []

        self.workspace = workspace
        self.client_config_file_names = config_files
        self.base_deployer = None
        self.overseer_agent = None
        self.site_org = ""
        self.app_validator = None

    def process_config_element(self, config_ctx: ConfigContext, node: Node):
        """Process config element.

        Args:
            config_ctx: config context
            node: element node
        """
        pass

    def build_component(self, config_dict):
        pass

    def _determine_conn_props(self, client_name, config_data: dict):
        pass

    def start_config(self, config_ctx: ConfigContext):
        """Start the config process.

        Args:
            config_ctx: config context
        """
        pass

    def finalize_config(self, config_ctx: ConfigContext):
        """Finalize the config process.

        Args:
            config_ctx: config context
        """
        pass


class PrivacyConfiger(JsonConfigurator):
    def __init__(self, workspace: Workspace, names_only: bool, is_server=False):
        """Uses the json configuration to start the FL admin client.

        Args:
            workspace: the workspace object
        """
        self.privacy_manager = None
        self.scopes = []
        self.default_scope_name = None
        self.components = {}
        self.current_scope = None
        self.names_only = names_only
        self.is_server = is_server

        privacy_file_path = workspace.get_site_privacy_file_path()
        JsonConfigurator.__init__(
            self,
            config_file_name=privacy_file_path,
            base_pkgs=FL_PACKAGES,
            module_names=FL_MODULES,
            exclude_libs=True,
        )

    def process_config_element(self, config_ctx: ConfigContext, node: Node):
        """Process config element.

        Args:
            config_ctx: config context
            node: element node
        """
        pass

    def finalize_config(self, config_ctx: ConfigContext):
        pass


def create_privacy_manager(workspace: Workspace, names_only: bool, is_server=False):
    pass
