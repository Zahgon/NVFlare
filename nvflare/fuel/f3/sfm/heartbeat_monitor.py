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
import logging
import time
from threading import Event, Thread
from typing import Dict

from nvflare.fuel.f3.comm_config import CommConfigurator
from nvflare.fuel.f3.drivers.driver_params import DriverCap
from nvflare.fuel.f3.sfm.constants import Types
from nvflare.fuel.f3.sfm.sfm_conn import SfmConnection

log = logging.getLogger(__name__)

HEARTBEAT_TICK = 5
DEFAULT_HEARTBEAT_INTERVAL = 60
DEFAULT_SEND_STALL_CONSECUTIVE_CHECKS = 3


class HeartbeatMonitor(Thread):
    def __init__(self, conns: Dict[str, SfmConnection]):
        Thread.__init__(self, name="hb_mon", daemon=True)
        self.conns = conns
        self.stopped = Event()
        self.curr_time = 0
        config = CommConfigurator()
        self.interval = config.get_heartbeat_interval(DEFAULT_HEARTBEAT_INTERVAL)
        self.send_stall_timeout = config.get_sfm_send_stall_timeout(45.0)
        self.close_stalled_connection = config.get_sfm_close_stalled_connection(False)
        self.stall_consecutive_checks = max(
            1, config.get_sfm_send_stall_consecutive_checks(DEFAULT_SEND_STALL_CONSECUTIVE_CHECKS)
        )
        self.stall_counts = {}
        if self.interval < HEARTBEAT_TICK:
            log.warning(f"Heartbeat interval is too small ({self.interval} < {HEARTBEAT_TICK})")

    def stop(self):
        pass

    def run(self):

        pass

    def _check_heartbeat(self):

        pass
