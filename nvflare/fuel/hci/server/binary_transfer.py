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
import shutil

from nvflare.fuel.f3.streaming.file_downloader import ObjectDownloader, add_file
from nvflare.fuel.hci.conn import Connection
from nvflare.fuel.hci.proto import MetaKey, MetaStatusValue, make_meta
from nvflare.fuel.hci.server.constants import ConnProps
from nvflare.fuel.utils.log_utils import get_obj_logger


class BinaryTransfer:
    def __init__(self):
        self.logger = get_obj_logger(self)

    @staticmethod
    def tx_path(conn: Connection, tx_id: str, folder_name=None):
        pass

    def download_folder(self, conn: Connection, tx_id: str, folder_name: str):
        pass

    def _cleanup_tx(self, tx_id: str, status, files, tx_path):
        """
        Remove the job download folder
        """
        pass
