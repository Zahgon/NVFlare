# Copyright (c) 2023, NVIDIA CORPORATION.  All rights reserved.
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
import shutil

from nvflare.apis.app_deployer_spec import AppDeployerSpec, FLContext
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import SystemComponents, SystemVarName
from nvflare.apis.job_def import JobMetaKey
from nvflare.apis.job_def_manager_spec import JobDefManagerSpec
from nvflare.apis.utils.job_utils import load_job_def_bytes
from nvflare.apis.workspace import Workspace
from nvflare.fuel.utils.dict_utils import update_components
from nvflare.lighter.tool_consts import NVFLARE_SIG_FILE
from nvflare.lighter.utils import verify_folder_signature
from nvflare.private.fed.utils.fed_utils import require_signed_jobs


class HubAppDeployer(AppDeployerSpec, FLComponent):

    HUB_CLIENT_CONFIG_TEMPLATE_NAME = "hub_client.json"
    OLD_HUB_CLIENT_CONFIG_TEMPLATE_NAME = "t1_config_fed_client.json"
    HUB_SERVER_CONFIG_TEMPLATE_NAME = "hub_server.json"
    OLD_HUB_SERVER_CONFIG_TEMPLATE_NAME = "t2_server_components.json"

    HUB_CLIENT_CONFIG_TEMPLATES = [HUB_CLIENT_CONFIG_TEMPLATE_NAME, OLD_HUB_CLIENT_CONFIG_TEMPLATE_NAME]
    HUB_SERVER_CONFIG_TEMPLATES = [HUB_SERVER_CONFIG_TEMPLATE_NAME, OLD_HUB_SERVER_CONFIG_TEMPLATE_NAME]

    def __init__(self):
        FLComponent.__init__(self)

    def prepare(
        self, fl_ctx: FLContext, workspace: Workspace, job_id: str, remove_tmp_t2_dir: bool = True
    ) -> (str, dict, bytes):
        """
        Prepare T2 job

        Args:
            fl_ctx:
            workspace:
            job_id:
            remove_tmp_t2_dir:

        Returns: error str if any, meta dict, and job bytes to be submitted to T2 store

        """
        pass

    def deploy(
        self, workspace: Workspace, job_id: str, job_meta: dict, app_name: str, app_data: bytes, fl_ctx: FLContext
    ) -> str:
        # step 1: deploy the T1 app into the workspace
        pass
