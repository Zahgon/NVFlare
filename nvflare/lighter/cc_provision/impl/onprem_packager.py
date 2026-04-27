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
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import yaml

from nvflare.lighter.constants import ProvFileName
from nvflare.lighter.ctx import ProvisionContext
from nvflare.lighter.entity import Participant, Project
from nvflare.lighter.spec import Packager

BUILD_IMAGE_CMD = "build_cvm_image.sh"


def _extract_cvm_tar_path(output):
    pass


def _extract_docker_tar_path(output):
    pass


def to_abs_path(yaml_path, file_path):
    """Converts a relative file path to an absolute path based on the directory of the given YAML file.

    Args:
        yaml_path (str): Path to the YAML file. Must be a non-empty string.
        file_path (str): Target file path. If relative, it's resolved against the YAML file's directory.

    Returns:
        str: An absolute file path.

    Raises:
        RuntimeError: If either input is None or empty.
    """
    pass


def run_command(command, cwd=None):
    pass


class OnPremPackager(Packager):
    def __init__(self, cc_config_key="cc_config", build_image_cmd=BUILD_IMAGE_CMD):
        super().__init__()
        self.cc_config_key = cc_config_key
        self.build_image_cmd = build_image_cmd

    def _build_cc_image(self, cc_config_yaml: str):
        """Build CC image for the site."""
        pass

    def _add_startup_kit_to_cc_config(self, cc_config_path: str, startup_kit_path: str):
        pass

    def _package_for_participant(self, participant: Participant, ctx: ProvisionContext):
        """Package the startup kit for the participant."""
        pass

    def package(self, project: Project, ctx: ProvisionContext):
        pass
