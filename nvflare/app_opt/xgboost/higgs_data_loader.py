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

import json

import pandas as pd
import xgboost as xgb

from nvflare.app_opt.xgboost.data_loader import XGBDataLoader


def _read_higgs_with_pandas(data_path, start: int, end: int):
    pass


class HIGGSDataLoader(XGBDataLoader):
    def __init__(self, data_split_filename):
        """Reads HIGGS dataset and return XGB data matrix.

        Args:
            data_split_filename: file name to data splits
        """
        self.data_split_filename = data_split_filename

    def load_data(self):
        pass
