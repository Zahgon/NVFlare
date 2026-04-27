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

import tenseal as ts

from nvflare.lighter.constants import ProvFileName
from nvflare.lighter.spec import Builder, Project, ProvisionContext


class HEBuilder(Builder):
    def __init__(
        self,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=None,
        scale_bits=40,
        scheme="CKKS",
    ):
        """Build Homomorphic related contents.

        Generates Tenseal homomorphic encryption context for server and client and writes them to server and client
        participant folders.

        Args:
            poly_modulus_degree: defaults to 8192.
            coeff_mod_bit_sizes: defaults to [60, 40, 40].
            scale_bits: defaults to 40.
            scheme: defaults to "CKKS".
        """
        if not coeff_mod_bit_sizes:
            coeff_mod_bit_sizes = [60, 40, 40]

        self._context = None
        self.scheme_type_mapping = {
            "CKKS": ts.SCHEME_TYPE.CKKS,
            "BFV": ts.SCHEME_TYPE.BFV,
        }
        self.poly_modulus_degree = poly_modulus_degree
        self.coeff_mod_bit_sizes = coeff_mod_bit_sizes
        self.scale_bits = scale_bits
        _scheme = scheme
        # Setup TenSEAL context
        self.scheme_type = self.scheme_type_mapping[_scheme]
        self.serialized = None

    def initialize(self, project: Project, ctx: ProvisionContext):
        pass

    def build(self, project: Project, ctx: ProvisionContext):
        pass

    def get_serialized_context(self, is_client=False):
        pass
