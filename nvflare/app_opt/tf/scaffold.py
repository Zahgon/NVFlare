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


import numpy as np
import tensorflow as tf

from .utils import flat_layer_weights_dict

gpu_devices = tf.config.experimental.list_physical_devices("GPU")
for device in gpu_devices:
    tf.config.experimental.set_memory_growth(device, True)


def optimize_weights(model, c_delta_para_value):
    """
    Efficiently assigns weights to `self.c_delta_para` based on trainability or non tainability.

    Args:
        model: The TensorFlow model containing layers.
        c_delta_para_value: Delta values for trainable variables.

    Returns:
        None. Modifies the `self.c_delta_para` attribute in-place.
    """
    pass


def get_lr_values(optimizer):
    """
    This function is used to get the learning rates of the optimizer.
    """
    pass


class TFScaffoldHelper(object):
    """Helper to be used with SCAFFOLD components."""

    def __init__(self):
        self.cnt = 0
        self.c_global = None
        self.c_local = None
        self.c_delta_para = None
        self.global_keys = None

    def init(self, model):
        pass

    def get_params(self):
        pass

    def model_update(self, model, curr_lr, c_global_para, c_local_para):
        pass

    def terms_update(
        self,
        model,
        curr_lr,
        c_global_para,
        c_local_para,
        model_global,
    ):
        pass

    def load_global_controls(self, weights):
        pass

    def get_delta_controls(self):
        pass


class ScaffoldCallback(tf.keras.callbacks.Callback):
    def __init__(self, scaffold_helper):
        super(ScaffoldCallback, self).__init__()
        self.scaffold_helper = scaffold_helper
        self.c_global_para, self.c_local_para = self.scaffold_helper.get_params()

    def on_epoch_end(self, epoch, logs=None):
        pass
