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

import re

from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import SiteType, SystemConfigs, SystemVarName
from nvflare.apis.impl.controller import Controller
from nvflare.apis.impl.wf_comm_server import WFCommServer
from nvflare.apis.workspace import Workspace
from nvflare.fuel.utils.argument_utils import parse_vars
from nvflare.fuel.utils.config_service import ConfigService
from nvflare.fuel.utils.json_scanner import Node
from nvflare.private.fed_json_config import FedJsonConfigurator
from nvflare.private.json_configer import ConfigContext, ConfigError

from .server_runner import ServerRunnerConfig

FL_PACKAGES = ["nvflare"]
FL_MODULES = ["apis", "app_common", "widgets"]


class WorkFlow:
    def __init__(self, id, controller: Controller):
        """Workflow is a controller with ID.

        Setting communicator to WFCommServer for server-side workflow.

        Args:
            id: identification
            controller (Controller): A controller
        """
        self.id = id
        self.controller = controller


class ServerJsonConfigurator(FedJsonConfigurator):
    def __init__(
        self, workspace_obj: Workspace, config_file_name: str, args, app_root: str, kv_list=None, exclude_libs=True
    ):
        """This class parses server config from json file.

        Args:
            config_file_name (str): json file to parse
            exclude_libs (bool): whether to exclude libs
        """
        self.config_file_name = config_file_name
        self.args = args
        self.app_root = app_root

        base_pkgs = FL_PACKAGES
        module_names = FL_MODULES

        if kv_list:
            assert isinstance(kv_list, list), "cmd_vars must be list, but got {}".format(type(kv_list))
            self.cmd_vars = parse_vars(kv_list)
        else:
            self.cmd_vars = {}

        sys_vars = {
            SystemVarName.JOB_ID: args.job_id,
            SystemVarName.SITE_NAME: SiteType.SERVER,
            SystemVarName.WORKSPACE: args.workspace,
            SystemVarName.SECURE_MODE: self.cmd_vars.get("secure_train", True),
            SystemVarName.JOB_CUSTOM_DIR: workspace_obj.get_app_custom_dir(args.job_id),
        }

        FedJsonConfigurator.__init__(
            self,
            config_file_name=config_file_name,
            base_pkgs=base_pkgs,
            module_names=module_names,
            exclude_libs=exclude_libs,
            is_server=True,
            sys_vars=sys_vars,
        )

        if kv_list:
            assert isinstance(kv_list, list), "cmd_vars must be list, but got {}".format(type(kv_list))
            self.cmd_vars = parse_vars(kv_list)
        else:
            self.cmd_vars = {}
        self.config_files = [config_file_name]

        self.runner_config = None

        # if server doesn't hear heartbeat from client for this long, we'll consider the client dead
        self.heartbeat_timeout = 60  # default to 1 minute

        # server will ask client to come back for next task after this many secs
        self.task_request_interval = 2  # default to 2 secs

        # workflows to be executed
        self.workflows = []

    def process_config_element(self, config_ctx: ConfigContext, node: Node):
        pass

    def _get_all_workflows_ids(self):
        pass

    def build_component(self, config_dict):
        pass

    def finalize_config(self, config_ctx: ConfigContext):
        pass
