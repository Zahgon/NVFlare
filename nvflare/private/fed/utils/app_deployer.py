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

import json
import os
import shutil

from nvflare.apis.app_deployer_spec import AppDeployerSpec
from nvflare.apis.fl_context import FLContext
from nvflare.apis.job_def import JobMetaKey
from nvflare.apis.workspace import Workspace
from nvflare.fuel.utils.zip_utils import unzip_all_from_bytes
from nvflare.private.privacy_manager import PrivacyService
from nvflare.security.logging import secure_format_exception

from .app_authz import AppAuthzService


class AppDeployer(AppDeployerSpec):
    def deploy(
        self, workspace: Workspace, job_id: str, job_meta: dict, app_name: str, app_data: bytes, fl_ctx: FLContext
    ) -> str:
        """Deploys the app.

        Returns:
            error message if any
        """
        pass
