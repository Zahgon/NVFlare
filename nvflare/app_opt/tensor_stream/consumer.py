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

from safetensors.torch import load as load_safetensors

from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReturnCode, Shareable, make_reply
from nvflare.apis.streaming import ConsumerFactory, ObjectConsumer, StreamContext
from nvflare.fuel.utils.log_utils import get_obj_logger

from .types import TensorBlobKeys, TensorCustomKeys, TensorsMap
from .utils import update_params_with_tensors


class TensorConsumerFactory(ConsumerFactory):
    """Factory for creating TensorConsumer instances.

    Methods:
        get_consumer(stream_ctx, fl_ctx): Creates and returns a TensorConsumer instance.
    """

    def get_consumer(self, stream_ctx: StreamContext, fl_ctx: FLContext) -> ObjectConsumer:
        pass


class TensorConsumer(ObjectConsumer):
    """TensorConsumer handles receiving and reconstructing torch tensors from a stream of byte objects.

    Attributes:
        logger: Logger for logging messages.
        tensors_map: Dictionary to store received tensors.
        total_bytes: Dictionary to track total bytes received per root key.
        num_tensors: Dictionary to track number of tensors received per root key.
        task_ids: Set to track unique task IDs received.
    """

    def __init__(self, stream_ctx: StreamContext, fl_ctx: FLContext):
        """Initialize the TensorConsumer.

        Args:
            stream_ctx (StreamContext): The stream context for the current operation. (not used)
            fl_ctx (FLContext): The FL context for the current operation. (not used)
        """
        self.logger = get_obj_logger(self)
        self.params: TensorsMap = {}
        self.total_bytes: int = 0
        self.num_tensors: int = 0
        self.task_ids: set[str] = set()

    def consume(
        self,
        shareable: Shareable,
        stream_ctx: StreamContext,
        fl_ctx: FLContext,
    ) -> tuple[bool, Shareable]:
        """Consume a shareable object and extract tensors.

        Args:
            shareable (Shareable): The shareable object containing tensor data.
            stream_ctx (StreamContext): The stream context for the current operation. (not used)
            fl_ctx (FLContext): The FL context for the current operation. (not used)

        Returns:
            tuple[bool, Shareable]: A tuple containing a success flag and a reply shareable.
        """
        pass

    def process_shareable(
        self,
        shareable: Shareable,
    ):
        """Process a received shareable object containing tensor data.

        Args:
            shareable (Shareable): The shareable object containing tensor data.

        Raises:
            ValueError: If the shareable object is invalid or contains errors.
        """
        pass

    def finalize(self, stream_ctx: StreamContext, fl_ctx: FLContext):
        """Finalize the consumer, ensuring all data is written and resources are released.

        It updates the FLContext with the received tensors.

        Args:
            stream_ctx (StreamContext): The stream context. (not used)
            fl_ctx (FLContext): The FL context. (not used)
        """
        pass

    def log_received(self, task_id: str, identity: str, peer_name: str):
        """Log the received tensors for debugging purposes.

        Args:
            identity (str): The identity of the peer.
            peer_name (str): The name of the peer.
            tensor_keys (list[str]): The keys of the received tensors.
        """
        pass
