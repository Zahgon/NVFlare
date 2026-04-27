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

import argparse
import json
from typing import List, Optional

from nvflare.tool.cli_contract import SCHEMA_VERSION

_PATH_KEYWORDS = ("dir", "path", "file", "output")


def _infer_type(action: argparse.Action) -> str:
    # Stage-1 schema is inferred from argparse only; richer explicit typing can be added later if
    # commands need stronger MCP/tool contracts than these naming heuristics provide.
    pass


def parser_to_schema(
    parser: argparse.ArgumentParser,
    command: str,
    examples: Optional[List[str]] = None,
    deprecated: bool = False,
    deprecated_message: str = "",
) -> dict:
    """Serialize an argparse parser to a JSON-compatible schema dict."""
    pass


def handle_schema_flag(
    parser: argparse.ArgumentParser,
    command: str,
    examples: List[str],
    args_list: List[str],
    deprecated: bool = False,
    deprecated_message: str = "",
) -> None:
    """Handle the pre-parse --schema fast path.

    This must run before parser.parse_args() because many commands want schema discovery even when
    the rest of the required arguments are absent.
    """
    pass
