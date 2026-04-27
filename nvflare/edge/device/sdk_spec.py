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
import copy
import time
from typing import List

from nvflare.apis.dxo import DXO, from_dict
from nvflare.apis.signal import Signal

from .config import process_train_config
from .defs import Context, ContextKey, DataSource, EventType, Executor, Filter


class FlareRunner:

    def __init__(
        self,
        job_name: str,
        data_source: DataSource,
        device_info: dict,
        user_info: dict,
        job_timeout: float,
        in_filters: List[Filter] = None,
        out_filters: List[Filter] = None,
        resolver_registry: dict = None,
    ):
        """Constructor of FlareRunner

        Args:
            job_name: name of the job. Used for matching Flare job on host.
            data_source: data source for the training
            device_info: device info
            user_info: info of the device user
            job_timeout: timeout for getting a job from Flare host
            in_filters: app provided filters for input model
            out_filters: app provided filters for output model
            resolver_registry: app provided resolvers

        Note: app provided filters apply to all jobs and are invoked before configured job filters!
        """
        self.job_name = job_name
        self.resolver_registry = {}
        self.data_source = data_source
        self.device_info = device_info
        self.user_info = user_info
        self.job_timeout = job_timeout
        self.app_in_filters = in_filters
        self.app_out_filters = out_filters
        self.abort_signal = Signal()
        self.job_id = None
        self.cookie = None

        # add built-in creators
        self.add_builtin_resolvers()

        # add app-provided resolvers, which can override builtin resolvers!
        if resolver_registry:
            if not isinstance(resolver_registry, dict):
                raise ValueError(f"resolver_registry must be dict but got {type(resolver_registry)}")
            self.resolver_registry.update(resolver_registry)

    def add_builtin_resolvers(self):
        """Add resolvers for Flare's builtin components

        Returns:

        """
        pass

    def run(self):
        pass

    def stop(self):
        pass

    def _get_job(self, ctx: Context, abort_signal: Signal) -> dict:
        """Repeatedly try to get job from host

        Returns: a job or None if the host says DONE or timed out.

        """
        pass

    def _get_task(self, ctx: Context, abort_signal: Signal) -> (dict, bool):
        """Repeatedly try to get a task from the host

        Returns: a task or None if the host says DONE

        """
        pass

    def _report_result(self, result: dict, ctx: Context, abort_signal: Signal) -> bool:
        pass

    def _do_filtering(self, data: DXO, filters, ctx) -> DXO:
        pass

    def _do_one_job(self) -> bool:
        """Work with the host to do one job

        Returns: whether whole session is done.

        """
        pass
