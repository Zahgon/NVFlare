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

import logging
from typing import Dict

import pytorch_lightning as pl
from pytorch_lightning.callbacks import Callback
from torch import Tensor

from nvflare.app_common.abstract.fl_model import FLModel, MetaKey
from nvflare.app_opt.pt.decomposers import TensorDecomposer
from nvflare.app_opt.pt.utils import inspect_model_params
from nvflare.client.api import clear, get_config, init, is_evaluate, is_submit_model, is_train, receive, send
from nvflare.client.config import ConfigKey
from nvflare.fuel.utils import fobs

from .callbacks import RestoreState

FL_META_KEY = "__fl_meta__"


def patch(
    trainer: pl.Trainer, restore_state: bool = True, load_state_dict_strict: bool = True, update_fit_loop: bool = True
):
    """Patches the PyTorch Lightning Trainer for usage with NVFlare.

    Args:
        trainer: the PyTorch Lightning trainer.
        restore_state: whether to restore optimizer and learning rate scheduler states.
            Defaults to `True`.
        load_state_dict_strict: exposes `strict` argument of `torch.nn.Module.load_state_dict()`
            used to load the received model. Defaults to `True`.
            See https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.load_state_dict for details.
            NVFlare still validates incoming keys and shapes before calling ``load_state_dict()``.
            With ``True``, any incoming key that does not exist in the local Lightning
            module is rejected before loading. With ``False``, NVFlare warns and
            filters the payload down to matching keys, which is useful for partial
            model updates where the client only keeps part of the server keyspace.
        update_fit_loop: whether to increase `trainer.fit_loop.max_epochs` and `trainer.fit_loop.epoch_loop.max_steps` each FL round.
            Defaults to `True` which is suitable for most PyTorch Lightning applications.

    Example:

        Normal usage:

        .. code-block:: python

            trainer = Trainer(max_epochs=1)
            flare.patch(trainer)


        Advanced usage:

        If users want to pass additional information to FLARE server side via the lightning API,
        they will need to set the information inside the attributes called ``__fl_meta__`` in their LightningModule.

        .. code-block:: python

            class LitNet(LightningModule):
                def __init__(self):
                    super().__init__()
                    self.save_hyperparameters()
                    self.model = Net()
                    self.train_acc = Accuracy(task="multiclass", num_classes=NUM_CLASSES)
                    self.valid_acc = Accuracy(task="multiclass", num_classes=NUM_CLASSES)
                    self.__fl_meta__ = {"CUSTOM_VAR": "VALUE_OF_THE_VAR"}

    """
    pass


class FLCallback(Callback):
    def __init__(self, rank: int = 0, load_state_dict_strict: bool = True, update_fit_loop: bool = True):
        """FL callback for lightning API.

        Args:
            rank: global rank of the PyTorch Lightning trainer.
            load_state_dict_strict: exposes `strict` argument of `torch.nn.Module.load_state_dict()`
                used to load the received model. Defaults to `True`.
                See https://pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.load_state_dict for details.
                NVFlare still validates incoming keys and shapes before calling ``load_state_dict()``.
                With ``True``, unexpected incoming keys are treated as contract
                drift and fail fast. With ``False``, unexpected keys are logged
                and ignored, while compatible keys are still loaded.
            update_fit_loop: whether to increase `trainer.fit_loop.max_epochs` and `trainer.fit_loop.epoch_loop.max_steps` each FL round.
                Defaults to `True` which is suitable for most PyTorch Lightning applications.
        """
        super(FLCallback, self).__init__()
        init(rank=str(rank))
        self.train_with_evaluation = get_config().get(ConfigKey.TASK_EXCHANGE, {}).get(ConfigKey.TRAIN_WITH_EVAL, False)
        self.current_round = None
        self.metrics = None
        self.total_local_epochs = 0
        self.total_local_steps = 0
        self.max_epochs_per_round = None
        self.max_steps_per_round = None
        self.rank = rank
        self._is_training = False
        self._is_evaluation = False
        self._is_submit_model = False
        self._load_state_dict_strict = load_state_dict_strict
        self._update_fit_loop = update_fit_loop

        self.logger = logging.getLogger(self.__class__.__name__)

    def reset_state(self, trainer):
        """Resets the state.

        If the next round of federated training needs to reuse the same callback
        instance, the reset_state() needs to be called first
        Not only resets the states, also sets states for next round
        """
        pass

    def on_train_start(self, trainer, pl_module):
        # receive the global model and update the local model with global model
        pass

    def on_train_end(self, trainer, pl_module):
        pass

    def on_validation_start(self, trainer, pl_module):
        # receive the global model and update the local model with global model
        # the 1st time validate() or train() is called.
        # expect user will validate the global model first (i.e. validate()), once that's done.
        # the metrics will be set.
        # The subsequent validate() calls will not trigger the receive update model.
        # Hence the validate() will be validating the local model.
        pass

    def on_validation_end(self, trainer, pl_module):
        pass

    def _receive_and_update_model(self, trainer, pl_module):
        """Receive a global model and apply the compatible portion locally.

        The incoming payload is validated before ``load_state_dict()`` so that
        wrapper-induced key drift and shape mismatches fail with actionable
        diagnostics instead of being silently skipped. In non-strict mode,
        incoming keys that are not present locally are filtered out after a
        warning, which allows partial model updates as long as some keys match.
        """
        pass

    def _receive_model(self, trainer) -> FLModel:
        """Receives model from NVFlare."""
        pass

    def _send_model(self, output_model: FLModel):
        pass


def _extract_metrics(metrics: Dict[str, Tensor]):
    pass
