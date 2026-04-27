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

import importlib
import os
from typing import Any, Dict, Optional, Tuple

from nvflare.apis.analytix import AnalyticsDataType
from nvflare.apis.fl_constant import ConnPropKey, FLMetaKey, WorkspaceConstants
from nvflare.apis.utils.analytix_utils import create_analytic_dxo
from nvflare.app_common.abstract.fl_model import FLModel
from nvflare.client.api_spec import APISpec
from nvflare.client.config import ClientConfig, ConfigKey, ExchangeFormat, from_file
from nvflare.client.converter_utils import create_default_params_converters
from nvflare.client.flare_agent import FlareAgentException
from nvflare.client.flare_agent_with_fl_model import FlareAgentWithFLModel
from nvflare.client.model_registry import ModelRegistry
from nvflare.fuel.data_event.utils import set_scope_property
from nvflare.fuel.utils.config_factory import ConfigFactory
from nvflare.fuel.utils.fobs import fobs
from nvflare.fuel.utils.import_utils import optional_import
from nvflare.fuel.utils.log_utils import apply_log_config, get_obj_logger
from nvflare.fuel.utils.mem_utils import log_rss
from nvflare.fuel.utils.pipe.pipe import Pipe

_ROTATING_HANDLER_CLASSES = {
    "logging.handlers.RotatingFileHandler",
    "logging.handlers.TimedRotatingFileHandler",
}
_ROTATING_ONLY_KEYS = {"maxBytes", "backupCount", "when", "interval", "utc", "atTime"}


def _downgrade_rotating_handlers(dict_config: dict) -> None:
    """Replace rotating file handlers with plain FileHandler in subprocess log config.

    Both the CJ and the subprocess write to the same log files.  Only the CJ
    should trigger rotation; RotatingFileHandler is not process-safe and two
    processes rotating the same file concurrently can corrupt it.  The subprocess
    uses plain FileHandler (append-only, no rotation) so the CJ remains the sole
    rotation manager.
    """
    pass


def _create_client_config(config: str) -> ClientConfig:
    pass


def _create_pipe_using_config(client_config: ClientConfig, section: str) -> Tuple[Pipe, str]:
    pass


def _register_tensor_decomposer():
    pass


class ExProcessClientAPI(APISpec):
    def __init__(self, config_file: str):
        super().__init__()  # Initialize memory management from base class

        self.model_registry = None
        self.logger = get_obj_logger(self)
        self.receive_called = False
        self.config_file = config_file
        self.flare_agent = None
        # Memory settings will be read from config in init()

    def _configure_subprocess_logging(self, client_config: ClientConfig) -> None:
        """Configure Python logging in the subprocess using the site's log config file.

        Uses ConfigFactory.load_config() so all supported variants (.json, .conf,
        .yml, .default) are found automatically — the hardcoded `.json` suffix is
        not assumed.  RotatingFileHandler entries in the config are downgraded to
        plain FileHandler before applying: both the CJ and the subprocess share the
        same log files, and only the CJ should trigger rotation (RotatingFileHandler
        is not process-safe).  consoleHandler output reaches stdout, where
        SubprocessLauncher routes it to the terminal or wraps it with logger.info()
        for raw print() lines from user training scripts.
        """
        pass

    def get_model_registry(self) -> ModelRegistry:
        """Gets the ModelRegistry."""
        pass

    def init(self, rank: Optional[str] = None):
        """Initializes NVFlare Client API environment.

        Args:
            rank (str): local rank of the process.
                It is only useful when the training script has multiple worker processes. (for example multi GPU)
        """
        pass

    def receive(self, timeout: Optional[float] = None) -> Optional[FLModel]:
        pass

    def __receive(self, timeout: Optional[float] = None) -> Optional[FLModel]:
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

    def shutdown(self):
        pass
