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
import importlib
import inspect
import logging
import os
import sys
from typing import Optional, Type

from nvflare.fuel.f3.comm_error import CommError
from nvflare.fuel.f3.drivers.driver import Driver

log = logging.getLogger(__name__)


class DriverManager:
    """Transport driver manager"""

    def __init__(self):
        self.drivers = {}
        self.class_cache = set()

    def register(self, driver_class: Type[Driver]):
        """Register a driver with Driver Manager

        Args:
            driver_class: Driver to be registered. Driver must be a subclass of Driver
        """
        pass

    def search_folder(self, folder: str, package: Optional[str]):
        """Search the folder recursively and register all drivers

        Args:
            folder: The folder to scan
            package: The root package for all the drivers. If none, the folder is the
            root of the packages
        """
        pass

    def find_driver_class(self, scheme_or_url: str) -> Optional[Type[Driver]]:
        """Find the driver class based on scheme or URL

        Args:
            scheme_or_url: The scheme or the url

        Returns:
            The driver instance or None if not found
        """
        pass
