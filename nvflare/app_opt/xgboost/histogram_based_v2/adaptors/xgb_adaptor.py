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

from abc import ABC, abstractmethod
from typing import Tuple

from nvflare.apis.fl_constant import ReturnCode
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import Shareable
from nvflare.apis.utils.reliable_message import PROP_KEY_DEBUG_INFO, ReliableMessage
from nvflare.app_opt.xgboost.histogram_based_v2.defs import Constant
from nvflare.fuel.f3.cellnet.fqcn import FQCN
from nvflare.fuel.utils.validation_utils import check_non_negative_int, check_positive_int

from .adaptor import AppAdaptor

XGB_APP_NAME = "XGBoost"


class XGBServerAdaptor(AppAdaptor):
    """XGBServerAdaptor specifies commonly required methods for server adaptor implementations.

    For example, an XGB server could be run as a gRPC server process, or be run as part of the FLARE's FL server
    process. Similarly, an XGB client could be run as a gRPC client process, or be run as part of the
    FLARE's FL client process.

    Each type of XGB Target requires an appropriate adaptor to integrate it with FLARE's XGB Controller or Executor.

    """

    def __init__(self, in_process: bool):
        AppAdaptor.__init__(self, XGB_APP_NAME, in_process)
        self.world_size = None

    def configure(self, config: dict, fl_ctx: FLContext):
        """Called by XGB Controller to configure the target.

        The world_size is a required config parameter.

        Args:
            config: config data
            fl_ctx: FL context

        Returns: None

        """
        pass

    @abstractmethod
    def all_gather(self, rank: int, seq: int, send_buf: bytes, fl_ctx: FLContext) -> bytes:
        """Called by the XGB Controller to perform Allgather operation, per XGBoost spec.

        Args:
            rank: rank of the calling client
            seq: sequence number of the request
            send_buf: operation input data
            fl_ctx: FL context

        Returns: operation result

        """
        pass

    @abstractmethod
    def all_gather_v(self, rank: int, seq: int, send_buf: bytes, fl_ctx: FLContext) -> bytes:
        """Called by the XGB Controller to perform AllgatherV operation, per XGBoost spec.

        Args:
            rank: rank of the calling client
            seq: sequence number of the request
            send_buf: input data
            fl_ctx: FL context

        Returns: operation result

        """
        pass

    @abstractmethod
    def all_reduce(
        self,
        rank: int,
        seq: int,
        data_type: int,
        reduce_op: int,
        send_buf: bytes,
        fl_ctx: FLContext,
    ) -> bytes:
        """Called by the XGB Controller to perform Allreduce operation, per XGBoost spec.

        Args:
            rank: rank of the calling client
            seq: sequence number of the request
            data_type: data type of the input
            reduce_op: reduce operation to be performed
            send_buf: input data
            fl_ctx: FL context

        Returns: operation result

        """
        pass

    @abstractmethod
    def broadcast(self, rank: int, seq: int, root: int, send_buf: bytes, fl_ctx: FLContext) -> bytes:
        """Called by the XGB Controller to perform Broadcast operation, per XGBoost spec.

        Args:
            rank: rank of the calling client
            seq: sequence number of the request
            root: root rank of the broadcast
            send_buf: input data
            fl_ctx: FL context

        Returns: operation result

        """
        pass


class XGBClientAdaptor(AppAdaptor, ABC):
    """XGBClientAdaptor specifies commonly required methods for client adaptor implementations."""

    def __init__(self, in_process: bool, per_msg_timeout: float, tx_timeout: float):
        """Constructor of XGBClientAdaptor.

        Args:
            in_process (bool):
            per_msg_timeout (float): Number of seconds to wait for each message before timing out.
            tx_timeout (float): Timeout for the entire transaction.
        """
        AppAdaptor.__init__(self, XGB_APP_NAME, in_process)
        self.engine = None
        self.stopped = False
        self.rank = None
        self.num_rounds = None
        self.data_split_mode = None
        self.secure_training = None
        self.xgb_params = None
        self.xgb_options = None
        self.disable_version_check = None
        self.world_size = None
        self.per_msg_timeout = per_msg_timeout
        self.tx_timeout = tx_timeout

    def _check_rank(self, ranks: dict, site_name: str):
        pass

    def configure(self, config: dict, fl_ctx: FLContext):
        """Called by XGB Executor to configure the target.

        The rank, world size, and number of rounds are required config parameters.

        Args:
            config: config data
            fl_ctx: FL context

        Returns: None

        """
        pass

    def _send_request(self, op: str, req: Shareable) -> Tuple[bytes, Shareable]:
        """Send XGB operation request to the FL server via FLARE message.

        Args:
            op: the XGB operation
            req: operation data

        Returns: operation result

        """
        pass

    def _send_all_gather(self, rank: int, seq: int, send_buf: bytes) -> Tuple[bytes, Shareable]:
        """This method is called by a concrete client adaptor to send Allgather operation to the server.

        Args:
            rank: rank of the client
            seq: sequence number of the request
            send_buf: input data

        Returns: operation result

        """
        pass

    def _send_all_gather_v(self, rank: int, seq: int, send_buf: bytes, headers=None) -> Tuple[bytes, Shareable]:
        pass

    def _do_all_gather_v(self, rank: int, seq: int, send_buf: bytes) -> Tuple[bytes, Shareable]:
        """This method is called by a concrete client adaptor to send AllgatherV operation to the server.

        Args:
            rank: rank of the client
            seq: sequence number of the request
            send_buf: operation input

        Returns: operation result

        """
        pass

    def _send_all_reduce(
        self, rank: int, seq: int, data_type: int, reduce_op: int, send_buf: bytes
    ) -> (bytes, Shareable):
        """This method is called by a concrete client adaptor to send Allreduce operation to the server.

        Args:
            rank: rank of the client
            seq: sequence number of the request
            data_type: data type of the input
            reduce_op: reduce operation to be performed
            send_buf: operation input

        Returns: operation result

        """
        pass

    def _send_broadcast(self, rank: int, seq: int, root: int, send_buf: bytes, headers=None) -> Tuple[bytes, Shareable]:
        pass

    def _do_broadcast(self, rank: int, seq: int, root: int, send_buf: bytes) -> bytes:
        """This method is called by a concrete client adaptor to send Broadcast operation to the server.

        Args:
            rank: rank of the client
            seq: sequence number of the request
            root: root rank of the broadcast
            send_buf: operation input

        Returns: operation result

        """
        pass

    @staticmethod
    def _add_headers(req: Shareable, headers: dict):
        pass
