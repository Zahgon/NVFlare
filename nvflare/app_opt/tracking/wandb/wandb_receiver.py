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
import time
from multiprocessing import Process, Queue
from typing import List, NamedTuple, Optional

import wandb

from nvflare.apis.analytix import AnalyticsData, AnalyticsDataType, LogWriterName
from nvflare.apis.dxo import from_shareable
from nvflare.apis.fl_constant import ProcessType
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.widgets.streaming import AnalyticsReceiver


class WandBTask(NamedTuple):
    task_owner: str
    task_type: str
    task_data: dict
    step: int


def _check_wandb_args(wandb_args):
    pass


def _get_job_id_tag(fl_ctx: FLContext) -> str:
    """Gets a unique job id tag."""
    pass


class WandBReceiver(AnalyticsReceiver):
    def __init__(
        self, wandb_args: dict, mode: str = "offline", events: Optional[List[str]] = None, process_timeout: float = 10.0
    ):
        super().__init__(events=events)
        self.fl_ctx = None
        self.mode = mode
        self.wandb_args = wandb_args
        self.queues = {}
        self.processes = {}
        self.metrics_buffer = {}
        self.process_timeout = process_timeout

        # os.environ["WANDB_API_KEY"] = YOUR_KEY_HERE
        os.environ["WANDB_MODE"] = self.mode

    def _process_queue_tasks(self, queue):
        pass

    def initialize(self, fl_ctx: FLContext):
        # Determine participating sites
        pass

    def save(self, fl_ctx: FLContext, shareable: Shareable, record_origin: str):
        pass

    def finalize(self, fl_ctx: FLContext):
        """Called at EventType.END_RUN.

        Args:
            fl_ctx (FLContext): the FLContext
        """
        pass

    def get_task_queue(self, record_origin):
        pass
