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

import random
from collections import Counter, defaultdict
from typing import Dict, Set

from nvflare.edge.assessors.device_manager import DeviceManager
from nvflare.edge.mud import PropKey
from nvflare.fuel.utils.validation_utils import check_positive_int


class BuffDeviceManager(DeviceManager):
    def __init__(
        self,
        device_selection_size: int,
        initial_min_client_num: int = 1,
        min_hole_to_fill: int = 1,
        device_reuse: bool = True,
        device_sampling_strategy: str = "balanced",
    ):
        """Initialize the BuffDeviceManager.
        BuffDeviceManager is responsible for managing the selection of devices for model training.
        It maintains a list of available devices, tracks the current selection, and refills the selection as needed.
        The device_selection_size determines how many "concurrent" devices can be selected for the training session.
        The min_hole_to_fill determines how many empty slots should be created before refilling.
            - An empty slot is created when any device reports its update back.
            - To fill a slot, a new device is selected from the available device pool.
        The device_reuse flag indicates whether devices can be reused across different model versions, if False, we will always select new devices when filling holes.
        Args:
            device_selection_size (int): Number of devices to select for each model update round.
            initial_min_client_num (int): Minimum number of clients to have at the beginning. This can be useful for initial model dispatch.
            min_hole_to_fill (int): Minimum number of empty slots in device selection before refilling. Defaults to 1 - once received an update, immediately sample a new device and send the current task to it.
            device_reuse (bool): Whether to allow reusing devices across different model versions. Defaults to True.
            device_sampling_strategy (str): Strategy for sampling devices when filling selection. Defaults to "balanced".
                - "balanced": try to balance the usage of devices across clients.
                - "random": randomly select devices from the available pool.
        """
        super().__init__()
        check_positive_int("device_selection_size", device_selection_size)
        check_positive_int("min_hole_to_fill", min_hole_to_fill)
        check_positive_int("initial_min_client_num", initial_min_client_num)
        if device_sampling_strategy not in ("balanced", "random"):
            raise ValueError(
                f"device_sampling_strategy must be 'balanced' or 'random', got '{device_sampling_strategy}'"
            )
        self.device_selection_size = device_selection_size
        self.initial_min_client_num = initial_min_client_num
        self.min_hole_to_fill = min_hole_to_fill
        self.device_reuse = device_reuse
        self.device_sampling_strategy = device_sampling_strategy
        # also keep track of the current selection version and used devices
        self.current_selection_version = 0
        self.used_devices = {}
        # keep a map of device_id -> client_name
        self.device_client_map = {}

    def _balanced_device_sampling(self, usable_devices: Set[str], num_holes: int) -> Set[str]:
        """Sample devices while balancing across clients.

        Args:
            usable_devices: Set of device IDs that can be selected
            num_holes: Number of devices to sample

        Returns:
            Set of selected device IDs
        """
        pass

    def update_available_devices(self, devices: Dict, fl_ctx) -> None:
        pass

    def fill_selection(self, current_model_version: int, fl_ctx) -> None:
        pass

    def remove_devices_from_selection(self, devices: Set[str], fl_ctx) -> None:
        pass

    def remove_devices_from_used(self, devices: Set[str], fl_ctx) -> None:
        pass

    def has_enough_devices_and_clients(self, fl_ctx) -> bool:
        pass

    def should_fill_selection(self, fl_ctx) -> bool:
        pass

    def get_active_model_versions(self, fl_ctx) -> Set[int]:
        pass
