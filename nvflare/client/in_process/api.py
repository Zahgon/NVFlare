# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
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
from typing import Any, Dict, Optional

from nvflare.apis.analytix import AnalyticsDataType
from nvflare.apis.fl_constant import FLMetaKey
from nvflare.apis.shareable import Shareable
from nvflare.app_common.abstract.fl_model import FLModel, ParamsType
from nvflare.app_common.utils.fl_model_utils import FLModelUtils
from nvflare.client.api_spec import APISpec
from nvflare.client.config import ClientConfig, ConfigKey, TransferType
from nvflare.client.constants import SYS_ATTRS
from nvflare.client.utils import DIFF_FUNCS
from nvflare.fuel.data_event.data_bus import DataBus
from nvflare.fuel.data_event.event_manager import EventManager
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.fuel.utils.mem_utils import log_rss

TOPIC_LOG_DATA = "LOG_DATA"
TOPIC_STOP = "STOP"
TOPIC_ABORT = "ABORT"
TOPIC_LOCAL_RESULT = "LOCAL_RESULT"
TOPIC_GLOBAL_RESULT = "GLOBAL_RESULT"


class InProcessClientAPI(APISpec):
    def __init__(self, task_metadata: dict, result_check_interval: float = 2.0):
        """Initializes the InProcessClientAPI.

        Args:
            task_metadata (dict): task metadata, added to client_config.
            result_check_interval (float): how often to check if result is available.
        """
        super().__init__()  # Initialize memory management from base class

        self.data_bus = DataBus()
        self.data_bus.subscribe([TOPIC_GLOBAL_RESULT], self.__receive_callback)
        self.data_bus.subscribe([TOPIC_ABORT, TOPIC_STOP], self.__ask_to_abort)

        self.meta = task_metadata
        self.result_check_interval = result_check_interval

        self.fl_model = None
        self.sys_info = {}
        self.client_config: Optional[ClientConfig] = None
        self.logger = get_obj_logger(self)
        self.event_manager = EventManager(self.data_bus)
        self.abort_reason = ""
        self.stop_reason = ""
        self.abort = False
        self.stop = False
        self.rank = None
        self.receive_called = False  # to check if users have call received for a new model

    def init(self, rank: Optional[str] = None, config: Optional[Dict] = None):
        """Initializes NVFlare Client API environment.

        Args:
            config (Union[str, Dict]): config dictionary.
            rank (str): local rank of the process.
                It is only useful when the training script has multiple worker processes. (for example multi GPU)
        """
        pass

    def prepare_client_config(self, config):
        pass

    def set_meta(self, meta: dict):
        pass

    def configure_memory_management(self, gc_rounds: int = 0, cuda_empty_cache: bool = False):
        """Configure memory management settings.

        Args:
            gc_rounds: Cleanup every N rounds. 0 = disabled.
            cuda_empty_cache: If True, call torch.cuda.empty_cache() on cleanup.
        """
        pass

    def receive(self, timeout: Optional[float] = None) -> Optional[FLModel]:
        pass

    def __receive(self) -> Optional[FLModel]:
        pass

    def send(self, model: FLModel, clear_cache: bool = True) -> None:
        pass

    def system_info(self) -> Dict:
        pass

    def get_config(self) -> Dict:
        pass

    def get_job_id(self) -> str:
        pass

    def get_site_name(self) -> str:
        pass

    def get_task_name(self) -> str:
        pass

    def is_running(self) -> bool:
        pass

    def is_train(self) -> bool:
        pass

    def is_evaluate(self) -> bool:
        pass

    def is_submit_model(self) -> bool:
        pass

    def log(self, key: str, value: Any, data_type: AnalyticsDataType, **kwargs):
        pass

    def clear(self):
        pass

    def _prepare_param_diff(self, model: FLModel) -> FLModel:
        pass

    def __receive_callback(self, topic, data, databus):

        pass

    def __ask_to_abort(self, topic, msg, databus):
        pass

    def __continue_job(self) -> bool:
        pass

    def shutdown(self):
        pass
