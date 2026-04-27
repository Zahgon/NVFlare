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

import os
import shutil
import time
from typing import Tuple

from nvflare.fuel.utils.attributes_exportable import ExportMode
from nvflare.fuel.utils.constants import Mode
from nvflare.fuel.utils.pipe.file_accessor import FileAccessor
from nvflare.fuel.utils.pipe.file_name_utils import file_name_to_message, message_to_file_name
from nvflare.fuel.utils.pipe.fobs_file_accessor import FobsFileAccessor
from nvflare.fuel.utils.pipe.pipe import HEARTBEAT_SEND_TIMEOUT, Message, Pipe, Topic
from nvflare.fuel.utils.validation_utils import check_object_type, check_positive_number, check_str


class FilePipe(Pipe):
    def __init__(self, mode: Mode, root_path: str, file_check_interval=0.1):
        """Implementation of communication through the file system.

        Args:
            mode (Mode): Mode of the endpoint. A pipe has two endpoints.
                An endpoint can be either the one that initiates communication or the one listening.
            root_path (str): root path for this file pipe, folders and files will be created under this root_path
                for communication.
            file_check_interval (float): how often should to check the file exists.
        """
        super().__init__(mode=mode)
        check_positive_number("file_check_interval", file_check_interval)
        check_str("root_path", root_path)

        self._remove_root = False
        self.root_path = root_path
        self.file_check_interval = file_check_interval
        self.pipe_path = None
        self.x_path = None
        self.y_path = None
        self.t_path = None

        if self.mode == Mode.ACTIVE:
            self.get_f = self.x_get
            self.put_f = self.x_put
        elif self.mode == Mode.PASSIVE:
            self.get_f = self.y_get
            self.put_f = self.y_put

        self.accessor = FobsFileAccessor()  # default

    def set_file_accessor(self, accessor: FileAccessor):
        """Sets the file accessor to be used by the pipe.
        The default file accessor is FobsFileAccessor.

        Args:
            accessor: the accessor to be used.
        """
        pass

    @staticmethod
    def _make_dir(path):
        pass

    def open(self, name: str):
        pass

    @staticmethod
    def _clear_dir(p: str):
        pass

    def _create_file(self, to_dir: str, msg: Message) -> str:
        pass

    def clear(self):
        pass

    def _monitor_file(self, file_path: str, timeout=None) -> bool:
        """Monitors the file until it's read-and-removed by peer, or timed out.

        Args:
            file_path: the path to be monitored
            timeout: how long to wait for timeout

        Returns:
            whether the file has been read and removed
        """
        pass

    def x_put(self, msg: Message, timeout) -> bool:
        """

        Args:
            msg:
            timeout:

        Returns: whether file is read by the peer

        """
        pass

    def _read_file(self, file_path: str):
        # since reading file may take time and another process may try to delete the file
        # we move the file to a temp name before reading it
        pass

    def _get_next(self, from_dir: str):
        def _safe_mtime(f):
            pass
        pass

    def _get_from_dir(self, from_dir: str, timeout=None):
        pass

    def x_get(self, timeout=None):
        # read from X's queue
        pass

    def y_put(self, msg: Message, timeout) -> bool:
        # put it in X's queue
        pass

    def y_get(self, timeout=None):
        # read from Y's queue
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

    def receive(self, timeout=None):
        pass

    def close(self):
        pass

    def can_resend(self) -> bool:
        pass

    def export(self, export_mode: str) -> Tuple[str, dict]:
        pass
