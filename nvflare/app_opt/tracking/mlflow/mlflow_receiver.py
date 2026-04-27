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
import timeit
from typing import Dict, List, Optional

import mlflow
from mlflow.entities import Metric, Param, RunTag
from mlflow.tracking.client import MlflowClient

from nvflare.apis.analytix import ANALYTIC_EVENT_TYPE, AnalyticsData, AnalyticsDataType, LogWriterName, TrackConst
from nvflare.apis.dxo import from_shareable
from nvflare.apis.fl_constant import ProcessType, ReservedKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.job_def import JobMetaKey
from nvflare.apis.shareable import Shareable
from nvflare.app_common.widgets.streaming import AnalyticsReceiver

DEFAULT_RUN_NAME = "FLARE FL Run"


class MlflowConstants:
    EXPERIMENT_TAG = "experiment_tag"
    RUN_TAG = "run_tag"
    EXPERIMENT_NAME = "experiment_name"


def get_current_time_millis():
    pass


def _get_job_name_from_fl_ctx(fl_ctx: FLContext, default=None):
    # TODO: it might be good to have a function in fl_context to get the job name
    pass


class MLflowReceiver(AnalyticsReceiver):
    def __init__(
        self,
        tracking_uri: Optional[str] = None,
        kw_args: Optional[dict] = None,
        artifact_location: Optional[str] = None,
        events: Optional[List[str]] = None,
        buffer_flush_time=1,
    ):
        """MLflowReceiver receives log events from clients and deliver them to the MLflow tracking server.

        Args:
            tracking_uri (Optional[str], optional): MLflow tracking server URI. When this is not specified, the metrics will be written to the local file system.
                If the tracking URI is specified, the MLflow tracking server must started before running the job. Defaults to None.
            kw_args (Optional[dict], optional): keyword arguments:
                "experiment_name" (str): Specifies the experiment name. If not specified, the default name of "FLARE FL Experiment" will be used.
                "run_name" (str): Specifies the run name
                "experiment_tags" (dict): Tags used when creating the MLflow experiment.
                "mlflow.note.content" is a special MLflow tag. When provided, it displays as experiment
                description field on the MLflow UI. You can use Markdown syntax for the description.
                "run_tags" (str): Tags used when creating the MLflow run. "mlflow.note.content" is a special MLflow tag.
                When provided, it displays as run description field on the MLflow UI.
                You can use Markdown syntax for the description.
            artifact_location (Optional[str], optional): Relative location of artifacts. Currently only text is supported at the moment.
            events (optional, List[str]): A list of event that this receiver will handle.
            buffer_flush_time (int, optional): The time in seconds between deliveries of event data to the MLflow tracking server. The
                data is buffered and then delivered to the MLflow tracking server in batches, and
                the buffer_flush_time controls the frequency of the sending. By default, the buffer
                flushes every second. You can reduce the time to a fraction of a second if you prefer
                less delay. Keep in mind that reducing the buffer_flush_time will potentially cause high
                traffic to the MLflow tracking server, which in some cases can actually cause more latency.
        """
        if not isinstance(tracking_uri, (str, type(None))):
            raise ValueError("tracking_uri needs to be either None or str")
        if events is None:
            events = ["fed." + ANALYTIC_EVENT_TYPE]
        super().__init__(events=events)
        self.artifact_location = artifact_location if artifact_location is not None else "artifacts"

        self.kw_args = kw_args if kw_args else {}
        self.tracking_uri = tracking_uri
        self.mlflow_clients: Dict[str, MlflowClient] = {}
        self.experiment_id = None
        self.run_ids = {}
        self.buffer = {}
        self.time_start = 0
        self.time_since_flush = 0
        self.buff_flush_time = buffer_flush_time

    def _get_tracking_uri(self, fl_ctx: FLContext):
        pass

    def initialize(self, fl_ctx: FLContext):
        """Initializes MlflowClient for each site.

        This method:
        1. Sets up the FL context and timing
        2. Validates and prepares experiment configuration
        3. Determines participating sites
        4. Sets up MLflow clients and experiments for each site
        5. Initializes data buffers

        Args:
            fl_ctx (FLContext): The FLContext containing runtime information

        Raises:
            ValueError: If experiment name is empty
            RuntimeError: If unable to determine participating sites
        """
        pass

    def _mlflow_setup(self, art_full_path, experiment_name, experiment_tags, site_names: List[str], fl_ctx: FLContext):
        """Set up an MlflowClient for each receiving site and create an experiment and run.

        Args:
            art_full_path (str): Full path to artifacts.
            experiment_name (str): Experiment name.
            experiment_tags (dict): Experiment tags.
            sites (List[str]): List of sites.
            fl_ctx (FLContext): An FLContext.
        """
        pass

    def _init_buffer(self, site_names: List[str]):
        """For each site, create a buffer (dict) consisting of a list each for metrics, parameters, and tags."""
        pass

    def _get_run_name(self, kwargs: dict, site_name: str, job_id_tag: str, job_name: str):
        pass

    def _get_run_tags(self, kwargs, job_id_tag: str, run_name: str):
        pass

    def _get_job_id_tag(self, fl_ctx: FLContext) -> str:
        """Gets a unique job id tag."""
        pass

    def _get_tags(self, tag_key: str, kwargs: dict):
        pass

    def _get_artifact_location(self, relative_path: str, fl_ctx: FLContext):
        pass

    def _get_or_create_experiment(
        self,
        mlflow_client: MlflowClient,
        experiment_name: str,
        artifact_location: str,
        experiment_tags: Optional[dict] = None,
    ) -> Optional[str]:
        pass

    def save(self, fl_ctx: FLContext, shareable: Shareable, record_origin: str):
        pass

    def buffer_data(self, data: AnalyticsData, record_origin: str) -> None:
        """Buffer the data to send later.

        A buffer for each data_type is in each site_buffer, all of which are in self.buffer

        Args:
            data (AnalyticsData): Data.
            record_origin (str): Origin of the data, or site name.
        """
        pass

    def get_target_type(self, data_type: AnalyticsDataType):
        pass

    def flush_buffers(self, record_origin):
        """Flush buffers and send all the data to the MLflow tracking server.

        Args:
            record_origin (str): Origin of the data, or site name.
        """
        pass

    def flush_buffer(self, log_buffer: List):
        pass

    def finalize(self, fl_ctx: FLContext):
        pass

    def get_run_id(self, site_id: str) -> Optional[str]:
        pass

    def get_mlflow_client(self, site_id: str) -> MlflowClient:
        pass
