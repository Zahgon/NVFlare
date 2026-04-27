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

# The SCAFFOLD-related functions are based on https://github.com/Xtra-Computing/NIID-Bench

# MIT License
#
# Copyright (c) 2021 Yiqun Diao, Qinbin Li
#
# Copyright (c) 2020 International Business Machines
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import copy

import torch
from torch.optim import Optimizer


def get_lr_values(optimizer: Optimizer):
    """
    This function is used to get the learning rates of the optimizer.
    """
    pass


class PTScaffoldHelper(object):
    """Helper to be used with SCAFFOLD components.
    Implements the functions used for the algorithm proposed in
    Karimireddy et al. "SCAFFOLD: Stochastic Controlled Averaging for Federated Learning"
    (https://arxiv.org/abs/1910.06378) using PyTorch.
    SCAFFOLD-related functions are based on https://github.com/Xtra-Computing/NIID-Bench.
    See also Li et al. "Federated Learning on Non-IID Data Silos: An Experimental Study"
    (https://arxiv.org/abs/2102.02079).
    """

    def __init__(self):
        # SCAFFOLD control terms
        self.cnt = 0
        self.c_global = None
        self.c_local = None
        self.c_delta_para = None
        self.device = None

    def init(self, model):
        # create models for SCAFFOLD correction terms
        pass

    def get_params(self):
        pass

    def model_update(self, model, curr_lr, c_global_para, c_local_para):
        # Update model using scaffold controls
        # See https://github.com/Xtra-Computing/NIID-Bench/blob/main/experiments.py#L391
        pass

    def terms_update(self, model, curr_lr, c_global_para, c_local_para, model_global):
        # Update the local scaffold controls
        # See https://github.com/Xtra-Computing/NIID-Bench/blob/main/experiments.py#L403

        pass

    def load_global_controls(self, weights):
        pass

    def get_delta_controls(self):
        pass
