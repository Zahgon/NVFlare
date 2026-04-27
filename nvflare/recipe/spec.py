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

import sys
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Dict, List, Optional, Union


def _consume_recipe_args() -> tuple:
    """Strip --export / --export-dir from sys.argv and return (export, export_dir).

    Called once at module import time so that the caller's argparse never sees
    these flags regardless of the order in which parse_args() and execute() appear
    in job.py.
    """
    pass


# Intentional import-time sys.argv mutation: strip --export / --export-dir before
# any ArgumentParser.parse_args() call in job.py runs. Doing this lazily (e.g. inside
# execute()) would be too late if the caller calls parse_args() first, which is the
# common pattern. The mutation is safe because job.py is always the process entry point.
_RECIPE_EXPORT, _RECIPE_EXPORT_DIR = _consume_recipe_args()


def _peek_recipe_args(argv: Optional[List[str]] = None) -> tuple:
    """Return the export flags consumed at import time (argv argument is ignored)."""
    pass


from nvflare.apis.filter import Filter
from nvflare.app_common.widgets.decomposer_reg import DecomposerRegister
from nvflare.fuel.utils.fobs import Decomposer
from nvflare.job_config.api import FedJob
from nvflare.job_config.defs import FilterType


class ExecEnv(ABC):

    def __init__(self, extra: Optional[dict] = None):
        """Constructor of ExecEnv

        Args:
            extra: a dict of extra properties
        """
        if extra is None:
            extra = {}
        if not isinstance(extra, dict):
            raise ValueError(f"extra must be dict but got {type(extra)}")
        self.extra = extra

    def get_extra_prop(self, prop_name: str, default=None):
        """Get the specified extra property.

        Args:
            prop_name: name of the property
            default: the default value to return if the named property does not exist.

        Returns: value of the property or the default

        """
        pass

    @abstractmethod
    def deploy(self, job: FedJob) -> str:
        """Deploy a FedJob and return an execution response.

        Args:
            job: The FedJob to deploy.

        Returns:
            str: The job ID.
        """
        pass

    @abstractmethod
    def get_job_status(self, job_id: str) -> Optional[str]:
        """Get the status of a job.

        Args:
            job_id: The job ID to check status for.

        Returns:
            Optional[str]: The status of the job, or None if not supported.
        """
        pass

    @abstractmethod
    def abort_job(self, job_id: str) -> None:
        """Abort a running job.

        Args:
            job_id: The job ID to abort.
        """
        pass

    @abstractmethod
    def get_job_result(self, job_id: str, timeout: float = 0.0) -> Optional[str]:
        """Get the result workspace of a job.

        Args:
            job_id: The job ID to get results for.
            timeout: The timeout for the job to complete. Defaults to 0.0 (no timeout).

        Returns:
            Optional[str]: The result workspace path if job completed, None if still running or stopped early.
        """
        pass

    def stop(self, clean_up: bool = False) -> None:
        """Stop the execution environment and optionally clean up resources.

        This method is called after job execution to ensure proper cleanup.
        Default implementation is a no-op. Override in subclasses that need cleanup.

        Args:
            clean_up: If True, remove workspace and temporary files after stopping.
                      If False, only stop running processes but preserve workspace.
                      Defaults to False.
        """
        pass


