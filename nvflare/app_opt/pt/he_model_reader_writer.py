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

import numpy as np

from nvflare.apis.fl_context import FLContext
from nvflare.app_opt.pt.model_reader_writer import PTModelReaderWriter
from nvflare.app_opt.pt.utils import feed_vars
from nvflare.security.logging import secure_format_exception


class HEPTModelReaderWriter(PTModelReaderWriter):
    def apply_model(self, network, multi_processes: bool, model_params: dict, fl_ctx: FLContext, options=None):
        """Write global model back to local model.

        Needed to extract local parameter shape to reshape decrypted vectors.

        Args:
            network (pytorch.nn): network object to read/write
            multi_processes (bool): is the workflow in multi_processes environment
            model_params (dict): which parameters to read/write
            fl_ctx (FLContext): FL system-wide context
            options (dict, optional): additional information on how to process read/write. Defaults to None.

        Raises:
            RuntimeError: unable to reshape the network layers or mismatch between network layers and model_params

        Returns:
            list: a list of parameters been processed
        """
        pass
