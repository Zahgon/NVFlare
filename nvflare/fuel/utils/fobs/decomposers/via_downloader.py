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
import json
import threading
import uuid
from abc import ABC, abstractmethod
from typing import Any

import nvflare.fuel.utils.app_config_utils as acu
from nvflare.apis.fl_constant import ConfigVarName
from nvflare.fuel.f3.cellnet.cell import Cell
from nvflare.fuel.f3.cellnet.defs import MessageHeaderKey
from nvflare.fuel.f3.streaming.download_service import Downloadable
from nvflare.fuel.f3.streaming.file_downloader import ObjectDownloader
from nvflare.fuel.utils import fobs
from nvflare.fuel.utils.fobs.datum import Datum, DatumManager, DatumType
from nvflare.fuel.utils.log_utils import get_obj_logger

MIN_DOWNLOAD_TIMEOUT_DEFAULT = 300  # inactivity timeout between chunk requests; 5 min covers GC pauses
_MIN_DOWNLOAD_TIMEOUT = MIN_DOWNLOAD_TIMEOUT_DEFAULT  # backward-compat alias

# Thread-local flag for synchronous download-initiation detection.
# Task pipe and metric pipe share the same CoreCell (same site_name + token + mode
# → same FQCN → same _CellInfo cache entry → same core_cell.fobs_ctx).  A plain
# fobs_ctx flag would be clobbered by concurrent serialisation calls from different
# threads on the same cell.  Thread-local gives per-thread isolation because
# _finalize_download_tx() is always called synchronously in the thread that invoked
# send_to_peer() → encode_payload() → FOBS serialisation.
_tls = threading.local()


def was_download_initiated() -> bool:
    """Return True if _finalize_download_tx() created a download transaction in
    the current thread's most recent encode_payload() call.

    Called by FlareAgent._do_submit_result() immediately after send_to_peer()
    returns to decide whether to wait for the server to finish downloading tensors.
    Returns False for validate results (metrics only, no tensors).
    """
    pass


def clear_download_initiated() -> None:
    """Reset the thread-local flag before a send_to_peer() call.

    Prevents a stale True from a previous training round (which did have tensors)
    from carrying over to the current validate round (which has no tensors).
    """
    pass


class LazyDownloadRef:
    """Placeholder created in PASS_THROUGH mode instead of downloading a tensor.

    When a cell is configured as a pure forwarder (``FOBSContextKey.PASS_THROUGH``
    is set in its FOBS context), incoming download references from the source are
    not resolved.  Instead a ``LazyDownloadRef`` is created for each tensor item
    in the received batch so that the original source FQCN and batch ref_id are
    preserved.

    When the forwarding node (CJ) later serialises the task for its subprocess,
    ``LazyDownloadRefDecomposer.decompose()`` detects ``LazyDownloadRef`` targets
    and re-emits the *original* download datum (pointing back to the server)
    instead of creating a new datum that would point to the CJ.  The subprocess
    agent then resolves the references directly from the originating source,
    downloading each tensor individually without any copy passing through the CJ.

    Attributes:
        fqcn:    FQCN of the originating cell that owns the download transaction.
        ref_id:  UUID of the batch download transaction on that cell.
        item_id: Intra-batch item placeholder (e.g. ``"T0"``, ``"T1"``).
        dot:     Datum Object Type of the original download datum.  Identifies
                 which ``ViaDownloaderDecomposer`` subclass owns this ref (e.g.
                 ``NUMPY_DOWNLOAD`` or ``TENSOR_DOWNLOAD``).  Required by
                 ``LazyDownloadRefDecomposer`` to route serialisation and
                 deserialisation to the correct handler.
    """

    __slots__ = ("fqcn", "ref_id", "item_id", "dot")

    def __init__(self, fqcn: str, ref_id: str, item_id: str, dot: int = 0):
        self.fqcn = fqcn
        self.ref_id = ref_id
        self.item_id = item_id
        self.dot = dot


