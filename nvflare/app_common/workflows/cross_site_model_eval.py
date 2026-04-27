# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
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
import shutil
import time
from typing import Union

from nvflare.apis.client import Client
from nvflare.apis.controller_spec import ClientTask, Task
from nvflare.apis.dxo import DXO, from_file, from_shareable, get_leaf_dxos
from nvflare.apis.fl_constant import ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.impl.controller import Controller
from nvflare.apis.shareable import Shareable
from nvflare.apis.signal import Signal
from nvflare.apis.workspace import Workspace
from nvflare.app_common.abstract.formatter import Formatter
from nvflare.app_common.abstract.model_locator import ModelLocator
from nvflare.app_common.app_constant import AppConstants, ModelName
from nvflare.app_common.app_event_type import AppEventType
from nvflare.security.logging import secure_format_exception
from nvflare.widgets.info_collector import GroupInfoCollector, InfoCollector


class CrossSiteModelEval(Controller):
    def __init__(
        self,
        task_check_period=0.5,
        cross_val_dir=AppConstants.CROSS_VAL_DIR,
        submit_model_timeout=600,
        validation_timeout: int = 6000,
        model_locator_id="",
        formatter_id="",
        submit_model_task_name=AppConstants.TASK_SUBMIT_MODEL,
        validation_task_name=AppConstants.TASK_VALIDATION,
        cleanup_models=False,
        participating_clients=None,
        wait_for_clients_timeout=300,
    ):
        """Cross Site Model Evaluation workflow.

        # TODO: change validation to evaluation to reflect the real meaning

        Args:
            task_check_period (float, optional): How often to check for new tasks or tasks being finished.
                Defaults to 0.5.
            cross_val_dir (str, optional): Path to cross site validation directory relative to run directory.
                Defaults to "cross_site_val".
            submit_model_timeout (int, optional): Timeout of submit_model_task. Defaults to 600 secs.
            validation_timeout (int, optional): Timeout for validate_model task. Defaults to 6000 secs.
            model_locator_id (str, optional): ID for `ModelLocator` component. Defaults to "".
            formatter_id (str, optional): ID for `Formatter` component. Defaults to "".
            submit_model_task_name (str, optional): Name of submit_model task. Defaults to "".
            validation_task_name (str, optional): Name of validate_model task. Defaults to "validate".
            cleanup_models (bool, optional): Whether or not models should be deleted after run. Defaults to False.
            participating_clients (list, optional): List of participating client names. If not provided, defaults
                to all clients connected at start of controller.
            wait_for_clients_timeout (int, optional): Timeout for clients to appear. Defaults to 300 secs
        """
        super().__init__(task_check_period=task_check_period)

        if not isinstance(task_check_period, float):
            raise TypeError("task_check_period must be float but got {}".format(type(task_check_period)))
        if not isinstance(cross_val_dir, str):
            raise TypeError("cross_val_dir must be a string but got {}".format(type(cross_val_dir)))
        if not isinstance(submit_model_timeout, int):
            raise TypeError("submit_model_timeout must be int but got {}".format(type(submit_model_timeout)))
        if not isinstance(validation_timeout, int):
            raise TypeError("validation_timeout must be int but got {}".format(type(validation_timeout)))
        if not isinstance(model_locator_id, str):
            raise TypeError("model_locator_id must be a string but got {}".format(type(model_locator_id)))
        if not isinstance(formatter_id, str):
            raise TypeError("formatter_id must be a string but got {}".format(type(formatter_id)))
        if not isinstance(submit_model_task_name, str):
            raise TypeError("submit_model_task_name must be a string but got {}".format(type(submit_model_task_name)))
        if not isinstance(validation_task_name, str):
            raise TypeError("validation_task_name must be a string but got {}".format(type(validation_task_name)))
        if not isinstance(cleanup_models, bool):
            raise TypeError("cleanup_models must be bool but got {}".format(type(cleanup_models)))

        if participating_clients:
            if not isinstance(participating_clients, list):
                raise TypeError("participating_clients must be a list but got {}".format(type(participating_clients)))
            if not all(isinstance(x, str) for x in participating_clients):
                raise TypeError("participating_clients must be strings")

        if submit_model_timeout < 0:
            raise ValueError("submit_model_timeout must be greater than or equal to 0.")
        if validation_timeout < 0:
            raise ValueError("model_validate_timeout must be greater than or equal to 0.")
        if wait_for_clients_timeout < 0:
            raise ValueError("wait_for_clients_timeout must be greater than or equal to 0.")

        self._cross_val_dir = cross_val_dir
        self._model_locator_id = model_locator_id
        self._formatter_id = formatter_id
        self._submit_model_task_name = submit_model_task_name
        self._validation_task_name = validation_task_name
        self._submit_model_timeout = submit_model_timeout
        self._validation_timeout = validation_timeout
        self._wait_for_clients_timeout = wait_for_clients_timeout
        self._cleanup_models = cleanup_models
        self._participating_clients = participating_clients

        self._val_results = {}
        self._server_models = {}
        self._client_models = {}

        self._formatter = None
        self._cross_val_models_dir = None
        self._cross_val_results_dir = None
        self._model_locator = None

    def start_controller(self, fl_ctx: FLContext):
        # If the list of participating clients is not provided, include all clients currently available.
        pass

    def control_flow(self, abort_signal: Signal, fl_ctx: FLContext):
        pass

    def stop_controller(self, fl_ctx: FLContext):
        pass

    def _receive_local_model_cb(self, client_task: ClientTask, fl_ctx: FLContext):
        pass

    def _before_send_validate_task_cb(self, client_task: ClientTask, fl_ctx: FLContext):
        pass

    def _after_send_validate_task_cb(self, client_task: ClientTask, fl_ctx: FLContext):
        # Once task is sent clear data to restore memory
        pass

    def _receive_val_result_cb(self, client_task: ClientTask, fl_ctx: FLContext):
        # Find name of the client sending this
        pass

    def _locate_server_models(self, fl_ctx: FLContext) -> bool:
        # Load models from model_locator
        pass

    def _accept_local_model(self, client_name: str, result: Shareable, fl_ctx: FLContext):
        pass

    def _save_client_model(self, model_name: str, dxo: DXO, fl_ctx: FLContext):
        pass

    def _send_validation_task(self, model_name: str, fl_ctx: FLContext):
        pass

    def _accept_val_result(self, client_name: str, result: Shareable, fl_ctx: FLContext):
        pass

    def _save_validation_result(self, client_name: str, model_name: str, dxo, fl_ctx):
        pass

    def _save_dxo_content(self, name: str, save_dir: str, dxo: DXO, fl_ctx: FLContext) -> str:
        """Saves shareable to given directory within the app_dir.

        Args:
            name (str): Name of shareable
            save_dir (str): Relative path to directory in which to save
            dxo (DXO): DXO object
            fl_ctx (FLContext): FLContext object

        Returns:
            str: Path to the file saved.
        """
        pass

    def _load_validation_content(self, name: str, load_dir: str, fl_ctx: FLContext) -> Union[DXO, None]:
        # Load shareable from disk
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def process_result_of_unknown_task(
        self, client: Client, task_name: str, client_task_id: str, result: Shareable, fl_ctx: FLContext
    ):
        pass