class Recipe(ABC):

    def __init__(self, job: FedJob):
        """This is base class of a recipe. Recipes are implemented by jobs.
        A concrete recipe must provide the job for recipe implementation.

        Args:
            job: the job that implements the recipe.
        """
        self.job = job

    def process_env(self, env: ExecEnv):
        """Process environment-specific configuration.

        Subclasses can override to add environment-specific processing.
        Script validation is handled by each ExecEnv subclass in deploy().
        """
        pass

    def _snapshot_additional_params(self) -> Dict[str, Dict]:
        pass

    def _restore_additional_params(self, snapshot: Dict[str, Dict]) -> None:
        pass

    def _replace_additional_params_for_targets(self, targets: List[str], new_params: dict) -> None:
        pass

    @contextmanager
    def _temporary_exec_params(
        self, server_exec_params: Optional[dict] = None, client_exec_params: Optional[dict] = None
    ):
        """Temporarily override per-target additional_params during execute/export.

        Semantics:
        - None: leave the target's existing additional_params unchanged.
        - non-empty dict: temporarily apply/merge those params for the target.
        - empty dict ({}): temporarily clear the target's additional_params for this call.

        Any original additional_params are restored when the context exits.
        """
        pass

    def _add_to_client_apps(self, obj, clients: Optional[List[str]] = None, **kwargs):
        """Add an object to client apps, preserving existing per-site structure.

        Args:
            obj: Object to add to clients.
            clients: Optional list of specific client names. If None, applies to all clients.
            **kwargs: Extra options forwarded to `job.to()`/`job.to_clients()`.
        """
        pass

    def add_client_input_filter(
        self, filter: Filter, tasks: Optional[List[str]] = None, clients: Optional[List[str]] = None
    ):
        """Add a filter to clients for incoming tasks from the server.

        Args:
            filter: the filter to be added
            tasks: tasks that the filter applies to
            clients: client names to add, if None, all clients will be added.

        Returns: None

        """
        pass

    def add_client_output_filter(
        self, filter: Filter, tasks: Optional[List[str]] = None, clients: Optional[List[str]] = None
    ):
        """Add a filter to clients for outgoing result to server.

        Args:
            filter: the filter to be added
            tasks: tasks that the filter applies to
            clients: client names to add, if None, all clients will be added.

        Returns: None

        """
        pass

    def add_client_config(self, config: Dict, clients: Optional[List[str]] = None):
        """Add top-level configuration parameters to config_fed_client.json.

        Args:
            config: Dictionary of configuration parameters to add.
            clients: Optional list of specific client names. If None, applies to all clients.

        Raises:
            TypeError: If config is not a dictionary.
        """
        pass

    def add_client_file(self, file_path: str, clients: Optional[List[str]] = None):
        """Add a file or directory to client apps.

        The file will be added to the client's custom directory and bundled with the job.
        Can be a script, configuration file, or any resource needed by clients.

        Args:
            file_path: Path to the file or directory to add to clients.
            clients: Optional list of specific client names. If None, applies to all clients.

        Raises:
            TypeError: If file_path is not a string.

        Example:
            # Add a wrapper script to all clients
            recipe.add_client_file("client_wrapper.sh")

            # Add a script to specific clients
            recipe.add_client_file("custom_script.py", clients=["site1", "site2"])
        """
        pass

    def add_server_output_filter(self, filter: Filter, tasks: Optional[List[str]] = None):
        """Add a filter to the server for outgoing tasks to clients.

        Args:
            filter: the filter to be added
            tasks: tasks that the filter applies to

        Returns: None

        """
        pass

    def add_server_input_filter(self, filter: Filter, tasks: Optional[List[str]] = None):
        """Add a filter to server for incoming task result from clients. .

        Args:
            filter: the filter to be added
            tasks: tasks that the filter applies to

        Returns: None

        """
        pass

    def add_server_config(self, config: Dict):
        """Add top-level configuration parameters to config_fed_server.json.

        Args:
            config: Dictionary of configuration parameters to add.

        Raises:
            TypeError: If config is not a dictionary.
        """
        pass

    def add_server_file(self, file_path: str):
        """Add a file or directory to server app.

        The file will be added to the server's custom directory and bundled with the job.
        Can be a script, configuration file, or any resource needed by the server.

        Args:
            file_path: Path to the file or directory to add to server.

        Raises:
            TypeError: If file_path is not a string.

        Example:
            # Add a wrapper script to server
            recipe.add_server_file("server_wrapper.sh")
        """
        pass

    @staticmethod
    def _get_full_class_name(obj):
        """
        Returns the fully qualified name of an object.
        """
        pass

    def add_decomposers(self, decomposers: List[Union[str, Decomposer]]):
        """Add decomposers to the job

        Args:
            decomposers: spec of decomposers. Can be class names or Decomposer objects

        Returns: None

        """
        pass

    def export(
        self,
        job_dir: str,
        server_exec_params: Optional[dict] = None,
        client_exec_params: Optional[dict] = None,
        env: Optional[ExecEnv] = None,
    ):
        """Export the recipe to a job definition.

        Args:
            job_dir: directory where the job will be exported to.
            server_exec_params: execution params for the server
            client_exec_params: execution params for clients
            env: the environment that the exported job will be running in

        Returns: None

        """
        pass

    def run(
        self, env: ExecEnv, server_exec_params: Optional[dict] = None, client_exec_params: Optional[dict] = None
    ) -> "Run":
        """Run the recipe in a specified execution environment.

        Args:
            env: the execution environment
            server_exec_params: execution params for the server
            client_exec_params: execution params for clients

        Returns: Run to get job ID and execution results

        """
        pass

    def execute(
        self,
        env: ExecEnv,
        server_exec_params: Optional[dict] = None,
        client_exec_params: Optional[dict] = None,
    ) -> Optional["Run"]:
        """Execute or export the recipe based on command-line flags.

        Transparently checks sys.argv for ``--export`` / ``--export-dir`` without
        interfering with the caller's own argument parser.

        * ``python job.py``                         → run the job
        * ``python job.py --export``                → export to ``./fl_job``
        * ``python job.py --export --export-dir X`` → export to ``X``

        Args:
            env: the execution environment
            server_exec_params: execution params for the server
            client_exec_params: execution params for clients

        Returns:
            Run when executing; raises SystemExit(0) when exporting so callers
            need not guard against a None return value.
        """
        pass
