# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
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
import argparse
import logging
import threading
import time

from nvflare.fuel.f3.cellnet.cell import Cell
from nvflare.fuel.f3.message import Message
from nvflare.fuel.f3.streaming.tools.utils import RX_CELL, TEST_CHANNEL, TEST_TOPIC, TIMESTAMP, setup_log

log = logging.getLogger("receiver")
event = threading.Event()


def request_cb(message: Message):
    pass


def create_receiver_cell(url: str):
    pass


def receive_blob(listening_url: str):
    pass


if __name__ == "__main__":
    setup_log(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str, help="Listening URL")
    args = parser.parse_args()

    receive_blob(args.url)
