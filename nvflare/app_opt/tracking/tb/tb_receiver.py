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
from typing import List, Optional

from nvflare.apis.analytix import AnalyticsData, AnalyticsDataType
from nvflare.apis.dxo import from_shareable
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.widgets.streaming import AnalyticsReceiver
from nvflare.app_opt.tracking.tb.tb_event_writer import TensorBoardEventWriter

FUNCTION_MAPPING = {
    AnalyticsDataType.SCALAR: "add_scalar",
    AnalyticsDataType.TEXT: "add_text",
    AnalyticsDataType.IMAGE: "add_image",
    AnalyticsDataType.SCALARS: "add_scalars",
    AnalyticsDataType.METRIC: "add_scalar",
    AnalyticsDataType.METRICS: "add_scalars",
}


def _create_new_data(key, value, sender):
    pass


class TBAnalyticsReceiver(AnalyticsReceiver):
    def __init__(self, tb_folder="tb_events", events: Optional[List[str]] = None):
        """Receives analytics data to save to TensorBoard.

        Args:
            tb_folder (str): the folder to store tensorboard files.
            events (optional, List[str]): A list of events to be handled by this receiver.

        .. code-block:: text
            :caption: Folder structure

              - site_workspace
                - job_id1 (already created):
                  - output_dir (default: tb_events):
                    - peer_name_1:
                    - peer_name_2:

                - job_id2 (already created):
                  - output_dir (default: tb_events):
                    - peer_name_1:
                    - peer_name_2:

        """
        super().__init__(events=events)
        self.writers_table = {}
        self.tb_folder = tb_folder
        self.root_log_dir = None

    def initialize(self, fl_ctx: FLContext):
        pass

    def _convert_to_records(self, analytic_data: AnalyticsData, fl_ctx: FLContext) -> List[AnalyticsData]:
        # break dict of stuff to smaller items to support
        # AnalyticsDataType.PARAMETER and AnalyticsDataType.PARAMETERS
        pass

    def save(self, fl_ctx: FLContext, shareable: Shareable, record_origin):
        pass

    def finalize(self, fl_ctx: FLContext):
        pass
