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

import json
from base64 import urlsafe_b64decode, urlsafe_b64encode
from binascii import hexlify, unhexlify

# ipcl_python is not a required dependency. The import error causes unit test failure so make it optional
try:
    import ipcl_python
    from ipcl_python import PaillierEncryptedNumber as EncryptedNumber
    from ipcl_python.ipcl_python import BNUtils, ipclCipherText

    ipcl_imported = True
except Exception:
    ipcl_imported = False

SCALE_FACTOR = 10000000000000
ENABLE_DJN = True


def generate_keys(n_length=1024):
    pass


def encrypt_number(pubkey, ciphertext, exponent):
    pass


def create_pub_key(key, n_length=1024):
    pass


def ciphertext_to_int(d):
    pass


def int_to_ciphertext(d, pubkey):
    pass


def get_exponent(d):
    pass


# base64 utils from jwcrypto
def base64url_encode(payload):
    pass


def base64url_decode(payload):
    pass


def base64_to_int(source):
    pass


def int_to_base64(source):
    pass


def combine(g, h):
    pass


def split(d):
    pass


def _encode_encrypted_numbers(numbers):
    pass


def encode_encrypted_numbers_to_str(numbers):
    pass


def encode_encrypted_data(pubkey, encrypted_numbers) -> str:
    pass


def decode_encrypted_data(encoded: str, n_length=1024):
    pass


def decode_encrypted_numbers_from_str(pubkey, encoded: str):
    pass


def _decode_encrypted_numbers(pubkey, data):
    pass


def encode_feature_aggregations(aggrs: list):
    pass


def decode_feature_aggregations(pubkey, encoded: str):
    pass
