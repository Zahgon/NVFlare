# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
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

from collections import defaultdict

from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.streaming import StreamableEngine, StreamContext
from nvflare.fuel.utils.log_utils import get_obj_logger

from .producer import TensorProducer
from .types import TENSORS_CHANNEL, TensorsMap
from .utils import get_dxo_from_ctx, get_targets_from_ctx_and_prop_key, get_topic_for_ctx_prop_key


class TensorSender:
    """Handles sending tensors between server and clients."""

    def __init__(
        self,
        engine: StreamableEngine,
        ctx_prop_key: str,
        format: str,
        tasks: list[str],
        channel: str = TENSORS_CHANNEL,
    ):
        """Initialize the TensorSender.

        Args:
            engine (StreamableEngine): The streamable engine to use for streaming.
            format (str): The format of the tensors to send.
            tasks (list[str]): The list of tasks to send tensors for.
            ctx_prop_key (str): The context property key to send tensors for.
            channel (str): The channel to use for streaming. Default is TENSORS_CHANNEL.
        """
        self.engine = engine
        self.ctx_prop_key = ctx_prop_key
        self.format = format
        self.tasks = tasks
        self.channel = channel
        # key: task_id, value: tensors to send to the peer
        self.task_params: dict[str, TensorsMap] = defaultdict(dict)
        self.logger = get_obj_logger(self)

    def store_tensors(self, fl_ctx: FLContext):
        """Parse tensors from the FLContext and store them for sending.

        Args:
            fl_ctx (FLContext): The FLContext for the current operation.
        """
        pass

    def send(
        self,
        fl_ctx: FLContext,
        tensor_send_timeout: float,
    ) -> None:
        """Send tensors to the peer.

        Args:
            fl_ctx (FLContext): The FLContext for the current operation.
            tensor_send_timeout (float): Timeout for each tensor entry transfer.
        """
        pass

    def _send_tensors(self, targets: list[str], producer: TensorProducer, fl_ctx: FLContext):
        """Send tensors to the peer using the StreamableEngine."""
        pass
