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

import os
from typing import Dict, List, Union

import numpy as np

from nvflare.apis.dxo import DXO, DataKind
from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.app_common.abstract.model_locator import ModelLocator
from nvflare.security.logging import secure_format_exception

from .constants import NPConstants


class NPModelLocator(ModelLocator):
    SERVER_MODEL_NAME = "server"

    def __init__(self, model_dir="models", model_name: Union[str, Dict[str, str]] = "server.npy"):
        """The ModelLocator's job is to find the models to be included for cross site evaluation
        located on server. This NPModelLocator finds and extracts "server" model that is saved during training.

        Args:
            model_dir (str): Directory to look for models in. Defaults to "models".
                Only used when model_name contains relative paths.
            model_name (Union[str, Dict[str, str]]): Name or path of the model(s).
                Defaults to "server.npy".
                - If a string, treated as filename for the "server" model
                - If a dict, maps model identifiers to filenames/paths
                - Paths can be:
                  - Relative: resolved as ``<run_dir>/<model_dir>/<model_name>``
                  - Absolute: used directly (e.g., "/path/to/pretrained.npy")
        """
        super().__init__()

        self.model_dir = model_dir
        if model_name is None:
            self.model_name = {NPModelLocator.SERVER_MODEL_NAME: "server.npy"}
        elif isinstance(model_name, str):
            self.model_name = {NPModelLocator.SERVER_MODEL_NAME: model_name}
        elif isinstance(model_name, dict):
            self.model_name = model_name
        else:
            raise ValueError(f"model_name must be a str, or a Dict[str, str]. But got: {type(model_name)}")

    def get_model_names(self, fl_ctx: FLContext) -> List[str]:
        """Returns the list of model names that should be included from server in cross site validation.add()

        Args:
            fl_ctx (FLContext): FL Context object.

        Returns:
            List[str]: List of model names.
        """
        pass

    def locate_model(self, model_name, fl_ctx: FLContext) -> DXO:
        pass
