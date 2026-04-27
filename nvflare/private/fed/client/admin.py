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

"""The FedAdmin to communicate with the Admin server."""
from nvflare.apis.fl_constant import FLContextKey
from nvflare.apis.fl_context import FLContext
from nvflare.apis.shareable import ReservedHeaderKey
from nvflare.fuel.f3.cellnet.cell import Cell
from nvflare.fuel.f3.cellnet.core_cell import Message as CellMessage
from nvflare.fuel.hci.proto import ReplyKeyword
from nvflare.fuel.hci.server.constants import ConnProps
from nvflare.fuel.sec.audit import Auditor, AuditService
from nvflare.fuel.sec.authz import AuthorizationService, AuthzContext, Person
from nvflare.private.admin_defs import Message, error_reply, ok_reply
from nvflare.private.defs import CellChannel, RequestHeader, new_cell_message
from nvflare.private.fed.server.site_security import SiteSecurity
from nvflare.security.logging import secure_format_exception, secure_log_traceback


class RequestProcessor(object):
    """The RequestProcessor is responsible for processing a request."""

    def get_topics(self) -> [str]:
        """Get topics that this processor will handle.

        Returns: list of topics

        """
        pass

    def process(self, req: Message, app_ctx) -> Message:
        """Called to process the specified request.

        Args:
            req: request message
            app_ctx: application context

        Returns: reply message

        """
        pass


class FedAdminAgent(object):
    """FedAdminAgent communicate with the FedAdminServer."""

    def __init__(self, client_name: str, cell: Cell, app_ctx):
        """Init the FedAdminAgent.

        Args:
            client_name: client name
            app_ctx: application context
            cell: the Cell for communication
        """
        auditor = AuditService.get_auditor()
        if not isinstance(auditor, Auditor):
            raise TypeError("auditor must be an instance of Auditor, but got {}".format(type(auditor)))

        self.name = client_name
        self.cell = cell
        self.auditor = auditor
        self.app_ctx = app_ctx
        self.processors = {}
        self.asked_to_stop = False
        self.register_cell_cb()

    def register_cell_cb(self):
        pass

    def register_processor(self, processor: RequestProcessor):
        """To register the RequestProcessor.

        Args:
            processor: RequestProcessor

        """
        pass

    def _dispatch_request(
        self,
        request: CellMessage,
        # *args, **kwargs
    ) -> CellMessage:
        pass

    def _set_security_data(self, req, fl_ctx: FLContext):
        pass
