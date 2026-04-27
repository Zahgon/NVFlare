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
import json
import os.path
from typing import Optional

from nvflare.edge.assessor import Assessor
from nvflare.edge.controllers.sage import ScatterAndGatherForEdge
from nvflare.edge.executors.edge_model_executor import EdgeModelExecutor
from nvflare.edge.simulation.device_task_processor import DeviceTaskProcessor
from nvflare.edge.updaters.emd import AggregatorFactory
from nvflare.edge.widgets.etr import EdgeTaskReceiver
from nvflare.edge.widgets.tp_runner import TPRunner
from nvflare.edge.widgets.tpo_runner import TPORunner
from nvflare.fuel.utils.validation_utils import check_object_type, check_positive_int, check_positive_number, check_str
from nvflare.job_config.api import FedJob
from nvflare.job_config.file_source import FileSource


class EdgeJob(FedJob):

    def __init__(
        self,
        name: str,
        edge_method: str,
        min_clients: int = 1,
    ):
        """Constructor of EdgeJob

        Args:
            name: name of the job.
            edge_method: method for matching job request. Goes to the job's meta.
            min_clients: min number of clients required for the job.
        """
        check_str("edge_method", edge_method)

        FedJob.__init__(self, name=name, min_clients=min_clients, meta_props={"edge_method": edge_method})

        self.server_config_added = False
        self.client_config_added = False
        self.simulation_set = False

    def configure_server(
        self,
        assessor: Assessor,
        num_rounds: int = 1,
        task_name: str = "train",
        assess_interval: float = 0.5,
        update_interval: float = 1.0,
    ):
        """Set up server config.

        Args:
            assessor: The Assessor object for assessing workflow progress.
            num_rounds: number of rounds.
            task_name: name of the task.
            assess_interval: how often to perform assessment.
            update_interval: how often the clients should send updates.

        Returns: None

        """
        pass

    def configure_client(
        self,
        aggregator_factory: AggregatorFactory,
        max_model_versions: Optional[int] = None,
        update_timeout=5.0,
        executor_task_name="train",
        simulation_config_file: str = None,
    ):
        """Set up client config.

        Args:
            aggregator_factory: an AggregatorFactory object to create aggregators when needed.
            max_model_versions: max number of model versions to keep.
            update_timeout: timeout for status update messages.
            executor_task_name: task name for executor.
            simulation_config_file: config file for local simulation (optional).

        Returns: None

        """
        pass

    def _configure_executor(self, aggr_factory_id, max_model_versions, update_timeout):
        pass

    def configure_simulation_with_file(self, simulation_config_file: str):
        """Configure simulation with a config file.

        Args:
            simulation_config_file: the simulation config file.

        Returns:

        """
        pass

    def configure_simulation(
        self,
        task_processor: DeviceTaskProcessor,
        job_timeout: float = 60.0,
        num_devices: int = 1000,
        num_workers: int = 10,
    ):
        """Configure simulation with a DeviceTaskProcessor.

        Args:
            task_processor: the DeviceTaskProcessor object to be used for processing tasks.
            job_timeout: timeout for trying to get job.
            num_devices: number of devices to simulate.
            num_workers: number of workers for executing tasks.

        Returns: None

        """
        pass
