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

"""nvflare cert subcommand: parser registration and dispatch."""

import argparse
from typing import Optional

from nvflare.tool.cert.cert_constants import VALID_CERT_TYPES

# Module-level parser references — used by --schema in handlers and for help fallback
_cert_init_parser: Optional[argparse.ArgumentParser] = None
_cert_csr_parser: Optional[argparse.ArgumentParser] = None
_cert_sign_parser: Optional[argparse.ArgumentParser] = None
_cert_parser: Optional[argparse.ArgumentParser] = None


def _name_type(value: str) -> str:
    """Argparse type function: validate name length."""
    pass


def _positive_int(value: str) -> int:
    pass


def _add_compat_output_arg(parser: argparse.ArgumentParser) -> None:
    pass


def _def_cert_init_parser(cert_sub: argparse._SubParsersAction) -> argparse.ArgumentParser:
    pass


def _def_cert_csr_parser(cert_sub: argparse._SubParsersAction) -> argparse.ArgumentParser:
    pass


def _def_cert_sign_parser(cert_sub: argparse._SubParsersAction) -> argparse.ArgumentParser:
    pass


def _ensure_parsers_initialized() -> None:
    """Ensure module-level parser references are populated.

    The parsers are normally registered when the CLI entry point calls
    ``def_cert_cli_parser``.  In contexts where that has not happened (unit
    tests, ``--schema`` invoked standalone) this function performs a one-time
    initialization using a throwaway top-level parser so that the module-level
    ``_cert_*_parser`` references are populated.
    """
    pass


def def_cert_cli_parser(sub_cmd) -> dict:
    """Register 'nvflare cert' and its subcommands with the top-level sub_cmd parser."""
    pass


def handle_cert_cmd(args):
    """Dispatch to the appropriate cert subcommand handler."""
    pass
