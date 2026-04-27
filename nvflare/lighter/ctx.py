# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
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
import sys
from typing import List, Optional, Union

import yaml

import nvflare.lighter as prov
from nvflare.lighter import utils
from nvflare.lighter.utils import load_yaml

from .constants import CtxKey, PropKey, ProvisionMode
from .entity import Entity, Project


class ProvisionContext(dict):
    def __init__(self, workspace_root_dir: str, project: Project):
        super().__init__()
        self[CtxKey.WORKSPACE] = workspace_root_dir

        wip_dir = os.path.join(workspace_root_dir, "wip")
        state_dir = os.path.join(workspace_root_dir, "state")
        self.update({CtxKey.WIP: wip_dir, CtxKey.STATE: state_dir})
        dirs = [workspace_root_dir, wip_dir, state_dir]
        utils.make_dirs(dirs)

        # set commonly used data into ctx
        self[CtxKey.PROJECT] = project

        server = project.get_server()
        fed_learn_port = server.get_prop(PropKey.FED_LEARN_PORT, 8002)
        admin_port = server.get_prop(PropKey.ADMIN_PORT, fed_learn_port)
        self[CtxKey.ADMIN_PORT] = admin_port
        self[CtxKey.FED_LEARN_PORT] = fed_learn_port
        self[CtxKey.SERVER_NAME] = server.name
        self[CtxKey.TEMP_FILES_LOADED] = []
        self[CtxKey.TEMPLATE] = {}
        self[CtxKey.ERRORS] = []
        self[CtxKey.WARNINGS] = []

    def get_project(self) -> Project:
        pass

    def load_templates(self, temp_files: Union[str, List[str]]):
        pass

    def get_template_section(self, section_key: str):
        pass

    def set_provision_mode(self, mode: str):
        pass

    def get_provision_mode(self):
        pass

    def set_logger(self, logger):
        pass

    def get_logger(self):
        pass

    def get_wip_dir(self):
        pass

    def get_ws_dir(self, entity: Entity):
        pass

    def get_kit_dir(self, entity: Entity):
        pass

    def get_transfer_dir(self, entity: Entity):
        pass

    def get_local_dir(self, entity: Entity):
        pass

    def get_state_dir(self):
        pass

    def get_workspace(self):
        pass

    def get_errors(self) -> List[str]:
        pass

    def get_warnings(self) -> List[str]:
        pass

    def yaml_load_template_section(self, section_key: str, replacement=None):
        pass

    def json_load_template_section(self, section_key: str, replacement=None):
        pass

    def build_from_template(
        self,
        dest_dir: str,
        temp_section: Union[str, List[str]],
        file_name,
        replacement=None,
        mode="t",
        exe=False,
        content_modify_cb=None,
        **cb_kwargs,
    ):
        """Build a file from a template section and writes it to the specified location.

        Args:
            dest_dir: destination directory
            temp_section: template section key
            file_name: file name
            replacement: replacement dict
            mode: file mode
            exe: executable
            content_modify_cb: content modification callback. If specified, it takes the section content as the
                first argument and returns the modified content
            cb_kwargs: additional keyword arguments for the callback

        """
        pass

    def build_section_from_template(
        self,
        temp_section: Union[str, List[str]],
        replacement=None,
        content_modify_cb=None,
        **cb_kwargs,
    ):
        pass

    def info(self, msg: str):
        pass

    def error(self, msg: str):
        pass

    def debug(self, msg: str):
        pass

    def warning(self, msg: str):
        pass

    def get_result_location(self) -> Optional[str]:
        """Get the directory of the provision result.
        This should be called after the provision is done.

        Returns: the name of the directory that holds the provisioned result.

        """
        pass
