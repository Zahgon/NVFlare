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
"""Decomposers for types from app_common and Machine Learning libraries."""
import os
from abc import ABC
from io import BytesIO
from typing import Any, Tuple

import numpy as np

import nvflare.fuel.utils.fobs.dots as dots
from nvflare.app_common.np.np_downloader import ArrayDownloadable, download_arrays
from nvflare.fuel.f3.cellnet.cell import Cell
from nvflare.fuel.f3.streaming.download_service import Downloadable
from nvflare.fuel.utils import fobs
from nvflare.fuel.utils.fobs.datum import DatumManager
from nvflare.fuel.utils.fobs.decomposers.via_downloader import ViaDownloaderDecomposer

_NPZ_EXTENSION = ".npz"


class NumpyScalarDecomposer(fobs.Decomposer, ABC):
    """Decomposer base class for all numpy types with item method."""

    def decompose(self, target: Any, manager: DatumManager = None) -> Any:
        pass

    def recompose(self, data: Any, manager: DatumManager = None) -> np.ndarray:
        pass


class Float64ScalarDecomposer(NumpyScalarDecomposer):
    def supported_type(self):
        pass


class Float32ScalarDecomposer(NumpyScalarDecomposer):
    def supported_type(self):
        pass


class Int64ScalarDecomposer(NumpyScalarDecomposer):
    def supported_type(self):
        pass


class Int32ScalarDecomposer(NumpyScalarDecomposer):
    def supported_type(self):
        pass


class NumpyArrayDecomposer(ViaDownloaderDecomposer):

    def __init__(self):
        ViaDownloaderDecomposer.__init__(self, 1024 * 1024 * 2, "np_")

    def supported_type(self):
        pass

    def get_download_dot(self) -> int:
        pass

    def to_downloadable(self, items: dict, max_chunk_size: int, fobs_ctx: dict) -> Downloadable:
        pass

    def download(
        self,
        from_fqcn: str,
        ref_id: str,
        per_request_timeout: float,
        cell: Cell,
        secure=False,
        optional=False,
        abort_signal=None,
    ) -> Tuple[str, dict]:
        pass

    def native_decompose(self, target: np.ndarray, manager: DatumManager = None) -> bytes:
        pass

    def native_recompose(self, data: bytes, manager: DatumManager = None) -> np.ndarray:
        pass


def register():
    pass


register.registered = False
