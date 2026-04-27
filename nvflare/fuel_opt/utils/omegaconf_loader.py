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
from typing import Dict, Optional

from nvflare.fuel.utils.config import Config, ConfigFormat, ConfigLoader


class OmegaConfConfig(Config):
    def __init__(self, conf, file_path: Optional[str] = None):
        super(OmegaConfConfig, self).__init__(conf, ConfigFormat.OMEGACONF, file_path)

    def to_dict(self, resolve: Optional[bool] = True) -> Dict:
        pass

    def to_str(self, element: Optional[Dict] = None) -> str:
        pass


class OmegaConfLoader(ConfigLoader):
    def __init__(self):
        super(OmegaConfLoader, self).__init__(ConfigFormat.OMEGACONF)

    def load_config(self, file_path: str) -> Config:
        pass

    def load_config_from_str(self, config_str: str) -> Config:
        pass

    def load_config_from_dict(self, config_dict: dict) -> Config:
        pass

    def _from_file(self, file_path):
        pass
