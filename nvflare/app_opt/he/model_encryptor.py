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

import re
import time
from typing import Optional, Union

import numpy as np
import tenseal as ts
from tenseal.tensors.ckksvector import CKKSVector

from nvflare.apis.dxo import DXO, DataKind, MetaKey
from nvflare.apis.dxo_filter import DXOFilter
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_opt.he import decomposers
from nvflare.app_opt.he.constant import HE_ALGORITHM_CKKS
from nvflare.app_opt.he.homomorphic_encrypt import count_encrypted_layers, load_tenseal_context_from_workspace


class HEModelEncryptor(DXOFilter):
    def __init__(
        self,
        tenseal_context_file: str = "client_context.tenseal",
        encrypt_layers: Optional[Union[list[str], str]] = None,
        aggregation_weights: Optional[dict[str, float]] = None,
        weigh_by_local_iter: bool = True,
        data_kinds: Optional[list[DataKind]] = None,
    ):
        """Filter to encrypt Shareable object using homomorphic encryption (HE) with TenSEAL
           https://github.com/OpenMined/TenSEAL.

        Args:
            tenseal_context_file: tenseal context files containing encryption keys and parameters
            encrypt_layers: if not specified (None), all layers are being encrypted;
                            if list of variable/layer names, only specified variables are encrypted;
                            if string containing regular expression (e.g. "conv"), only matched variables are
                            being encrypted.
            aggregation_weights: dictionary of client aggregation `{"client1": 1.0, "client2": 2.0, "client3": 3.0}`;
                                 defaults to a weight of 1.0 if not specified.
                                 Note, if specified, the same `aggregation_weights` should also be used on the server
                                 aggregator for the resulting weighted sum to be valid,
                                 i.e. in `HEInTimeAccumulateWeightedAggregator`.
            weigh_by_local_iter: If true, multiply client weights on first before encryption (default: `True`
            which is recommended for HE)
            data_kinds: data kinds to apply this filter

        """
        if not data_kinds:
            data_kinds = [DataKind.WEIGHT_DIFF, DataKind.WEIGHTS]

        super().__init__(supported_data_kinds=[DataKind.WEIGHTS, DataKind.WEIGHT_DIFF], data_kinds_to_filter=data_kinds)

        self.logger.info("Using HE model encryptor.")
        self.tenseal_context = None
        self.tenseal_context_file = tenseal_context_file
        self.aggregation_weights = aggregation_weights or {}
        self.logger.info(f"client weights control: {self.aggregation_weights}")
        self.weigh_by_local_iter = weigh_by_local_iter
        self.n_iter = None
        self.client_name = None
        self.aggregation_weight = None
        self.encrypt_layers = encrypt_layers

        # choose which layers to encrypt
        if self.encrypt_layers is not None:
            if not (isinstance(self.encrypt_layers, list) or isinstance(self.encrypt_layers, str)):
                raise ValueError(
                    f"Must provide a list of layer names or a string for regex matching, but got {type(self.encrypt_layers)}"
                )
        if isinstance(self.encrypt_layers, list):
            for encrypt_layer in self.encrypt_layers:
                if not isinstance(encrypt_layer, str):
                    raise ValueError(
                        f"encrypt_layers needs to be a list of layer names to encrypt, but found element of type {type(encrypt_layer)}"
                    )
            self.logger.info(f"Encrypting {len(self.encrypt_layers)} layers")
        elif isinstance(self.encrypt_layers, str):
            self.encrypt_layers = re.compile(self.encrypt_layers) if self.encrypt_layers else None
            self.logger.info(f'Encrypting all layers based on regex matches with "{self.encrypt_layers}"')

        decomposers.register()

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def encryption(self, params, fl_ctx: FLContext):
        pass

    def process_dxo(self, dxo: DXO, shareable: Shareable, fl_ctx: FLContext) -> Union[None, DXO]:
        """Filter process apply to the Shareable object.

        Args:
            dxo: data to be processed
            shareable: that the dxo belongs to
            fl_ctx: FLContext

        Returns: DXO object with encrypted weights

        """
        pass

    def _process(self, dxo: DXO, fl_ctx: FLContext) -> DXO:
        pass
