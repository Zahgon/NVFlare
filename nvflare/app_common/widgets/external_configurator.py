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

import os
from typing import List

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_constant import ConnPropKey, FLMetaKey
from nvflare.apis.fl_context import FLContext
from nvflare.app_common.utils.export_utils import update_export_props
from nvflare.client.config import write_config_to_file
from nvflare.client.constants import CLIENT_API_CONFIG
from nvflare.fuel.utils.attributes_exportable import ExportMode, export_components
from nvflare.fuel.utils.validation_utils import check_object_type
from nvflare.widgets.widget import Widget


class ExternalConfigurator(Widget):
    def __init__(
        self,
        component_ids: List[str],
        config_file_name: str = CLIENT_API_CONFIG,
    ):
        """Prepares any external configuration files.

        Args:
            component_ids: A list of components that are `AttributesExportable`
            config_file_name: The file name of the external config.
        """
        super().__init__()
        check_object_type("component_ids", component_ids, list)

        # the components that needs to export attributes
        self._component_ids = component_ids
        self._config_file_name = config_file_name

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def _get_external_config_file_path(self, fl_ctx: FLContext):
        pass

    def _export_all_components(self, fl_ctx: FLContext) -> dict:
        """Exports all components."""
        pass
