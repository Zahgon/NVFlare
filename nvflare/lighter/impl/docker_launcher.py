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

from nvflare.app_opt.job_launcher.docker_launcher import ClientDockerJobLauncher, ServerDockerJobLauncher
from nvflare.lighter import utils
from nvflare.lighter.constants import CommConfigArg, CtxKey, PropKey, ProvFileName, TemplateSectionKey
from nvflare.lighter.entity import Participant
from nvflare.lighter.spec import Builder, Project, ProvisionContext


class DockerLauncherBuilder(Builder):
    """Generates start_docker.sh per site and injects DockerJobLauncher into resources.json.

    The site admin is responsible for building the Docker image before deployment.
    This builder only needs the image name to embed in start_docker.sh.

    Usage in project.yml:
        - path: nvflare.lighter.impl.docker_launcher.DockerLauncherBuilder
          args:
            docker_image: my-nvflare-image:latest

    Each participant that has ``run_in_docker: true`` in its props will get a
    ``startup/start_docker.sh`` generated alongside the standard ``startup/start.sh``.
    Running start_docker.sh starts the SP/CP container in Docker mode; job containers
    (SJ/CJ) are then launched automatically by DockerJobLauncher when jobs are submitted.
    """

    def __init__(self, docker_image: str = "nvflare:latest"):
        """
        Args:
            docker_image: Docker image name for SP/CP containers. The site admin must
                          build and tag this image before running start_docker.sh.
                          Job images (SJ/CJ) are specified per job in meta.json.
        """
        self.docker_image = docker_image

    def _inject_launcher(self, dest_dir: str, path: str, args: dict):
        """Replace any existing job launcher component with DockerJobLauncher."""
        pass

    def _set_internal_listener_host(self, participant: Participant):
        """Override internal listener host to 0.0.0.0 so SJ/CJ containers on the Docker network can connect."""
        pass

    def _build_server(self, server: Participant, ctx: ProvisionContext):
        pass

    def _build_client(self, client: Participant, ctx: ProvisionContext):
        pass

    def initialize(self, project: Project, ctx: ProvisionContext):
        pass

    def build(self, project: Project, ctx: ProvisionContext):
        pass
