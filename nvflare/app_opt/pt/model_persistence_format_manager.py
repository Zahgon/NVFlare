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

from collections import OrderedDict

import torch

from nvflare.apis.dxo import MetaKey
from nvflare.app_common.abstract.model import (
    ModelLearnable,
    ModelLearnableKey,
    make_model_learnable,
    validate_model_learnable,
)
from nvflare.app_common.app_constant import ModelFormat
from nvflare.app_opt.pt.utils import inspect_model_params


class PTModelPersistenceFormatManager(object):

    PERSISTENCE_KEY_MODEL = "model"
    PERSISTENCE_KEY_TRAIN_CONF = "train_conf"
    PERSISTENCE_KEY_META_PROPS = "meta_props"

    def __init__(self, data: dict, default_train_conf=None, allow_numpy_conversion=True):
        """Manage the format for model persistence.

        Args:
            data (dict): either the dictionary mapping variables to values or a dict of dict.
            default_train_conf (dict, optional): configuration for train. Defaults to None.
            allow_numpy_conversion (bool): If set to True, enables conversion between PyTorch tensors and NumPy arrays.
                PyTorch tensors will be converted to NumPy arrays during 'load_model',
                and NumPy arrays will be converted to PyTorch tensors during 'save_model'. Defaults to True.

        Raises:
            TypeError: when data is not a dictionary
        """
        if not isinstance(data, dict):
            raise TypeError("data must be a dict but got {}".format(type(data)))

        self.var_dict = None
        self.meta = None
        self.train_conf = None
        self.other_props = {}  # other props from the original data that need to be kept

        if self.PERSISTENCE_KEY_MODEL not in data:
            # this is a simple weight dict
            self.var_dict = data
        else:
            # dict of dicts
            self.var_dict = data[self.PERSISTENCE_KEY_MODEL]
            self.meta = data.get(self.PERSISTENCE_KEY_META_PROPS, None)
            self.train_conf = data.get(self.PERSISTENCE_KEY_TRAIN_CONF, None)

            # we need to keep other props, if any, so they can be kept when persisted
            for k, v in data.items():
                if k not in [
                    self.PERSISTENCE_KEY_MODEL,
                    self.PERSISTENCE_KEY_META_PROPS,
                    self.PERSISTENCE_KEY_TRAIN_CONF,
                ]:
                    self.other_props[k] = v

        if not self.train_conf:
            self.train_conf = default_train_conf

        self._allow_numpy_conversion = allow_numpy_conversion

    def _get_processed_vars(self) -> dict:
        pass

    def to_model_learnable(self, exclude_vars) -> ModelLearnable:
        pass

    def to_persistence_dict(self) -> dict:
        pass

    def update(self, ml: ModelLearnable):
        """Update the persistence data with the learned values.

        Args:
            ml (ModelLearnable): updated information to be merged into existing ModelLearnable

        Raises:
            ValueError: if the incoming learnable is invalid, if any matching key
                has a shape mismatch, if a non-empty update has zero compatible
                matches with the persisted checkpoint, or if the update would
                introduce keys that do not already exist in the checkpoint.

        Notes:
            Partial updates are supported: learned weights only need to cover the
            subset of checkpoint keys that the client actually trained. The
            original persisted weights for untouched keys are preserved.
        """
        pass

    @staticmethod
    def get_persist_model_format():
        pass
