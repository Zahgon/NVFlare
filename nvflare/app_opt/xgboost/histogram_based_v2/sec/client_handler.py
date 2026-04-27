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
import os
import time

import xgboost
from packaging import version

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.app_opt.xgboost.histogram_based_v2.aggr import Aggregator
from nvflare.app_opt.xgboost.histogram_based_v2.defs import Constant
from nvflare.app_opt.xgboost.histogram_based_v2.sec.dam import DamDecoder
from nvflare.app_opt.xgboost.histogram_based_v2.sec.data_converter import FeatureAggregationResult
from nvflare.app_opt.xgboost.histogram_based_v2.sec.partial_he.adder import Adder
from nvflare.app_opt.xgboost.histogram_based_v2.sec.partial_he.decrypter import Decrypter
from nvflare.app_opt.xgboost.histogram_based_v2.sec.partial_he.encryptor import Encryptor
from nvflare.app_opt.xgboost.histogram_based_v2.sec.partial_he.util import (
    combine,
    decode_encrypted_data,
    decode_feature_aggregations,
    encode_encrypted_data,
    encode_feature_aggregations,
    generate_keys,
    ipcl_imported,
    split,
)
from nvflare.app_opt.xgboost.histogram_based_v2.sec.processor_data_converter import (
    DATA_SET_HISTOGRAMS,
    ProcessorDataConverter,
)
from nvflare.app_opt.xgboost.histogram_based_v2.sec.sec_handler import SecurityHandler

try:
    import tenseal as ts
    from tenseal.tensors.ckksvector import CKKSVector

    from nvflare.app_opt.he import decomposers
    from nvflare.app_opt.he.homomorphic_encrypt import load_tenseal_context_from_workspace

    tenseal_imported = True
    tenseal_error = None
except Exception as ex:
    tenseal_imported = False
    tenseal_error = f"Import error: {ex}"

XGBOOST_MIN_VERSION = "2.2.0-dev"


class ClientSecurityHandler(SecurityHandler):
    def __init__(self, key_length=1024, num_workers=10, tenseal_context_file="client_context.tenseal"):
        FLComponent.__init__(self)
        self.num_workers = num_workers
        self.key_length = key_length
        self.public_key = None
        self.private_key = None
        self.encryptor = None
        self.adder = None
        self.decrypter = None
        self.data_converter = ProcessorDataConverter()
        self.encrypted_ghs = None
        self.clear_ghs = None  # for label client: list of tuples (g, h)
        self.original_gh_buffer = None
        self.feature_masks = None
        self.aggregator = Aggregator()
        self.aggr_result = None  # for label client: computed aggr result based on clear-text clear_ghs
        self.tenseal_context_file = tenseal_context_file
        self.tenseal_context = None

        if tenseal_imported:
            decomposers.register()

    def _process_before_broadcast(self, fl_ctx: FLContext):
        pass

    def _process_after_broadcast(self, fl_ctx: FLContext):
        # this is called when the bcst result is received from the server
        pass

    def _process_before_all_gather_v(self, fl_ctx: FLContext):
        pass

    def _process_before_all_gather_v_vertical(self, fl_ctx: FLContext):
        pass

    def _process_before_all_gather_v_horizontal(self, fl_ctx: FLContext):
        pass

    def _do_aggregation(self, groups, fl_ctx: FLContext):
        # this is only for the label-client to compute aggregation in clear-text!
        pass

    def _decrypt_aggr_result(self, encoded, fl_ctx: FLContext):
        # decrypt aggr result from a client
        pass

    def _process_after_all_gather_v(self, fl_ctx: FLContext):
        # called after AllGatherV result is received from the server
        pass

    def _process_after_all_gather_v_vertical(self, fl_ctx: FLContext):
        pass

    def _process_after_all_gather_v_horizontal(self, fl_ctx: FLContext):
        pass

    def _check_xgboost_version(self, disable_version_check: bool) -> bool:
        """Check XGBoost version. Returns true if it supports secure training"""
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass
