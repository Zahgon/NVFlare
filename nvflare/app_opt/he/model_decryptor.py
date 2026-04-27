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

import time
from typing import Union

import numpy as np
from tenseal.tensors.ckksvector import CKKSVector

from nvflare.apis.dxo import DXO, DataKind, MetaKey
from nvflare.apis.dxo_filter import DXOFilter
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_opt.he import decomposers
from nvflare.app_opt.he.constant import HE_ALGORITHM_CKKS
from nvflare.app_opt.he.homomorphic_encrypt import (
    count_encrypted_layers,
    deserialize_nested_dict,
    load_tenseal_context_from_workspace,
)


class HEModelDecryptor(DXOFilter):
    def __init__(self, tenseal_context_file="client_context.tenseal", data_kinds: [str] = None):
        """Filter to decrypt Shareable object using homomorphic encryption (HE) with TenSEAL
        https://github.com/OpenMined/TenSEAL.

        Args:
            tenseal_context_file: tenseal context files containing decryption keys and parameters
            data_kinds: kinds of DXOs to filter

        """
        if not data_kinds:
            data_kinds = [DataKind.WEIGHT_DIFF, DataKind.WEIGHTS]

        super().__init__(supported_data_kinds=[DataKind.WEIGHTS, DataKind.WEIGHT_DIFF], data_kinds_to_filter=data_kinds)

        self.logger.info("Using HE model decryptor.")
        self.tenseal_context = None
        self.tenseal_context_file = tenseal_context_file
        self.data_kinds = data_kinds

        decomposers.register()

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def decryption(self, params: dict, encrypted_layers: dict, fl_ctx: FLContext):

        pass

    def process_dxo(self, dxo: DXO, shareable: Shareable, fl_ctx: FLContext) -> Union[None, DXO]:
        """Filter process apply to the Shareable object.

        Args:
            dxo: Data Exchange Object
            shareable: shareable
            fl_ctx: FLContext

        Returns: DXO object with decrypted weights

        """
        pass
