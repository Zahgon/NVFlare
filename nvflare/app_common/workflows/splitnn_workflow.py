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

from nvflare.apis.client import Client
from nvflare.apis.controller_spec import ClientTask, Task
from nvflare.apis.fl_constant import ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.impl.controller import Controller
from nvflare.apis.shareable import Shareable
from nvflare.apis.signal import Signal
from nvflare.app_common.abstract.learnable_persistor import LearnablePersistor
from nvflare.app_common.abstract.shareable_generator import ShareableGenerator
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.app_event_type import AppEventType
from nvflare.security.logging import secure_format_exception
from nvflare.widgets.info_collector import GroupInfoCollector, InfoCollector


class SplitNNDataKind(object):
    ACTIVATIONS = "_splitnn_activations_"
    GRADIENT = "_splitnn_gradient_"


class SplitNNConstants(object):
    BATCH_INDICES = "_splitnn_batch_indices_"
    DATA = "_splitnn_data_"
    BATCH_SIZE = "_splitnn_batch_size_"
    TARGET_NAMES = "_splitnn_target_names_"

    TASK_INIT_MODEL = "_splitnn_task_init_model_"
    TASK_TRAIN_LABEL_STEP = "_splitnn_task_train_label_step_"
    TASK_VALID_LABEL_STEP = "_splitnn_task_valid_label_step_"
    TASK_TRAIN = "_splitnn_task_train_"

    TASK_RESULT = "_splitnn_task_result_"
    TIMEOUT = 60.0  # timeout for waiting for reply from aux message request


class SplitNNController(Controller):
    def __init__(
        self,
        num_rounds: int = 5000,
        start_round: int = 0,
        persistor_id=AppConstants.DEFAULT_PERSISTOR_ID,  # used to init the models on both clients
        shareable_generator_id=AppConstants.DEFAULT_SHAREABLE_GENERATOR_ID,
        init_model_task_name=SplitNNConstants.TASK_INIT_MODEL,
        train_task_name=SplitNNConstants.TASK_TRAIN,
        task_timeout: int = 10,
        ignore_result_error: bool = True,
        batch_size: int = 256,
    ):
        """The controller for Split Learning Workflow.

        The SplitNNController workflow defines Federated training on all clients.
        The model persistor (persistor_id) is used to load the initial global model which is sent to all clients.
        Each clients sends it's updated weights after local training which is aggregated (aggregator_id). The
        shareable generator is used to convert the aggregated weights to shareable and shareable back to weights.
        The model_persistor also saves the model after training.

        Args:
            num_rounds (int, optional): The total number of training rounds. Defaults to 5.
            start_round (int, optional): Start round for training. Defaults to 0.
            persistor_id (str, optional): ID of the persistor component. Defaults to "persistor".
            shareable_generator_id (str, optional): ID of the shareable generator. Defaults to "shareable_generator".
            init_model_task_name: Task name used to initialize the local models.
            train_task_name: Task name used for split learning.
            task_timeout (int, optional): timeout (in sec) to determine if one client fails
                to request the task which it is assigned to. Defaults to 10.
            ignore_result_error (bool, optional): whether this controller can proceed if result has errors. Defaults to True.
        Raises:
            TypeError: when any of input arguments does not have correct type
            ValueError: when any of input arguments is out of range
        """
        Controller.__init__(self)

        # Check arguments
        if not isinstance(num_rounds, int):
            raise TypeError("`num_rounds` must be int but got {}".format(type(num_rounds)))
        if not isinstance(start_round, int):
            raise TypeError("`start_round` must be int but got {}".format(type(start_round)))
        if not isinstance(task_timeout, int):
            raise TypeError("`train_timeout` must be int but got {}".format(type(task_timeout)))
        if not isinstance(persistor_id, str):
            raise TypeError("`persistor_id` must be a string but got {}".format(type(persistor_id)))
        if not isinstance(shareable_generator_id, str):
            raise TypeError("`shareable_generator_id` must be a string but got {}".format(type(shareable_generator_id)))
        if not isinstance(init_model_task_name, str):
            raise TypeError("`init_model_task_name` must be a string but got {}".format(type(init_model_task_name)))
        if not isinstance(train_task_name, str):
            raise TypeError("`train_task_name` must be a string but got {}".format(type(train_task_name)))
        if num_rounds < 0:
            raise ValueError("num_rounds must be greater than or equal to 0.")
        if start_round < 0:
            raise ValueError("start_round must be greater than or equal to 0.")

        self.persistor_id = persistor_id
        self.shareable_generator_id = shareable_generator_id
        self.persistor = None
        self.shareable_generator = None

        # config data
        self._num_rounds = num_rounds
        self._start_round = start_round
        self._task_timeout = task_timeout
        self.ignore_result_error = ignore_result_error

        # workflow phases: init, train, validate
        self._phase = AppConstants.PHASE_INIT
        self._global_weights = None
        self._current_round = None

        # task names
        self.init_model_task_name = init_model_task_name
        self.train_task_name = train_task_name

        self.targets_names = ["site-1", "site-2"]
        self.nr_supported_clients = 2
        self.batch_size = batch_size

    def start_controller(self, fl_ctx: FLContext):
        pass

    def _process_result(self, client_task: ClientTask, fl_ctx: FLContext) -> bool:
        # submitted shareable is stored in client_task.result
        # we need to update task.data with that shareable so the next target
        # will get the updated shareable
        pass

    def _check_targets(self, fl_ctx: FLContext):
        pass

    def _init_models(self, abort_signal: Signal, fl_ctx: FLContext):
        pass

    def _train(self, abort_signal: Signal, fl_ctx: FLContext):
        pass

    def control_flow(self, abort_signal: Signal, fl_ctx: FLContext):
        pass

    def stop_controller(self, fl_ctx: FLContext):
        pass

    def process_result_of_unknown_task(
        self,
        client: Client,
        task_name: str,
        client_task_id: str,
        result: Shareable,
        fl_ctx: FLContext,
    ):
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass
