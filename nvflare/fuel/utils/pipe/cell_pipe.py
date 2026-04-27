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

import queue
import threading
import time
from typing import Tuple, Union

from nvflare.apis.fl_constant import ConnPropKey, FLMetaKey, SystemVarName
from nvflare.fuel.data_event.utils import get_scope_property
from nvflare.fuel.f3.cellnet.cell import Cell
from nvflare.fuel.f3.cellnet.cell import Message as CellMessage
from nvflare.fuel.f3.cellnet.defs import MessageHeaderKey, ReturnCode
from nvflare.fuel.f3.cellnet.fqcn import FQCN
from nvflare.fuel.f3.cellnet.net_agent import NetAgent
from nvflare.fuel.f3.cellnet.utils import make_reply
from nvflare.fuel.f3.drivers.driver_params import DriverParams
from nvflare.fuel.sec.authn import set_add_auth_headers_filters
from nvflare.fuel.utils.attributes_exportable import ExportMode
from nvflare.fuel.utils.config_service import search_file
from nvflare.fuel.utils.constants import Mode
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.fuel.utils.validation_utils import check_object_type, check_str

from .pipe import Message, Pipe, Topic

SSL_ROOT_CERT = "rootCA.pem"
_PREFIX = "cell_pipe."

_HEADER_MSG_TYPE = _PREFIX + "msg_type"
_HEADER_MSG_ID = _PREFIX + "msg_id"
_HEADER_REQ_ID = _PREFIX + "req_id"
_HEADER_START_TIME = _PREFIX + "start"
_HEADER_HB_SEQ = _PREFIX + "hb_seq"


def _cell_fqcn(mode, site_name, token, parent_fqcn):
    # The FQCN of the cell must be unique in the whole cellnet.
    # We use the combination of mode, site_name, and token to derive the value of FQCN
    # Since the token is usually used across all sites, the "site_name" differentiate cell on one site from another.
    # The two peer pipes on the same site share the same site_name and token, but are differentiated by their modes.
    pass


def _to_cell_message(msg: Message, extra=None) -> CellMessage:
    pass


def _from_cell_message(cm: CellMessage) -> Message:
    pass


class _CellInfo:
    """
    A cell could be used by multiple pipes (e.g. one pipe for task interaction, another for metrics logging).
    """

    def __init__(self, site_name, cell, net_agent, auth_token, token_signature):
        self.site_name = site_name
        self.cell = cell
        self.auth_token = auth_token
        self.token_signature = token_signature
        self.net_agent = net_agent
        self.started = False
        self.pipes = []
        self.lock = threading.Lock()

    def start(self):
        pass

    def add_pipe(self, p):
        pass

    def close_pipe(self, p):
        pass


