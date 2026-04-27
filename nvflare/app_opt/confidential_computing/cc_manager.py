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
import random
import sys
import threading
from typing import Tuple

from nvflare.apis.app_validation import AppValidationKey
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.server_engine_spec import ServerEngineSpec
from nvflare.app_opt.confidential_computing.cc_authorizer import CCAuthorizer, CCTokenGenerateError, CCTokenVerifyError
from nvflare.fuel.f3.cellnet.core_cell import make_reply
from nvflare.fuel.f3.cellnet.defs import MessageHeaderKey
from nvflare.fuel.f3.cellnet.defs import ReturnCode as F3ReturnCode
from nvflare.fuel.f3.cellnet.fqcn import FQCN
from nvflare.fuel.hci.conn import Connection
from nvflare.fuel.hci.server.constants import ConnProps
from nvflare.fuel.utils.admin_name_utils import is_valid_admin_client_name
from nvflare.private.defs import ClientType, new_cell_message
from nvflare.private.fed.server.training_cmds import TrainingCommandModule

CC_TOKEN = "_cc_token"
CC_ISSUER = "_cc_issuer"
CC_NAMESPACE = "_cc_namespace"
CC_INFO = "_cc_info"
CC_TOKEN_VALIDATED = "_cc_token_validated"
CC_VERIFY_ERROR = "_cc_verify_error"

CC_ISSUER_ID = "issuer_id"
TOKEN_GENERATION_TIME = "token_generation_time"
TOKEN_EXPIRATION = "token_expiration"

CC_VERIFICATION_FAILED = "not meeting CC requirements"

# Dedicated CC validation channel and topics
CC_CHANNEL = "cc_validation"
CC_TOPIC_REQUEST_TOKEN = "request_fresh_token"
CC_TOPIC_GET_SITES = "get_sites"


