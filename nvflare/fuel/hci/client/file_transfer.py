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
import shutil
import tempfile
import time
import uuid

import nvflare.fuel.hci.file_transfer_defs as ftd
from nvflare.fuel.hci.client.event import EventType
from nvflare.fuel.hci.cmd_arg_utils import join_args
from nvflare.fuel.hci.proto import MetaKey, ProtoKey
from nvflare.fuel.hci.reg import CommandEntry, CommandModule, CommandModuleSpec, CommandSpec
from nvflare.fuel.utils.log_utils import get_obj_logger
from nvflare.fuel.utils.zip_utils import split_path, unzip_all_from_file, zip_directory_to_file
from nvflare.lighter.utils import load_private_key_file, sign_folders

from .api import _print_hci_message
from .api_spec import CommandContext, HCIRequester
from .api_status import APIStatus


class _FileSender(HCIRequester):
    def __init__(self, file_name: str):
        self.file_name = file_name

    def send_request(self, api, conn, cmd_ctx):
        pass


class _FileReceiver(HCIRequester):
    def __init__(self, source_fqcn: str, ref_id, file_name: str):
        self.source_fqcn = source_fqcn
        self.ref_id = ref_id
        self.file_name = file_name
        self.num_bytes_received = 0

    def send_request(self, api, conn, cmd_ctx):
        pass


class FileTransferModule(CommandModule):
    """Command module with commands relevant to file transfer."""

    PULL_BINARY_FILE_CMD = "pull_binary_file"

    def __init__(self, upload_dir: str, download_dir: str):
        if not os.path.isdir(upload_dir):
            raise ValueError("upload_dir {} is not a valid dir".format(upload_dir))

        if not os.path.isdir(download_dir):
            raise ValueError("download_dir {} is not a valid dir".format(download_dir))

        self.upload_dir = upload_dir
        self.download_dir = download_dir
        self.logger = get_obj_logger(self)

        self.cmd_handlers = {
            ftd.PUSH_FOLDER_FQN: self.push_folder,
            ftd.PULL_FOLDER_FQN: self.pull_folder,
        }

    def get_spec(self):
        pass

    def generate_module_spec(self, server_cmd_spec: CommandSpec):
        """
        Generate a new module spec based on a server command

        Args:
            server_cmd_spec:

        Returns:

        """
        pass

    def _tx_path(self, tx_id: str, folder_name: str):
        pass

    def pull_binary_file(self, args, ctx: CommandContext):
        """
        Args: cmd_name, source_fqcn, tx_id, ref_id, folder_name, file_name, [end]
        """
        pass

    @staticmethod
    def _unzip_file(api, file_path):
        # unzip the file
        pass

    def pull_folder(self, args, ctx: CommandContext):
        pass

    @staticmethod
    def _rename_folder(src: str, destination: str):
        pass

    def info(self, args, ctx: CommandContext):
        pass

    def push_folder(self, args, ctx: CommandContext):
        # upload with binary protocol
        pass