class CellPipe(Pipe):
    """
    CellPipe is an implementation of `Pipe` that utilizes the `Cell` from NVFlare's foundation layer (f3) to
    do the communication.
    """

    _lock = threading.Lock()
    _cells_info = {}  # (root_url, site_name, token) => _CellInfo

    @classmethod
    def _build_cell(cls, site_name, fqcn, parent_conn_props, secure_mode, workspace_dir, logger):
        """Build a cell if necessary.
        The combination of (root_url, site_name, token) uniquely determine one cell.
        There can be multiple pipes on the same cell.

        Args:
            parent_conn_props: parent for this cell
            secure_mode: whether cellnet is in secure mode
            workspace_dir: workspace that contains startup kit for connecting to server. Needed only if secure_mode

        Returns:

        """
        pass

    def __init__(
        self,
        mode: Mode,
        site_name: str,
        token: str,
        root_url: str = "",
        secure_mode: bool = True,
        workspace_dir: str = "",
    ):
        """The constructor of the CellPipe.

        Args:
            mode: passive or active mode
            site_name (str): name of the FLARE site
            token (str): unique id to guarantee the uniqueness of cell's FQCN.
            root_url (str): the root url of the cellnet that the pipe's cell will join
            secure_mode (bool): whether connection to the root is secure (TLS)
            workspace_dir (str): the directory that contains startup for joining the cellnet. Required only in secure_mode
        """
        super().__init__(mode)
        self.logger = get_obj_logger(self)

        self.site_name = site_name
        self.token = token
        self.secure_mode = secure_mode
        self.workspace_dir = workspace_dir
        self.root_url = root_url

        # this section is needed by job config to prevent building cell when using SystemVarName arguments
        # TODO: enhance this part
        sysvarname_placeholders = ["{" + varname + "}" for varname in dir(SystemVarName)]
        if any([arg in sysvarname_placeholders for arg in [site_name, token, root_url, secure_mode, workspace_dir]]):
            return

        check_str("root_url", root_url)
        check_object_type("secure_mode", secure_mode, bool)
        check_str("token", token)
        check_str("site_name", site_name)
        check_str("workspace_dir", workspace_dir)

        # determine the endpoint for this pipe to connect to
        root_conn_props = get_scope_property(site_name, ConnPropKey.ROOT_CONN_PROPS)

        if root_conn_props:
            # Not in simulator
            if not isinstance(root_conn_props, dict):
                raise RuntimeError(f"expect root_conn_props for {site_name} to be dict but got {type(root_conn_props)}")

            cp_conn_props = get_scope_property(site_name, ConnPropKey.CP_CONN_PROPS)
            if cp_conn_props:
                if not isinstance(cp_conn_props, dict):
                    raise RuntimeError(f"expect cp_conn_props to be dict but got {type(cp_conn_props)}")

            url_to_conns = {
                root_conn_props.get(ConnPropKey.URL): root_conn_props,
                cp_conn_props.get(ConnPropKey.URL): cp_conn_props,
            }

            relay_conn_props = get_scope_property(site_name, ConnPropKey.RELAY_CONN_PROPS)
            if relay_conn_props:
                if not isinstance(relay_conn_props, dict):
                    raise RuntimeError(f"expect relay_conn_props to be dict but got {type(relay_conn_props)}")
                url_to_conns[relay_conn_props.get(ConnPropKey.URL)] = relay_conn_props

            if not root_url:
                # root_url not specified - use CP!
                root_url = cp_conn_props.get(ConnPropKey.URL)
                self.root_url = root_url

            conn_props = url_to_conns.get(self.root_url)
            if not conn_props:
                raise RuntimeError(f"cannot determine conn props for '{root_url}'")
        else:
            # this is running in simulator
            conn_props = {
                ConnPropKey.URL: root_url,
                ConnPropKey.FQCN: FQCN.ROOT_SERVER,
            }

        mode = f"{mode}".strip().lower()  # convert to lower case string
        fqcn = _cell_fqcn(mode, site_name, token, conn_props.get(ConnPropKey.FQCN))

        self.ci = self._build_cell(site_name, fqcn, conn_props, secure_mode, workspace_dir, self.logger)
        self.cell = self.ci.cell
        self.ci.add_pipe(self)

        if mode == "active":
            peer_mode = "passive"
        elif mode == "passive":
            peer_mode = "active"
        else:
            raise ValueError(f"invalid mode {mode} - must be 'active' or 'passive'")

        self.peer_fqcn = _cell_fqcn(peer_mode, site_name, token, conn_props.get(ConnPropKey.FQCN))
        self.received_msgs = queue.Queue()  # contains raw CellMessage objects
        self.channel = None  # the cellnet message channel
        self.pipe_lock = threading.Lock()  # used to ensure no msg to be sent after closed
        self.closed = False
        self.last_peer_active_time = 0.0
        self.hb_seq = 1
        # When True, every non-heartbeat outgoing cell message gets
        # MessageHeaderKey.PASS_THROUGH=True stamped on it.  The peer's
        # Adapter.call() reads this header and builds a per-call FOBS decode
        # context with FOBSContextKey.PASS_THROUGH=True so that tensors arrive
        # as LazyDownloadRef placeholders rather than being downloaded inline.
        #
        # Set by ExProcessClientAPI.init() (subprocess→CJ reverse direction)
        # when CellPipe is in use.  Has no effect for FilePipe (which is not a
        # CellPipe and never has this attribute set).
        #
        # Note: the forward direction (Fix 18, CJ→subprocess) does not use this
        # flag; it is implemented via ReservedHeaderKey.PASS_THROUGH stamped on
        # the shareable in SwarmClientController._scatter() and propagated by
        # aux_runner.py — not through pipe.pass_through_on_send.
        self.pass_through_on_send: bool = False

    def _update_peer_active_time(self, msg: CellMessage, ch_name: str, msg_type: str):
        pass

    def get_last_peer_active_time(self):
        pass

    def set_cell_cb(self, channel_name: str):
        # This allows multiple pipes over the same cell (e.g. one channel for tasks, another for metrics),
        # as long as different pipes use different cell message channels
        pass

    def send(self, msg: Message, timeout=None) -> bool:
        """Sends the specified message to the peer.

        Args:
            msg: the message to be sent
            timeout: if specified, number of secs to wait for the peer to read the message.
                If not specified, wait indefinitely.

        Returns:
            Whether the message is read by the peer.
        """
        pass

    def _receive_message(self, request: CellMessage) -> Union[None, CellMessage]:
        # Return the pipe-level ACK as quickly as possible.
        #
        # The expensive work (FOBS decode / tensor download) has ALREADY been done
        # by Adapter.call() in cell.py BEFORE this callback is invoked.  With
        # reverse PASS_THROUGH enabled on the pipe cell, that decode is cheap
        # (creates LazyDownloadRef objects rather than downloading).
        #
        # We queue the raw CellMessage rather than converting it to a Message here.
        # The conversion (_from_cell_message) is deferred to receive() time so that
        # this callback – and therefore the cell-level ACK path – performs the
        # absolute minimum work before returning ReturnCode.OK to the sender.
        pass

    def receive(self, timeout=None) -> Union[None, Message]:
        pass

    def clear(self):
        pass

    def release_send_cache(self, msg: Message):
        """Clear the cached CellMessage that was attached to *msg* by send().

        The cache is created on the first send() call so that retries reuse the
        already-serialized CellMessage.  Once the retry loop exits this
        cache is no longer needed.  Dropping it allows the encoded payload bytes
        and any lingering references to be reclaimed by GC promptly, rather than
        waiting for the Message object itself to go out of scope.
        """
        pass

    def can_resend(self) -> bool:
        pass

    def open(self, name: str):
        pass

    def close(self):
        pass

    def export(self, export_mode: str) -> Tuple[str, dict]:
        pass
