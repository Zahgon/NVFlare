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

from nvflare.apis.fl_context import FLContext
from nvflare.app_common.abstract.model_processor import ModelProcessor
from nvflare.app_opt.pt.utils import feed_vars
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.security.logging import secure_format_exception


class PTModelReaderWriter(ModelProcessor):
    def __init__(self):
        """Perform the actual read/write operation for PyTorch-based models."""
        self._name = self.__class__.__name__
        self.logger = get_obj_logger(self)

    def extract_model(self, network, multi_processes: bool, model_vars: dict, fl_ctx: FLContext) -> dict:
        pass

    def apply_model(self, network, multi_processes: bool, model_params: dict, fl_ctx: FLContext, options=None):
        """Set the local model according to model_data.

        Args:
            model_params: model data information
            fl_ctx (FLContext): FL Context delivered by workflow
            options: . Defaults to None.

        Raises:
            RuntimeError: Raised when being unable to apply model_params to the network

        Returns:
            a list of ops applied to model
        """
        pass
