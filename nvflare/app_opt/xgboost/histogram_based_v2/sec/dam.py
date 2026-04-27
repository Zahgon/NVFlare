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
import struct
from io import BytesIO
from typing import List

SIGNATURE = "NVDADAM1"  # DAM (Direct Accessible Marshalling) V1
PREFIX_LEN = 24

DATA_TYPE_INT = 1
DATA_TYPE_FLOAT = 2
DATA_TYPE_STRING = 3
DATA_TYPE_INT_ARRAY = 257
DATA_TYPE_FLOAT_ARRAY = 258


class DamEncoder:
    def __init__(self, data_set_id: int):
        self.data_set_id = data_set_id
        self.entries = []
        self.buffer = BytesIO()

    def add_int_array(self, value: List[int]):
        pass

    def add_float_array(self, value: List[float]):
        pass

    def finish(self) -> bytes:
        pass

    def write_int64(self, value: int):
        pass

    def write_float(self, value: float):
        pass

    def write_str(self, value: str):
        pass


class DamDecoder:
    def __init__(self, buffer: bytes):
        self.buffer = buffer
        self.pos = 0
        if len(buffer) >= PREFIX_LEN:
            self.signature = self.read_string(8)
            self.size = self.read_int64()
            self.data_set_id = self.read_int64()
        else:
            self.signature = None
            self.size = 0
            self.data_set_id = 0

    def is_valid(self):
        pass

    def get_data_set_id(self):
        pass

    def decode_int_array(self) -> List[int]:
        pass

    def decode_float_array(self):
        pass

    def read_string(self, length: int) -> str:
        pass

    def read_int64(self) -> int:
        pass

    def read_float(self) -> float:
        pass
