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

import os

from cryptography.exceptions import InvalidKey, InvalidSignature
from cryptography.hazmat.primitives import asymmetric, ciphers, hashes, padding
from cryptography.x509 import Certificate

HASH_LENGTH = 4  # Adjustable to avoid collision
NONCE_LENGTH = 16  # For AES, this is 128 bits (i.e. block size)
KEY_LENGTH = 32  # AES 256.  Choose from 16, 24, 32
HEADER_LENGTH = HASH_LENGTH + NONCE_LENGTH
PADDING_LENGTH = NONCE_LENGTH * 8  # in bits
KEY_ENC_LENGTH = 256
SIGNATURE_LENGTH = 256
SIMPLE_HEADER_LENGTH = NONCE_LENGTH + KEY_ENC_LENGTH + SIGNATURE_LENGTH


def get_hash(value):
    pass


class SessionKeyUnavailable(Exception):
    pass


class InvalidCertChain(Exception):
    pass


def _asym_enc(k, m):
    pass


def _asym_dec(k, m):
    pass


def _sign(k, m):
    pass


def _verify(k, m, s):

    pass


def _sym_enc(k: bytes, n: bytes, m: bytes):
    pass


def _sym_dec(k: bytes, n: bytes, m: bytes):
    pass


class SessionKeyManager:
    def __init__(self, root_ca):
        self.key_hash_dict = dict()
        self.root_ca = root_ca
        self.root_ca_pub_key = root_ca.public_key()

    def validate_cert_chain(self, cert):
        pass

    def key_request(self, remote_cert, local_cert, local_pri_key):
        pass

    def process_key_response(self, remote_cert, local_cert, local_pri_key, key_response):
        pass

    def key_available(self):
        pass

    def get_key(self, key_hash):
        pass

    def get_latest_key(self):
        pass


class SimpleCellCipher:
    def __init__(self, root_ca: Certificate, pri_key: asymmetric.rsa.RSAPrivateKey, cert: Certificate):
        self._root_ca = root_ca
        self._root_ca_pub_key = root_ca.public_key()
        self._pri_key = pri_key
        self._cert = cert
        self._pub_key = cert.public_key()
        self._validate_cert_chain(self._cert)
        self._cached_enc = dict()
        self._cached_dec = dict()

    def _validate_cert_chain(self, cert: Certificate):
        pass

    def encrypt(self, message: bytes, target_cert: Certificate):
        pass

    def decrypt(self, message: bytes, origin_cert: Certificate):
        pass
