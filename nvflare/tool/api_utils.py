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
import time
from typing import List

from nvflare.fuel.flare_api.api_spec import JobNotFound, NoConnection
from nvflare.fuel.flare_api.flare_api import Session


def shutdown_system(
    prod_dir: str, username: str = "admin@nvidia.com", secure_mode: bool = True, timeout_in_sec: int = 30
):
    pass


def shutdown_system_by_session(sess: Session, timeout_in_sec: int = 20):
    pass


def get_running_job_ids(jobs: list) -> List[str]:
    pass


def abort_jobs(sess, job_ids):
    pass


def wait_for_system_start(
    num_clients: int,
    prod_dir: str,
    username: str = "admin",
    secure_mode: bool = False,
    second_to_wait: int = 10,
    timeout_in_sec: int = 30,
):
    pass