class CCManager(FLComponent):
    def __init__(
        self,
        cc_issuers_conf: list[dict[str, str]],
        cc_verifier_ids: list[str],
        verify_frequency: int = 600,
        cc_enabled_sites: list[str] = [],
        get_site_request_timeout: float = 10.0,
        get_token_request_timeout: float = 10.0,
    ):
        """Manage all confidential computing related tasks.

        This manager does the following tasks:
            1. Obtains and attaches its own CC tokens.
            2. Validates CC tokens received from other sites.
            3. Prevents system startup if CC validation fails.
            4. Periodically re-validates all CC tokens and shuts down
               the system if validation fails (e.g., due to expired or invalid tokens).

        Note:
            arguments example:
                "cc_issuers_conf": [
                    {
                        "issuer_id": "mock_authorizer",
                        "token_expiration": 100
                    }
                ],
                "cc_verifier_ids": [
                    "mock_authorizer"
                ],
                "verify_frequency": 120,
                "cc_enabled_sites": [
                    "server1",
                    "site-1",
                    "site-2"
                ]

        Args:
            cc_issuers_conf: configuration of the CC token issuers.
                Each item in the list is a dict that contains the CC token issuer component ID,
                and the token expiration time in seconds.
            cc_verifier_ids: CC token verifiers component IDs
            verify_frequency: CC tokens verification frequency
            cc_enabled_sites: list of sites that are enabled for CC
            get_site_request_timeout: timeout value for get site request
            get_token_request_timeout: timeout value for get token request
        """
        FLComponent.__init__(self)
        self.site_name = None
        self.cc_issuers_conf = cc_issuers_conf
        self.cc_verifier_ids = cc_verifier_ids
        self.cc_enabled_sites = cc_enabled_sites

        if not isinstance(verify_frequency, int):
            raise ValueError(f"verify_frequency must be int, but got {type(verify_frequency).__name__}")

        self.verify_time = None
        self.cc_issuers = {}
        self.cc_verifiers = {}

        self.get_site_request_timeout = get_site_request_timeout
        self.get_token_request_timeout = get_token_request_timeout

        # Store engine reference for cell handlers
        self.engine = None

        self.lock = threading.RLock()

        # Cross-site validation support
        self.cross_validation_run_once = False
        self.cross_validation_thread = None
        self.cross_validation_interval = int(verify_frequency)
        self.cross_validation_stop_event = threading.Event()

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def _setup_cc_authorizers(self, fl_ctx):
        pass

    def _generate_and_attach_tokens(self, fl_ctx: FLContext):
        """Generate and attach CC tokens for sending to peer."""
        pass

    def _validate_server_tokens(self, fl_ctx: FLContext):
        """Validate the server's CC info during registration."""
        pass

    def _validate_client_tokens(self, fl_ctx: FLContext):
        """Validate the client's CC info during registration."""
        pass

    def _validate_cc_infos(self, participants_cc_info: dict[str, list[dict[str, str]]], fl_ctx: FLContext):
        """Shared validator for CC info (server or client).

        Args:
            participants_cc_info:
                A dict of (participant_name, participant_cc_infos)
                participant_cc_infos is a list of CC tokens.
        """
        pass

    def _validate_participants_tokens(self, participants_tokens: dict[str, list[dict[str, str]]]) -> str:
        pass

    def _verify_participants_tokens(
        self, participants_tokens: dict[str, list[dict[str, str]]]
    ) -> Tuple[dict[str, bool], list[str]]:
        """Verifies tokens for all participants.

        Args:
            participants_tokens: dict of participant name to list of tokens

        Returns:
            tuple of (result, invalid_participant_list)
            result: dict of participant name to bool
            invalid_participant_list: list of invalid participants
        """
        pass

    def _perform_cross_site_validation(self, fl_ctx: FLContext) -> bool:
        """Perform cross-site validation and shutdown system on failure.

        Returns:
            True if validation passed, False if validation failed (system will shutdown)
        """
        pass

    def _get_all_sites(self) -> list[Tuple[str, str]]:
        """Get list of all sites (server + participating clients), excluding admin clients."""
        pass

    def _get_all_cc_enabled_sites(self, fl_ctx: FLContext) -> list[Tuple[str, str]]:
        """Get list of all sites (server + participating clients), excluding admin clients.

        This method works differently depending on the context:
        - Server (ServerEngine): Gets all registered clients via engine.get_clients()
        - Client (ClientEngine): Dynamically requests current site list from server

        Admin clients are excluded from CC verification as they don't participate in FL jobs.

        Args:
            fl_ctx: FLContext

        Returns:
            List of tuples of (site fqcn, site name) (excluding admin clients).
        """
        pass

    def _request_sites_from_server(self, fl_ctx: FLContext) -> list[Tuple[str, str]]:
        """Client side: Request current list of participating sites from server."""
        pass

    def _start_cross_site_validation(self, fl_ctx: FLContext):
        """Start periodic cross-site validation thread on ALL sites."""
        pass

    def _stop_cross_site_validation(self):
        """Stop cross-site validation thread."""
        pass

    def _cross_site_validation_loop(self, fl_ctx: FLContext):
        """Periodic cross-site validation - runs on ALL sites."""
        pass

    def _collect_all_site_tokens(self, fl_ctx: FLContext) -> dict[str, list[dict[str, str]]]:
        """Collect FRESH CC tokens from all participants using dedicated CC channel.

        This method:
        1. Requests fresh tokens from ALL other sites
        2. Returns all fresh tokens for validation

        This ensures all tokens are freshly generated and synchronized.
        """
        pass

    def _register_cc_handlers(self, fl_ctx: FLContext):
        """Register handlers for dedicated CC validation channel."""
        pass

    def _generate_fresh_tokens_for_validation(self) -> list[dict[str, str]]:
        """Generate completely fresh tokens for validation request.

        This creates NEW tokens on-the-fly for each validation request.

        Returns:
            List of fresh CC tokens ready for validation.
            Each token is a dict consists of CC_TOKEN, CC_NAMESPACE and CC_TOKEN_VALIDATED.
        """
        pass

    def _handle_token_refresh_request(self, request):
        """Handle request from another site to generate and return fresh token.

        This is called when another site initiates cross-site validation.

        IMPORTANT: Multiple validation events can happen simultaneously, so we generate
        a FRESH token for EACH request (nonce-based tokens are single-use).
        """
        pass

    def _handle_get_sites_request(self, request):
        """Server side: Handle request for current list of participating sites."""
        pass

    def _shutdown_system(self, reason: str, fl_ctx: FLContext):
        """Shuts down the entire NVFlare system due to CC validation failure."""
        pass
