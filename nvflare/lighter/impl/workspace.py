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

import os
import shutil

from nvflare.lighter.constants import CtxKey
from nvflare.lighter.spec import Builder, Project, ProvisionContext
from nvflare.lighter.utils import make_dirs


class WorkspaceBuilder(Builder):
    def __init__(self, template_file=None):
        """Manages the folder structure for provisioned projects.

        Sets the template_file containing scripts and configs to put into startup folders, creates directories for the
        participants, and moves the provisioned project to the final location at the end
        ($WORKSPACE/$PROJECT_NAME/prod_XX). WorkspaceBuilder manages and sets the number in prod_XX by incrementing from
        the last time provision was run for this project in this workspace, starting with 00 to a max of 99.

        Each time the provisioning tool runs, it requires a workspace folder in the local file system.  The workspace
        will have the following folder structure:

        .. code-block:: text

          $WORKSPACE/    <--- this is assigned by -w option of provision command (default is workspace)
            $PROJECT_NAME/  <--- this is the name value in the project.yml file
              prod_00/   <--- a new prod_NN folder is created if provision does not have any errors.
              prod_01/
              ...
              resources/ <--- this folder stores resources for other builders to load
              state/     <--- this folder stores persistent information (such as certificates) so subsequent runs of the provision command can load the state back.
              wip/  <--- this is only used during runtime, and will be removed when the provision command exits

        Args:
            template_file: one or more template file names
        """
        self.template_files = template_file  # obsolete

    def initialize(self, project: Project, ctx: ProvisionContext):
        # be backward compatible: load template files if specified.
        pass

    def build(self, project: Project, ctx: ProvisionContext):
        pass

    def finalize(self, project: Project, ctx: ProvisionContext):
        pass
