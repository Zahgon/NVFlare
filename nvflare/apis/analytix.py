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

from enum import Enum

from nvflare.apis.dxo import DXO, DataKind

ANALYTIC_EVENT_TYPE = "analytix_log_stats"


class LogWriterName(Enum):
    TORCH_TB = "TORCH_TENSORBOARD"
    MLFLOW = "MLFLOW"
    WANDB = "WEIGHTS_AND_BIASES"


class TrackConst(object):
    TRACKER_KEY = "tracker_key"

    TRACK_KEY = "track_key"
    TRACK_VALUE = "track_value"

    TAG_KEY = "tag_key"
    TAGS_KEY = "tags_key"

    EXP_TAGS_KEY = "tags_key"

    GLOBAL_STEP_KEY = "global_step"
    PATH_KEY = "path"
    DATA_TYPE_KEY = "analytics_data_type"
    KWARGS_KEY = "analytics_kwargs"

    PROJECT_NAME = "project_name"
    PROJECT_TAGS = "project_name"

    EXPERIMENT_NAME = "experiment_name"
    RUN_NAME = "run_name"
    EXPERIMENT_TAGS = "experiment_tags"
    INIT_CONFIG = "init_config"
    RUN_TAGS = "run_tags"

    SITE_KEY = "site"
    JOB_ID_KEY = "job_id"


class AnalyticsDataType(Enum):
    SCALARS = "SCALARS"
    SCALAR = "SCALAR"
    IMAGE = "IMAGE"
    TEXT = "TEXT"
    LOG_RECORD = "LOG_RECORD"

    PARAMETER = "PARAMETER"
    PARAMETERS = "PARAMETERS"
    METRIC = "METRIC"
    METRICS = "METRICS"
    MODEL = "MODEL"

    #     # MLFLOW ONLY
    TAG = "TAG"
    TAGS = "TAGS"
    INIT_DATA = "INIT_DATA"


class AnalyticsData:
    def __init__(
        self,
        key: str,
        value,
        data_type: AnalyticsDataType,
        sender: LogWriterName = LogWriterName.TORCH_TB,
        **kwargs,
    ):
        """This class defines AnalyticsData format.

        It is a wrapper to provide to/from DXO conversion.

        Args:
            key (str): tag name
            value: value
            data_type (AnalyticDataType): type of the analytic data.
            sender (LogWriterName): Type of sender for syntax such as Tensorboard or MLflow
            kwargs (optional, dict): additional arguments to be passed.
        """
        self._validate_data_types(data_type, key, value, **kwargs)
        self.tag = key
        self.value = value
        self.data_type = data_type
        self.kwargs = kwargs
        self.sender = sender
        self.step = kwargs.get(TrackConst.GLOBAL_STEP_KEY, None)
        self.path = kwargs.get(TrackConst.PATH_KEY, None)

    def to_dxo(self):
        """Converts the AnalyticsData to DXO object.

        Returns:
            DXO object
        """
        pass

    @classmethod
    def from_dxo(cls, dxo: DXO, receiver: LogWriterName = LogWriterName.TORCH_TB):
        """Generates the AnalyticsData from DXO object.

        Args:
            receiver: type of the experiment tacker, defaults to Tensorboard with LogWriterName.TORCH_TB.
            dxo (DXO): The DXO object to convert.

        Returns:
            AnalyticsData object
        """
        pass

    def _validate_data_types(
        self,
        data_type: AnalyticsDataType,
        key: str,
        value: any,
        **kwargs,
    ):
        pass

    @classmethod
    def convert_data_type(
        cls, sender_data_type: AnalyticsDataType, sender: LogWriterName, receiver: LogWriterName
    ) -> AnalyticsDataType:

        pass

    def __str__(self) -> str:
        return f"AnalyticsData(tag: {self.tag}, value: {self.value}, data_type: {self.data_type}, kwargs: {self.kwargs}, step: {self.step})"
