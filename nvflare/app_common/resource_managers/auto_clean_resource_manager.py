# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
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

import time
import uuid
from abc import ABC, abstractmethod
from threading import Event, Lock, Thread

from nvflare.apis.event_type import EventType
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_context import FLContext
from nvflare.apis.resource_manager_spec import ResourceManagerSpec


class AutoCleanResourceManager(ResourceManagerSpec, FLComponent, ABC):
    def __init__(self, resources: dict, expiration_period: int = 30, check_period: float = 1.0):
        """AutoCleanResourceManager implementation.

        It will automatically clean up reserved resources.

        Args:
            resources (dict): Specify the list of resources unit
            expiration_period (int): Number of seconds to hold the resources reserved. default to 30.
                If check_resources is called but after "expiration_period" no allocate resource is called,
                then the reserved resources will be released.
            check_period (float): Number of seconds to check for expired resources. default to 1.0.
        """
        super().__init__()
        if not isinstance(resources, dict):
            raise TypeError(f"resources should be of type dict, but got {type(resources)}.")
        if not isinstance(expiration_period, int):
            raise TypeError(f"expiration_period should be of type int, but got {type(expiration_period)}.")
        if expiration_period <= 0:
            raise ValueError("expiration_period should be greater than 0.")

        self.resources = resources
        self.expiration_period = expiration_period
        self.reserved_resources = {}

        self._lock = Lock()
        self._stop_event = Event()
        self._cleanup_thread = Thread(target=self._check_expired)
        self._check_period = check_period

    @abstractmethod
    def _deallocate(self, resources: dict):
        """Deallocates the resources.

        Args:
            resources (dict): the resources to be freed.
        """
        pass

    @abstractmethod
    def _check_required_resource_available(self, resource_requirement: dict) -> bool:
        """Checks if resources are available.

        Args:
            resource_requirement (dict): the resource requested.

        Return:
            A boolean to indicate whether the current resources are enough for the required resources.
        """
        pass

    @abstractmethod
    def _reserve_resource(self, resource_requirement: dict) -> dict:
        """Reserves resources given the requirements.

        Args:
            resource_requirement (dict): the resource requested.

        Return:
            A dict of reserved resources associated with the requested resource.
        """
        pass

    @abstractmethod
    def _resource_to_dict(self) -> dict:
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        pass

    def _check_expired(self):
        pass

    def check_resources(self, resource_requirement: dict, fl_ctx: FLContext):
        pass

    def cancel_resources(self, resource_requirement: dict, token: str, fl_ctx: FLContext):
        pass

    def allocate_resources(self, resource_requirement: dict, token: str, fl_ctx: FLContext) -> dict:
        pass

    def free_resources(self, resources: dict, token: str, fl_ctx: FLContext):
        pass

    def report_resources(self, fl_ctx):
        pass
