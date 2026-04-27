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

import time
from typing import Union

import torch

from nvflare.app_common.abstract.fl_model import FLModel
from nvflare.app_common.workflows.fedavg import FedAvg
from nvflare.security.logging import secure_format_exception


class FedOpt(FedAvg):
    def __init__(
        self,
        *args,
        source_model: Union[str, torch.nn.Module],
        optimizer_args: dict = {
            "class_path": "torch.optim.SGD",
            "args": {"lr": 1.0, "momentum": 0.6},
        },
        lr_scheduler_args: dict = {
            "class_path": "torch.optim.lr_scheduler.CosineAnnealingLR",
            "args": {"T_max": 3, "eta_min": 0.9},
        },
        device=None,
        **kwargs,
    ):
        """Implement the FedOpt algorithm. Based on FedAvg ModelController.

        The algorithm is proposed in Reddi, Sashank, et al. "Adaptive federated optimization." arXiv preprint arXiv:2003.00295 (2020).
        After each round, update the global model using the specified PyTorch optimizer and learning rate scheduler.
        Note: This class will use FedOpt to optimize the global trainable parameters (i.e. `self.torch_model.named_parameters()`)
        but use FedAvg to update any other layers such as batch norm statistics.

        Args:
            source_model: component id of torch model object or a valid torch model object
            optimizer_args: dictionary of optimizer arguments, with keys of 'optimizer_path' and 'args.
            lr_scheduler_args: dictionary of server-side learning rate scheduler arguments, with keys of 'lr_scheduler_path' and 'args.
            device: specify the device to run server-side optimization, e.g. "cpu" or "cuda:0"
                (will default to cuda if available and no device is specified).

        Raises:
            TypeError: when any of input arguments does not have correct type
        """
        super().__init__(*args, **kwargs)

        self.source_model = source_model
        self.optimizer_args = optimizer_args
        self.lr_scheduler_args = lr_scheduler_args
        if device is None:
            self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)

        self.torch_model = None
        self.optimizer = None
        self.lr_scheduler = None

    def run(self):
        # set up source model
        pass

    def optimizer_update(self, model_diff):
        """Updates the global model using the specified optimizer.

        Args:
            model_diff: the aggregated model differences from clients.

        Returns:
            The updated PyTorch model state dictionary.

        """
        pass

    def update_model(self, global_model: FLModel, aggr_result: FLModel):
        pass
