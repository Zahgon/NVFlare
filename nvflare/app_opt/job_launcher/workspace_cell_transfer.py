# Copyright (c) 2026, NVIDIA CORPORATION.  All rights reserved.
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
"""CellNet-based workspace transfer for launched jobs.

The parent process exposes a small transfer service on its existing CellNet cell.
Launched job pods create short-lived bootstrap child cells to:

1. request a workspace bundle from the parent
2. upload final job results back to the parent

The actual payload transfer uses the existing F3 file downloader infrastructure,
so large bundles move in chunks instead of being buffered into a single message.
"""
from __future__ import annotations

import hashlib
import logging
import os
import secrets
import shutil
import stat
import tempfile
import threading
import time
import zipfile
from dataclasses import dataclass
from pathlib import PurePosixPath

from nvflare.fuel.f3.cellnet.cell import Cell
from nvflare.fuel.f3.cellnet.defs import MessageHeaderKey, ReturnCode
from nvflare.fuel.f3.cellnet.fqcn import FQCN
from nvflare.fuel.f3.cellnet.net_agent import NetAgent
from nvflare.fuel.f3.cellnet.utils import make_reply, new_cell_message
from nvflare.fuel.f3.drivers.driver_params import DriverParams
from nvflare.fuel.f3.message import Message
from nvflare.fuel.f3.streaming.download_service import DownloadService
from nvflare.fuel.f3.streaming.file_downloader import add_file, download_file
from nvflare.fuel.f3.streaming.obj_downloader import ObjectDownloader
from nvflare.fuel.sec.authn import set_add_auth_headers_filters
from nvflare.private.defs import AUTH_CLIENT_NAME_FOR_SJ
from nvflare.security.logging import secure_format_exception

logger = logging.getLogger(__name__)

ENV_WORKSPACE_OWNER_FQCN = "NVFL_WORKSPACE_OWNER_FQCN"
ENV_WORKSPACE_TRANSFER_TOKEN = "NVFL_WORKSPACE_TRANSFER_TOKEN"

WORKSPACE_TRANSFER_CHANNEL = "workspace_transfer"
TOPIC_PREPARE_DOWNLOAD = "prepare_download"
TOPIC_PUBLISH_RESULTS = "publish_results"

DOWNLOAD_TIMEOUT = 600.0
PER_REQUEST_TIMEOUT = 300.0
BOOTSTRAP_CONNECT_TIMEOUT = 30.0
BOOTSTRAP_CONNECT_POLL_INTERVAL = 0.1

_BOOTSTRAP_CELL_PREFIX = "ws_transfer_"
_WORKSPACE_DOWNLOAD_EXCLUDES = frozenset({"local/study_data_pvc.yaml"})


@dataclass
class _JobTransferRecord:
    job_id: str
    workspace_root: str
    transfer_token: str
    download_tx_id: str = ""
    download_bundle_path: str = ""


def _write_dir_to_zip(zf: zipfile.ZipFile, src: str, root: str, excluded_paths: frozenset[str] = frozenset()) -> None:
    pass


def _zip_workspace_to_file(workspace_root: str, job_id: str, file_path: str) -> None:
    pass


def _zip_results_to_file(workspace_root: str, job_id: str, file_path: str) -> None:
    pass


def _validate_relative_zip_members(zf: zipfile.ZipFile) -> None:
    pass


def _validate_job_zip_members(zf: zipfile.ZipFile, job_id: str) -> None:
    pass


def _hash_file(path: str) -> str:
    pass


def make_workspace_transfer_fqcn(owner_fqcn: str, job_id: str) -> str:
    pass


def _cleanup_files(paths) -> None:
    pass


def _cleanup_transfer_files(_tx_id: str, _status: str, _objects: list, temp_paths=None, **_kwargs) -> None:
    pass


def _cleanup_download(tx_id: str, bundle_path: str) -> None:
    pass


def _make_error(message: str, rc: str = ReturnCode.INVALID_REQUEST) -> Message:
    pass


class WorkspaceTransferManager:
    """Manage per-job workspace transfer over an existing CellNet cell."""

    def __init__(
        self,
        cell: Cell,
        download_timeout: float = DOWNLOAD_TIMEOUT,
        per_request_timeout: float = PER_REQUEST_TIMEOUT,
    ):
        self.cell = cell
        self.owner_fqcn = cell.get_fqcn()
        self.download_timeout = download_timeout
        self.per_request_timeout = per_request_timeout
        self.jobs: dict[str, _JobTransferRecord] = {}
        self._lock = threading.Lock()

        self.cell.register_request_cb(
            channel=WORKSPACE_TRANSFER_CHANNEL,
            topic=TOPIC_PREPARE_DOWNLOAD,
            cb=self._handle_prepare_download,
        )
        self.cell.register_request_cb(
            channel=WORKSPACE_TRANSFER_CHANNEL,
            topic=TOPIC_PUBLISH_RESULTS,
            cb=self._handle_publish_results,
        )

    @classmethod
    def get_or_create(cls, cell: Cell) -> "WorkspaceTransferManager":
        """Return the per-cell manager, constructing one on first use."""
        pass

    def add_job(self, job_id: str, workspace_root: str) -> str:
        pass

    def remove_job(self, job_id: str) -> None:
        pass

    def _get_record(self, job_id: str) -> _JobTransferRecord | None:
        pass

    def _authorize(self, request: Message, action: str) -> tuple[_JobTransferRecord | None, str, Message | None]:
        """Validate request payload and token. Returns (record, origin, error_reply)."""
        pass

    def _handle_prepare_download(self, request: Message) -> Message:
        pass

    def _download_transaction_done(self, tx_id: str, _status: str, objects: list, job_id: str) -> None:
        pass

    def _handle_publish_results(self, request: Message) -> Message:
        pass


# Process-level singleton. download_workspace runs at startup and
# upload_results runs at shutdown inside the SAME process, so they share
# one bootstrap cell for the life of the job. Creating a second cell with
# the same FQCN crashes CellNet's registry ("there is already a cell
# named ..."), and nothing in CellNet unregisters the name reliably after
# cell.stop(), so keeping one alive is the simplest contract.
_bootstrap_cell: Cell | None = None
_bootstrap_net_agent: NetAgent | None = None
_bootstrap_lock = threading.Lock()


def _get_bootstrap_cell(args, owner_fqcn: str, secure_mode: bool) -> Cell:
    pass


def _close_bootstrap_cell() -> None:
    pass


def _get_root_url(args) -> str:
    pass


def _get_bootstrap_tls_pair(startup_dir: str, owner_fqcn: str) -> tuple[str, str, str, str]:
    pass


def _create_bootstrap_cell(args, owner_fqcn: str, secure_mode: bool) -> tuple[Cell, NetAgent]:
    pass


def _wait_for_bootstrap_ready(cell: Cell, owner_fqcn: str, timeout: float = BOOTSTRAP_CONNECT_TIMEOUT) -> None:
    pass


def _request_workspace_bundle(cell: Cell, owner_fqcn: str, job_id: str, transfer_token: str) -> dict:
    pass


def download_workspace(args, secure_mode: bool) -> None:
    pass


def upload_results(args, secure_mode: bool) -> None:
    pass


def upload_results_safely(args, secure_mode: bool, log=None) -> None:
    pass
