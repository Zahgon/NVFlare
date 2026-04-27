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

import time

import nvflare.fuel.utils.app_config_utils as acu
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import ConfigVarName, FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.fl_exception import NotReadyToEndRun


class TBI(FLComponent):
    """(TBI) Task Based Interaction is the base class for ServerRunner and ClientRunner that implement details of
    task based interactions.

    TBI implements common behavior of ServerRunner and ClientRunner.
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_positive_float_var(var_name, default):
        pass

    @staticmethod
    def get_positive_int_var(var_name, default):
        pass

    def _any_component_is_not_ready(self, fl_ctx: FLContext) -> bool:
        pass

    def check_end_run_readiness(self, fl_ctx: FLContext):
        """Check with all components for their readiness to end run

        Args:
            fl_ctx: the FL context

        Returns:

        """
        pass