class _LazyBatchInfo:
    """Sentinel stored in fobs_ctx[items_key] during PASS_THROUGH mode.

    Carries the (fqcn, ref_id, dot) of the *original* download batch so that
    ``recompose()`` can build a ``LazyDownloadRef`` for each item_id it
    encounters.  Using a named sentinel class (rather than a plain tuple)
    makes the PASS_THROUGH path unambiguous and robust against accidental
    type collisions.
    """

    __slots__ = ("fqcn", "ref_id", "dot")

    def __init__(self, fqcn: str, ref_id: str, dot: int = 0):
        self.fqcn = fqcn
        self.ref_id = ref_id
        self.dot = dot


# fobs_ctx key used to carry the fqcn/ref_id batch info in PASS_THROUGH mode
# so that recompose() can build per-item LazyDownloadRefs from a single datum.
_LAZY_BATCH_CTX_SUFFIX = "_lazy_batch"


class EncKey:
    TYPE = "type"
    DATA = "data"


class EncType:
    NATIVE = "native"
    REF = "ref"


class _RefKey:
    REF_ID = "ref_id"
    FQCN = "fqcn"


class _CtxKey:
    MSG_ROOT_ID = "msg_root_id"
    MSG_ROOT_TTL = "msg_root_ttl"
    OBJECTS = "objects"  # objects to be downloaded
    FINAL_CB_REGISTERED = "final_cb_registered"


class _DecomposeCtx:

    def __init__(self):
        self.target_to_item = {}  # target_id => item_id
        self.target_items = {}  # item_id => item value
        self.last_item_id = 0
        self.lock = threading.Lock()

    def add_item(self, item: Any):
        pass

    def get_item_count(self):
        pass


