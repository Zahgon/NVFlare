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

"""PT lazy tensor references used by tensor disk offload.

When `enable_tensor_disk_offload=True`, incoming streamed tensor payloads are written
to temporary safetensors files instead of being fully deserialized into memory.
`LazyTensorDict` maps item IDs to on-disk files, and `_LazyRef` defers loading until
`materialize()` is called by aggregation code.

This keeps peak memory lower for large models while still allowing deterministic
explicit cleanup via `cleanup()`, with GC as a fallback through `_TempDirRef`.
"""

import logging
import shutil

from safetensors import safe_open

logger = logging.getLogger(__name__)


def _cleanup_temp_dir(path: str) -> None:
    pass


class _TempDirRef:
    """Reference-counted sentinel for a temp directory.

    Shared between LazyTensorDict and all _LazyRef instances created from it.
    The directory is deleted only when ALL holders are garbage collected.
    """

    def __init__(self, temp_dir: str):
        self.path = temp_dir
        self._deleted = False

    def cleanup(self):
        pass

    def __del__(self):
        self.cleanup()


class _LazyRef:
    """Lightweight placeholder for an on-disk tensor.

    Carries only file_path + key (~100 bytes). The tensor is loaded from disk
    only when materialize() is called, keeping memory near zero until then.

    Holds a reference to _TempDirRef to prevent premature cleanup.
    """

    def __init__(self, file_path: str, key: str, temp_ref: _TempDirRef):
        self.file_path = file_path
        self.key = key
        self._temp_ref = temp_ref

    def materialize(self):
        """Load tensor from safetensors file. Opens mmap, copies data out, closes mmap."""
        pass

    def __repr__(self):
        return f"_LazyRef({self.file_path!r}, key={self.key!r})"


class LazyTensorDict:
    """Dict-like mapping of FOBS item_ids to on-disk safetensors files.

    Each entry maps an item_id to a (file_path, key) pair. Tensors are loaded
    via safetensors safe_open (mmap) on access.
    """

    def __init__(self, key_to_file: dict[str, tuple[str, str]], temp_dir: str):
        self._key_to_file = key_to_file
        self._temp_ref = _TempDirRef(temp_dir)

    def __getitem__(self, key):
        file_path, st_key = self._key_to_file[key]
        with safe_open(file_path, framework="pt") as f:
            return f.get_tensor(st_key)

    def get(self, key, default=None):
        pass

    def keys(self):
        pass

    def __iter__(self):
        return iter(self._key_to_file)

    def items(self):
        pass

    def values(self):
        pass

    def __len__(self):
        return len(self._key_to_file)

    def __contains__(self, key):
        return key in self._key_to_file

    def make_lazy_ref(self, key) -> "_LazyRef":
        pass

    def cleanup(self):
        pass
