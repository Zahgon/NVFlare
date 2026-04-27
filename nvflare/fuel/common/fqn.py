# Copyright (c) 2023, NVIDIA CORPORATION.  All rights reserved.
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
import re
from typing import List


class FQN:

    SEPARATOR = "."
    ROOT_SERVER = "server"

    @staticmethod
    def normalize(fqn: str) -> str:
        pass

    @staticmethod
    def split(fqn: str) -> List[str]:
        pass

    @staticmethod
    def join(path: List[str]) -> str:
        pass

    @staticmethod
    def validate(fqn) -> str:
        pass

    @staticmethod
    def get_root(fqn: str) -> str:
        pass

    @staticmethod
    def get_parent(fqn: str) -> str:
        pass

    @staticmethod
    def is_parent(fqn1: str, fqn2: str) -> bool:
        pass

    @staticmethod
    def is_ancestor(fqn1: str, fqn2: str) -> bool:
        pass
