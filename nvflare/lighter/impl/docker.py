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

import copy
import os
import shutil

import yaml

from nvflare.lighter.constants import CtxKey, ProvFileName, TemplateSectionKey
from nvflare.lighter.spec import Builder, Project, ProvisionContext


class DockerBuilder(Builder):
    def __init__(self, base_image="python:3.10", requirements_file="requirements.txt"):
        """Build docker file."""
        self.base_image = base_image
        self.requirements_file = requirements_file
        self.services = {}
        self.compose_file_path = None

    def _build_overseer(self, overseer):
        pass

    def _build_server(self, server, ctx: ProvisionContext):
        pass

    def _build_client(self, client):
        pass

    def build(self, project: Project, ctx: ProvisionContext):
        pass
