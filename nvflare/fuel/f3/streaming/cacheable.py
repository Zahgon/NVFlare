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
import threading
from abc import abstractmethod
from typing import Any, List, Optional, Tuple

from nvflare.fuel.f3.streaming.download_service import Consumer, Downloadable, DownloadService, ProduceRC
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.fuel.utils.validation_utils import check_non_negative_int


class _StateKey:
    START = "start"
    COUNT = "count"


class CacheableObject(Downloadable):
    """This class provides cache capability for managing chunks generated during streaming.
    When the object is to be sent to multiple receivers, each chunk is generated only once and cached for other
    receivers. Once all receivers received the chunk, it's removed from the cache.

    """

    def __init__(self, obj: Any, max_chunk_size: int):
        """Constructor of CacheableObject.

        Args:
            obj: the object to be downloaded.
            max_chunk_size: max number of bytes for each chunk.

        Notes: The object must be able to be divided into multiple items. A chunk is generated for each item.
        """
        super().__init__(obj)
        check_non_negative_int("max_chunk_size", max_chunk_size)
        self.max_chunk_size = max_chunk_size
        self.size = self.get_item_count()
        self.cache: list[tuple[Optional[bytes], int]] = [(None, 0)] * self.size
        self.lock = threading.Lock()
        self.num_receivers = 0
        self.logger = get_obj_logger(self)

    @abstractmethod
    def get_item_count(self) -> int:
        """The subclass must implement this method to return the number of items the object contains.

        Returns: the number of items the object contains

        """
        pass

    @abstractmethod
    def produce_item(self, index: int) -> bytes:
        """This method is called to produce the chunk for the specified item.

        Args:
            index: index of the item.

        Returns: a chunk for the item

        """
        pass

    def set_transaction(self, tx_id, ref_id):
        pass

    def downloaded_to_all(self):
        pass

    def transaction_done(self, transaction_id: str, status: str):
        pass

    def clear_cache(self):
        """Clear the chunk cache only.

        Does NOT touch base_obj — the source object is released separately
        via release() after the transaction_done_cb has been invoked, so the
        callback can still observe the original data if needed.
        """
        pass

    def release(self):
        """Drop the reference to the source object.

        Called by _Transaction.transaction_done() AFTER the transaction_done_cb
        fires.  Setting base_obj to None drops the last infrastructure reference
        to the source data (e.g. a 5 GiB numpy dict), allowing it to be
        reclaimed by the GC immediately rather than waiting for a future cycle.

        Overrides Downloadable.release() (which is a no-op by default).
        """
        pass

    def _get_item(self, index: int, requester: str) -> bytes:
        pass

    def _adjust_cache(self, start: int, count: int):
        pass

    def produce(self, state: dict, requester: str) -> Tuple[str, Any, dict]:
        pass


class ItemConsumer(Consumer):

    def __init__(self):
        super().__init__()
        self.error = None
        self.result = None

    @abstractmethod
    def consume_items(self, items: List[Any], result: Any) -> Any:
        """Process items and return updated result."""
        pass

    def consume(self, ref_id: str, state: dict, data: Any) -> dict:
        pass

    def download_failed(self, ref_id, reason: str):
        pass

    def download_completed(self, ref_id: str):
        pass
