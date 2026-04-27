# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
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

import torch

from nvflare.apis.dxo import DataKind, MetaKey, from_shareable
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_common.abstract.learnable import Learnable
from nvflare.app_common.abstract.model import ModelLearnableKey, make_model_learnable
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_common.shareablegenerators.full_model_shareable_generator import FullModelShareableGenerator
from nvflare.security.logging import secure_format_exception


class PTFedOptModelShareableGenerator(FullModelShareableGenerator):
    def __init__(
        self,
        optimizer_args: dict = None,
        lr_scheduler_args: dict = None,
        source_model="model",
        device=None,
    ):
        """Implement the FedOpt algorithm.

        The algorithm is proposed in Reddi, Sashank, et al. "Adaptive federated optimization." arXiv preprint arXiv:2003.00295 (2020).
        This SharableGenerator will update the global model using the specified
        PyTorch optimizer and learning rate scheduler.
        Note: This class will use FedOpt to optimize the global trainable parameters (i.e. `self.model.named_parameters()`)
        but use FedAvg to update any other layers such as batch norm statistics.

        Args:
            optimizer_args: dictionary of optimizer arguments, e.g.
                {'class_path': 'torch.optim.SGD', 'args': {'lr': 1.0}} (default). 'path' is also accepted.
            lr_scheduler_args: dictionary of server-side learning rate scheduler arguments, e.g.
                {'class_path': 'torch.optim.lr_scheduler.CosineAnnealingLR', 'args': {'T_max': 100}} (default: None). 'path' is also accepted.
            source_model: either a valid torch model object or a component ID of a torch model object
            device: specify the device to run server-side optimization, e.g. "cpu" or "cuda:0"
                (will default to cuda if available and no device is specified).

        Raises:
            TypeError: when any of input arguments does not have correct type
        """
        super().__init__()
        if not optimizer_args:
            self.logger.warning("No optimizer_args provided. Using FedOpt with SGD and lr 1.0")
            optimizer_args = {"name": "SGD", "args": {"lr": 1.0}}

        if not isinstance(optimizer_args, dict):
            raise TypeError(
                "optimizer_args must be a dict of format, e.g. {'class_path': 'torch.optim.SGD', 'args': {'lr': 1.0}}."
            )
        if lr_scheduler_args is not None:
            if not isinstance(lr_scheduler_args, dict):
                raise TypeError(
                    "lr_scheduler_args must be a dict of format, e.g. "
                    "{'class_path': 'torch.optim.lr_scheduler.CosineAnnealingLR', 'args': {'T_max': 100}}."
                )
        self.source_model = source_model
        self.optimizer_args = optimizer_args
        self.lr_scheduler_args = lr_scheduler_args
        self.model = None
        self.optimizer = None
        self.lr_scheduler = None
        self.device = device
        self.optimizer_name = None
        self.lr_scheduler_name = None

    def _get_component_name(self, component_args):
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def server_update(self, model_diff):
        """Updates the global model using the specified optimizer.

        Args:
            model_diff: the aggregated model differences from clients.

        Returns:
            The updated PyTorch model state dictionary.

        """
        pass

    def shareable_to_learnable(self, shareable: Shareable, fl_ctx: FLContext) -> Learnable:
        """Convert Shareable to Learnable while doing a FedOpt update step.

        Supporting data_kind == DataKind.WEIGHT_DIFF

        Args:
            shareable (Shareable): Shareable to be converted
            fl_ctx (FLContext): FL context

        Returns:
            Model: Updated global ModelLearnable.
        """
        pass
