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

from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.storage import StorageException
from nvflare.app_common.abstract.statistics_writer import StatisticsWriter
from nvflare.app_common.utils.json_utils import ObjectEncoder
from nvflare.fuel.utils.class_loader import load_class


class JsonStatsFileWriter(StatisticsWriter):
    def __init__(self, output_path: str, json_encoder_path: str = ""):
        super().__init__()
        self.job_dir = None
        if len(output_path) == 0:
            raise ValueError(f"output_path {output_path} is empty string")

        self.output_path = output_path
        if json_encoder_path == "":
            self.json_encoder_class = ObjectEncoder
        else:
            self.json_encoder_path = json_encoder_path
            self.json_encoder_class = load_class(json_encoder_path)

    def save(
        self,
        data: dict,
        overwrite_existing,
        fl_ctx: FLContext,
    ):

        pass

    def get_output_path(self, fl_ctx: FLContext) -> str:
        pass

    def _validate_directory(self, full_path: str):
        pass
