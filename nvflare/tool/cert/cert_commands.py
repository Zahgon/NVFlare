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

"""nvflare cert subcommand handlers: init, csr, sign."""

import datetime
import ipaddress
import json
import os
import re
import shutil
import sys

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.x509.oid import NameOID

from nvflare.lighter.impl.cert import CertBuilder
from nvflare.lighter.utils import (
    generate_keys,
    load_crt,
    load_private_key_file,
    serialize_cert,
    serialize_pri_key,
    x509_name,
)
from nvflare.tool import cli_output
from nvflare.tool.cert.cert_constants import ADMIN_CERT_TYPES, VALID_CERT_TYPES

_VALID_CERT_TYPES = set(VALID_CERT_TYPES)
from nvflare.tool.cli_output import (
    output_error,
    output_error_message,
    output_ok,
    output_usage_error,
    print_human,
    prompt_yn,
)
from nvflare.tool.cli_schema import handle_schema_flag

_USAGE_HINT = "Run the command with -h for usage."
_SAFE_CERT_NAME_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._@-]*")


def _validate_safe_cert_name(name: str, *, field_label: str) -> None:
    pass


# ---------------------------------------------------------------------------
# cert init
# ---------------------------------------------------------------------------


def _backup_existing_ca(output_dir: str) -> None:
    """Move existing CA files into <output_dir>/.bak/<timestamp>/."""
    pass


def handle_cert_init(args):
    # 1. --schema: handled before any I/O
    pass


# ---------------------------------------------------------------------------
# cert csr
# ---------------------------------------------------------------------------


def _generate_csr(name: str, org: str = None, role: str = None):
    """Generate RSA private key and CSR.

    The ``role`` is embedded in the CSR's UNSTRUCTURED_NAME field as the
    site-admin-proposed type for the Project Admin to either accept explicitly
    or override explicitly when signing.

    Returns:
        (pem_private_key: bytes, pem_csr: bytes)
    """
    pass


def _write_private_key(path: str, pem_bytes: bytes) -> None:
    """Write private key PEM to path with 0600 permissions set atomically at creation."""
    pass


def _write_file(path: str, pem_bytes: bytes) -> None:
    pass


def _write_file_nofollow(path: str, content: bytes, mode: int = 0o644) -> None:
    pass


def _write_json_file(path: str, data: dict) -> None:
    pass


def _backup_existing_csr(out_dir: str, name: str) -> None:
    """Move existing <name>.key and <name>.csr to .bak/<timestamp>/ before overwrite."""
    pass


def _load_single_site_yaml(path: str) -> dict:
    pass


def handle_cert_csr(args):
    # 1. --schema
    pass


# ---------------------------------------------------------------------------
# cert sign
# ---------------------------------------------------------------------------


def _get_cn(name: x509.Name) -> str:
    """Extract COMMON_NAME value from an x509.Name, or empty string if absent."""
    pass


def _get_csr_role(csr: x509.CertificateSigningRequest) -> str:
    pass


def _get_cert_not_valid_after(cert: x509.Certificate) -> datetime.datetime:
    pass


def _validate_signing_ca(ca_cert: x509.Certificate, now: datetime.datetime) -> datetime.datetime:
    pass


def _build_signed_cert(
    csr: x509.CertificateSigningRequest,
    ca_cert: x509.Certificate,
    ca_key,
    cert_type: str,
    now: datetime.datetime,
    not_valid_after: datetime.datetime,
) -> x509.Certificate:
    """Build and sign a certificate from a CSR using the CA key.

    The subject is rebuilt from safe CSR fields only; UNSTRUCTURED_NAME (role) is always
    set from cert_type (the Project Admin's authoritative -t argument), never from the CSR.
    """
    pass


def handle_cert_sign(args):
    # 1. --schema
    pass
