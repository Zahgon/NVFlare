# Copyright (c) 2021-2026, NVIDIA CORPORATION.  All rights reserved.
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

from nvflare.lighter.constants import CtxKey, PropKey, ProvFileName
from nvflare.lighter.spec import Builder, Project, ProvisionContext
from nvflare.lighter.utils import sign_folders


class SignatureBuilder(Builder):
    """Sign files with rootCA's private key.

    Creates signatures for all the files signed with the root CA for the startup kits so that they
    can be cryptographically verified to ensure any tampering is detected. This builder writes the
    signature.json file.

    signature.json is generated only for:
    - CC (Confidential Computing) kits: full workspace signed for CVM attestation chain.
    - HE (Homomorphic Encryption) kits: startup + local dirs signed to protect shared TenSEAL context.

    Plain non-CC, non-HE kits do not receive signature.json. mTLS is the trust anchor for those
    deployments. Absence of signature.json is the correct and expected state for centrally
    provisioned standard kits and for kits assembled via the Manual Workflow (nvflare package).
    """

    def build(self, project: Project, ctx: ProvisionContext):
        pass
                # else: plain non-CC, non-HE — no signature.json generated.
                # mTLS is the trust anchor; signature.json adds no security and would
                # prevent local config customization and break the Manual Workflow.
