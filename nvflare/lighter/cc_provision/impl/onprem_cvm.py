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

import json
import os

from nvflare.lighter import utils
from nvflare.lighter.cc_provision.cc_constants import CC_AUTHORIZERS_KEY
from nvflare.lighter.constants import PropKey, ProvFileName
from nvflare.lighter.ctx import ProvisionContext
from nvflare.lighter.entity import Entity, Project
from nvflare.lighter.spec import Builder


def _update_log_filenames(config, new_log_root: str = "/applog"):
    pass


def _change_log_dir(log_config_path: str):
    pass


class OnPremCVMBuilder(Builder):
    """Builder for On-premises Confidential Computing VMs."""

    def initialize(self, project: Project, ctx: ProvisionContext):
        """Initialize the configurator.

        Args:
            project: The project to configure
            ctx: The provisioning context
        """
        pass

    def build(self, project: Project, ctx: ProvisionContext):
        """Build CVM configuration for all participants."""
        pass

    def _build_resources(self, entity: Entity, ctx: ProvisionContext):
        """Build resources for the entity."""
        pass
