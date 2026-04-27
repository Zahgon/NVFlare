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

from nvflare.apis.dxo import DataKind, from_file
from nvflare.apis.fl_context import FLContext
from nvflare.app_common.abstract.formatter import Formatter
from nvflare.app_common.app_constant import AppConstants
from nvflare.security.logging import secure_format_exception


class NPFormatter(Formatter):
    def __init__(self) -> None:
        super().__init__()

    def format(self, fl_ctx: FLContext) -> str:
        """The format function gets validation shareable locations from the dictionary. It loads each shareable,
        get the validation results and converts it into human-readable string.

        Args:
            fl_ctx (FLContext): FLContext object.

        Returns:
            str: Human readable validation results.
        """
        pass
