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

import glob
import json
import os
from base64 import b64decode
from enum import Enum

from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


class LoadResult(Enum):
    """Constants for different results when loading secure content."""

    OK = "ok"
    NOT_MANAGED = "notManaged"
    NO_SUCH_CONTENT = "noSuchContent"
    NOT_SIGNED = "notSigned"
    INVALID_SIGNATURE = "invalidSignature"
    INVALID_CONTENT = "invalidContent"


class SecurityContentManager(object):
    def __init__(self, content_folder, signature_filename="signature.json", root_cert="rootCA.pem"):
        """Content manager used by SecurityContentService to load secure content.

        Args:
            content_folder (str): the folder path that includes signature file
            signature_filename (str, optional): the signature file (signed dictionary). Defaults to "signature.json".
            root_cert (str, optional): root CA certificate filename. Defaults to "rootCA.pem".
        """
        self.content_folder = content_folder
        signature_path = os.path.join(self.content_folder, signature_filename)
        rootCA_cert_path = os.path.join(self.content_folder, root_cert)
        if os.path.exists(signature_path) and os.path.exists(rootCA_cert_path):
            self.signature = json.load(open(signature_path, "rt"))
            for k in self.signature:
                self.signature[k] = b64decode(self.signature[k].encode("utf-8"))
            cert = x509.load_pem_x509_certificate(open(rootCA_cert_path, "rb").read(), default_backend())
            self.public_key = cert.public_key()
            self.valid_config = True
        else:
            self.signature = dict()
            self.valid_config = False

    def load_content(self, file_under_verification):
        """Loads the data of the file under verification and verifies that the signature is valid.

        Args:
            file_under_verification: file to load and verify

        Returns:
            A tuple of the file data and the LoadResult. File data may be None if the data cannot be loaded.
        """
        pass

    def load_json(self, file_under_verification):
        pass


class SecurityContentService(object):
    """Uses SecurityContentManager to load secure content."""

    security_content_manager = None
    content_folder = None

    @classmethod
    def initialize(cls, content_folder: str, signature_filename="signature.json", root_cert="rootCA.pem"):
        pass

    @classmethod
    def load_content(cls, file_under_verification):
        pass

    @classmethod
    def load_json(cls, file_under_verification):
        pass

    @classmethod
    def check_json_files(cls, patterns: [str]) -> [str]:
        """Check JSON files that match the specified patterns

        Args:
            patterns: the patterns to be checked

        Returns: full paths of invalid files if any.
        A file is considered invalid in any of the cases:
        - The file is not signed
        - The file does not match signature

        """
        pass
