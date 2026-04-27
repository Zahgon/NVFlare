# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
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

import binascii
import hashlib
import os
import uuid


class IdentityKey(object):

    NAME = "common_name"
    ORG = "organization"
    ROLE = "role"


def hash_password(password):
    """Hash a password for storing.

    Args:
        password: password to hash

    Returns: hashed password

    """
    pass


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user.

    Args:
        stored_password: stored password
        provided_password: password provided by user

    Returns: True if the stored password equals the provided password, otherwise False

    """
    pass


def make_session_token():
    """Makes a new session token.

    Returns: created session token

    """
    pass


def get_identity_info(cert: dict):
    """Gets the identity information from the provided certificate.

    Args:
        cert: certificate

    Returns: if the cert is None, returning None.
             if the cert is a dictionary, returning a dictionary containing three keys, common_name, organization and role.

    """
    pass


def get_certificate_common_name(cert: dict):
    """Gets the common name of the provided certificate.

    Args:
        cert: certificate

    Returns: common name of provided cert

    """
    pass
