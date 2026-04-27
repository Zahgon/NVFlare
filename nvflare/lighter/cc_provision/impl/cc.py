# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
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

import os
from typing import Any, Dict, Optional, Type

from nvflare.app_opt.confidential_computing.cc_manager import CC_ISSUER_ID, TOKEN_EXPIRATION
from nvflare.lighter import utils
from nvflare.lighter.constants import PropKey, TemplateSectionKey
from nvflare.lighter.ctx import ProvisionContext
from nvflare.lighter.entity import Participant, Project
from nvflare.lighter.spec import Builder

from ..cc_constants import CC_AUTHORIZERS_KEY, CCConfigKey, CCConfigValue, CCIssuerConfig, CCManagerArgs
from .azure import AzureSimpleBuilder
from .onprem_cvm import OnPremCVMBuilder

CC_MGR_PATH = "nvflare.app_opt.confidential_computing.cc_manager.CCManager"


# (deploy_env, CPU_CC_MECHANISM, GPU_CC_MECHANISM)
VALID_COMPUTE_ENVS = [
    CCConfigValue.ONPREM_CVM,
    CCConfigValue.AZURE_CONFIDENTIAL_CONTAINER,
    CCConfigValue.AZURE_CVM,
    CCConfigValue.MOCK,
]


BUILDER_CLASSES = {
    CCConfigValue.ONPREM_CVM: OnPremCVMBuilder,
    CCConfigValue.AZURE_CVM: AzureSimpleBuilder,
    CCConfigValue.AZURE_CONFIDENTIAL_CONTAINER: AzureSimpleBuilder,
    CCConfigValue.MOCK: OnPremCVMBuilder,
}


class CCBuilder(Builder):
    """Builder that coordinates different CC implementations (AzureCVM, OnPremCVM, etc.).

    Each CC implementation builder handles all participants that use its implementation.
    This builder also sets up the CCManager component for each participant.
    """

    def __init__(
        self,
        cc_mgr_id="cc_manager",
    ):
        self.project_name: Optional[str] = None
        self.project: Optional[Project] = None
        self.cc_config: Optional[Dict[str, Any]] = None
        # CC Manager specific
        self._cc_mgr_id = cc_mgr_id
        self._cc_enabled_sites = []
        # Map of compute environment to its builder class
        self._cc_builders: Dict[str, Type[Builder]] = {}

    def _load_and_validate_cc_config(self, config_path):
        """Load CC configuration from YAML file."""
        pass

    def _enable_participant_for_cc(self, participant, cc_config, ctx):
        pass

    def _create_builder_for_env(self, cc_config):
        pass

    def initialize(self, project: Project, ctx: ProvisionContext):
        """Initialize all CC builders needed for the project."""
        pass

    def _build_cc_manager_component(self, participant: Participant, ctx: ProvisionContext):
        """Build CCManager component for a participant."""
        pass

    def build(self, project: Project, ctx: ProvisionContext):
        """Build CC configuration for all participants."""
        pass

    def finalize(self, project: Project, ctx: ProvisionContext):
        """Finalize all CC builders."""
        pass