class ViaDownloaderDecomposer(fobs.Decomposer, ABC):

    def __init__(self, max_chunk_size: int, config_var_prefix):
        self.logger = get_obj_logger(self)
        self.prefix = self.__class__.__name__
        self.decompose_ctx_key = f"{self.prefix}_dc"  # kept in fobs_ctx: each target type has its own DecomposeCtx
        self.items_key = f"{self.prefix}_items"  # in fobs_ctx: each target type has its own set of items
        self.config_var_prefix = config_var_prefix
        self.max_chunk_size = max_chunk_size

    @abstractmethod
    def to_downloadable(self, items: dict, max_chunk_size: int, fobs_ctx: dict) -> Downloadable:
        """Convert the items Downloadable object.

        Args:
            items: a dict of items of target object type to be converted
            max_chunk_size: max size of one chunk.
            fobs_ctx: FOBS Context

        Returns: a Downloadable object

        The "items" is a dict of target objects. The dict contains all objects of the target type in one payload.

        """
        pass

    @abstractmethod
    def download(
        self,
        from_fqcn: str,
        ref_id: str,
        per_request_timeout: float,
        cell: Cell,
        secure=False,
        optional=False,
        abort_signal=None,
    ) -> tuple[str, dict]:
        pass

    def supported_dots(self):
        pass

    @abstractmethod
    def get_download_dot(self) -> int:
        """Get the Datum Object Type to be used for download ref datum

        Returns: the DOT for download ref datum

        """
        pass

    @abstractmethod
    def native_decompose(self, target: Any, manager: DatumManager = None) -> bytes:
        pass

    @abstractmethod
    def native_recompose(self, data: bytes, manager: DatumManager = None) -> Any:
        pass

    def _create_ref(self, target: Any, manager: DatumManager, fobs_ctx: dict):
        # create a reference item for the target object. The ref item represents the target object in
        # the serialized payload.
        pass

    def _create_downloadable(self, fobs_ctx: dict) -> Downloadable:
        pass

    @staticmethod
    def _determine_msg_root(fobs_ctx: dict):
        pass

    def decompose(self, target: Any, manager: DatumManager = None) -> Any:
        pass

    def _create_downloader(self, fobs_ctx: dict):
        # Transaction lifecycle is managed solely by _monitor_tx() (download_service.py).
        # We deliberately do NOT subscribe to msg_root deletion here.  The msg_root is
        # deleted as soon as all blobs are delivered, but blob_cb fires asynchronously —
        # secondary tensor downloads are still in flight when msg_root is deleted.
        # Subscribing caused a race: delete_transaction() removed refs from _ref_table
        # before blob_cb could finish its _download_from_remote_cell() calls, producing
        # "no ref found" FATAL_SYSTEM_ERROR (RC12 Bug 1).
        # _monitor_tx() polls is_finished() every 5s and cleans up within 5s of the last
        # receiver completing all chunk downloads — sufficient for all model sizes.
        pass

    def _process_items_to_datum(self, mgr: DatumManager):
        """This method is called during serialization after all target items are serialized.
        For primary msg, we turn the collected items into a file, and add file info as a Datum to the datum manager.

        Args:
            mgr:

        Returns:

        """
        pass

    def _config_var_name(self, base_name: str):
        pass

    def _create_datum(self, fobs_ctx: dict):
        pass

    def _finalize_download_tx(self, mgr: DatumManager):
        pass

    def _finalize_lazy_batch(self, mgr: DatumManager):
        """Post-callback used when re-emitting a LazyDownloadRef batch.

        Adds a single datum containing the *original* source FQCN and ref_id so
        that the downstream consumer (subprocess agent) can download the tensors
        directly from the originating cell (typically the FL server) without
        involving the CJ at all.
        """
        pass

    def process_datum(self, datum: Datum, manager: DatumManager):
        """This is called by the manager to process a datum that has a DOT.
        This happens before the recompose processing.

        The datum contains information about where the data is:
        For bytes DOT, the data is included in the datum directly.
        For file DOT, the data is in a file, and the location of the file is further specified:
            - If the location is local, then the file is on local file system;
            - If the location is remote_cell, then the file is on a remote cell, and needs to be downloaded.

        Args:
            datum: datum to be processed.
            manager: the datum manager.

        Returns: None

        """
        pass

    def recompose(self, data: Any, manager: DatumManager = None) -> Any:
        pass

    def _download_from_remote_cell(self, fobs_ctx: dict, ref: dict):
        pass


class LazyDownloadRefDecomposer(fobs.Decomposer):
    """Decomposer that serialises and deserialises :class:`LazyDownloadRef` objects.

    ``LazyDownloadRef`` objects are created at a forwarding hop (e.g. the CJ
    process) when ``FOBSContextKey.PASS_THROUGH`` is set.  Instead of
    downloading tensors from the FL server, each tensor is represented as a
    lightweight placeholder that carries the original server FQCN, batch
    ref_id, item_id, and the Datum Object Type (``dot``) of the originating
    ``ViaDownloaderDecomposer`` subclass.

    When the forwarding node re-serialises the task for the subprocess agent,
    FOBS routes each ``LazyDownloadRef`` to this decomposer.

    **decompose()**
        Delegates to the ``ViaDownloaderDecomposer`` subclass identified by
        ``lazy.dot``.  That handler's ``decompose()`` re-emits the original
        server batch datum (fqcn / ref_id) via a post-callback so the
        subprocess knows exactly where to download from.  ``lazy_dot`` is
        appended to the returned encoding dict so ``recompose()`` can route
        back to the same handler.

    **recompose()**
        Uses ``lazy_dot`` to look up the original handler and delegates to
        ``handler.recompose()``.  At the subprocess, ``process_datum()`` has
        already populated ``fobs_ctx[handler.items_key]`` with the downloaded
        tensors, so the call returns the real tensor value directly.
    """

    def supported_type(self):
        pass

    def decompose(self, lazy: LazyDownloadRef, manager: DatumManager = None) -> dict:
        pass

    def recompose(self, data: dict, manager: DatumManager = None) -> Any:
        pass
