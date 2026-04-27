# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
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
import os.path
import re
import uuid
from typing import Any, Dict, List, Optional, Union

from nvflare.apis.executor import Executor
from nvflare.apis.filter import Filter
from nvflare.apis.impl.controller import Controller
from nvflare.apis.job_def import ALL_SITES, SERVER_SITE_NAME
from nvflare.fuel.utils.class_utils import get_component_init_parameters
from nvflare.fuel.utils.validation_utils import check_object_type, check_positive_int, check_str
from nvflare.job_config.fed_app_config import ClientAppConfig, FedAppConfig, ServerAppConfig
from nvflare.job_config.fed_job_config import FedJobConfig

from .defs import FilterType, JobTargetType

SPECIAL_CHARACTERS = '"!@#$%^&*()+?=,<>/'

_ADD_TO_JOB_METHOD_NAME = "add_to_fed_job"


class FedApp:
    def __init__(self, app_config: Union[ClientAppConfig, ServerAppConfig]):
        """FedApp handles `ClientAppConfig` and `ServerAppConfig` and allows setting task result or task data filters."""
        self.app_config = app_config
        self._used_ids = []

        # obj_id => comp_id
        # obj_id is the Python's object ID; comp_id is the component ID for job config
        # _oid_to_cid keeps the mapping between obj_id and comp_id.
        # this is to make sure that when the same object is used, it is configured only once in the job.
        self._oid_to_cid = {}

    def get_app_config(self):
        pass

    def add_task_result_filter(self, tasks: List[str], task_filter: Filter):
        pass

    def add_task_data_filter(self, tasks: List[str], task_filter: Filter):
        pass

    def add_component(self, component, comp_id=None):
        # is the component already configured?
        pass

    def _generate_id(self, id: str = "") -> str:
        pass

    def generate_tracked_id(self, id: str = "") -> str:
        pass

    def add_external_script(self, ext_script: str):
        """Register external script to include them in custom directory.

        Args:
            ext_script: List of external scripts that need to be deployed to the client/server.
        """
        pass

    def add_external_dir(self, ext_dir: str):
        """Register external folder to include them in custom directory.

        Args:
            ext_dir: external folder that need to be deployed to the client/server.
        """
        pass

    def add_file_source(self, src_path: str, dest_dir=None, app_folder_type=None):
        pass

    def add_params(self, args: Dict[str, any]):
        """Add additional system configuration parameters to be included in the generated JSON configs.

        Args:
            args: Dictionary of system configuration parameters (e.g., {"timeout": 600, "max_retries": 3})
        """
        pass

    def _add_resource(self, resource: str):
        pass

    def add_resources(self, resources: List[str]):
        """Add resources to the job. To be used by job component programmer.

        Args:
            resources:

        Returns:

        """
        pass


class JobCtx:
    def __init__(self, obj: Any, target: str, comp_id: str):
        self.obj = obj
        self.target = target
        self.comp_id = comp_id


class ClientApp(FedApp):
    def __init__(self):
        """Wrapper around `ClientAppConfig`."""
        super().__init__(ClientAppConfig())

    def add_executor(self, executor: Executor, tasks=None):
        pass


class ServerApp(FedApp):
    """Wrapper around `ServerAppConfig`."""

    def __init__(self):
        super().__init__(ServerAppConfig())

    def add_controller(self, controller: Controller, id=None):
        pass


class FedJob:
    def __init__(
        self,
        name: str = "fed_job",
        min_clients: int = 1,
        mandatory_clients: Optional[List[str]] = None,
        meta_props: Optional[Dict[str, Any]] = None,
    ) -> None:
        """FedJob allows users to generate job configurations in a Pythonic way.
        The `to()` routine allows users to send different components to either the server or clients.

        Args:
            name: the name of the NVFlare job
            min_clients: the minimum number of clients for the job
            mandatory_clients: mandatory clients to run the job (optional)

        """
        check_str("name", name)
        check_positive_int("min_clients", min_clients)
        if mandatory_clients:
            check_object_type("mandatory_clients", mandatory_clients, list)
        if meta_props:
            check_object_type("meta_props", meta_props, dict)

        self.name = name
        self.clients = []
        self.job: FedJobConfig = FedJobConfig(
            job_name=self.name,
            min_clients=min_clients,
            mandatory_clients=mandatory_clients,
            meta_props=meta_props,
        )
        self._deploy_map = {}
        self._deployed = False
        self._components = {}

    def set_app_packages(self, app_packages: List[str]):
        """Set app packages.
        When generating job config, code from these packages will not be included into "custom" folder.

        Args:
            app_packages: app packages to be set

        Returns: None

        """
        pass

    def set_up_client(self, target: str):
        """Setup routine called by FedJob when first sending object to a client target.

        Args:
            target: the target to perform setup.

        Returns:

        """
        pass

    def _add_server_app(self, obj: ServerApp, target: str):
        pass

    def _add_client_app(self, obj: ClientApp, target: str):
        pass

    def to(
        self,
        obj: Any,
        target: str,
        id=None,
        **kwargs,
    ) -> Any:
        """Assign an object to the target. For end users.

        Args:
            obj: the object to be assigned
            target: the target that the object is assigned to
            id: the id of the object
            **kwargs: additional args to be passed to the object's add_to_fed_job method.

        If the obj provides the add_to_fed_job method, it will be called with the kwargs.
        This method must follow this signature:

            add_to_fed_job(job, ctx, ...)

            job: this is the job (self)
            ctx: this is the JobCtx that keeps contextual info of this call.

        The add_to_fed_job function is usually implemented in FL component classes.
        When implementing this function, you should not use anything in the ctx; instead, you should use
        the "add_xxx" methods of the "job" object: add_component, add_resources, add_filter, add_executor, etc.

        Returns:
            result of add_to_job_method if called, or id of added component

        """
        pass

    def _add_referenced_components(self, base_component, target):
        """Adds any other components the object might have referenced via id"""
        pass

    def _get_app(self, ctx: JobCtx):
        pass

    def add_component(self, comp_id: str, obj: Any, ctx: JobCtx):
        """Add a component to the job. To be used by job component programmer.

        Args:
            comp_id: component id
            obj: component to be added to job.
            ctx: JobCtx for contextual information.

        Returns:
            final id assigned to component.

        """
        pass

    def add_controller(self, obj: Controller, ctx: JobCtx):
        """Add a Controller object to the job. To be used by controller programmer.

        Args:
            obj: Controller to be added to job.
            ctx: JobCtx for contextual information.

        Returns:

        """
        pass

    def add_executor(self, obj: Executor, tasks: List[str], ctx: JobCtx):
        """Add an executor to the job. To be used by executor programmer.

        Args:
            obj: Executor to be added to job.
            tasks: List of tasks that should be handled. If `None`, all tasks will be handled using `[*]`.
            ctx: JobCtx for contextual information.

        Returns:

        """
        pass

    def add_filter(self, obj: Filter, filter_type: str, tasks, ctx: JobCtx):
        """Add a filter to the job. To be used by filter programmer.

        Args:
            obj: Filter to be added to job.
            filter_type: The type of filter used. Either `FilterType.TASK_RESULT` or `FilterType.TASK_DATA`.
            tasks: List of tasks that Filter applies to.
            ctx: JobCtx for contextual information.

        Returns:

        """
        pass

    def add_resources(self, resources: List[str], ctx: JobCtx):
        """Add resources to the job. To be used by job component programmer.

        Args:
            resources: List of filenames or directories to be added to job.
            ctx: JobCtx for contextual information.

        Returns:

        """
        pass

    def add_file_source(self, src_path: str, dest_dir, app_folder_type, ctx: JobCtx):
        """Add a file source to the job. To be used by job component programmer.

        Args:
            src_path: path to the source to be added to job.
            dest_dir: destination path for the source
            app_folder_type: type of app folder to place the files
            ctx: JobCtx for contextual information.

        Returns:

        """
        pass

    def add_params(self, args: Dict[str, any], ctx: JobCtx):
        """Add additional system configuration parameters to the job. To be used by job component programmer.

        Args:
            args: Dictionary of configuration parameters (e.g., {"timeout": 600, "max_retries": 3})
            ctx: JobCtx for contextual information.

        Returns:

        """
        pass

    def to_server(
        self,
        obj: Any,
        id=None,
        **kwargs,
    ):
        """assign an object to the server. For end users.

        Args:
            obj: The object to be assigned. The obj will be given a default `id` if none is provided based on its type.
            id: Optional user-defined id for the object. Defaults to `None` and ID will automatically be assigned.
            **kwargs: additional args to be passed to the object's add_to_fed_job method.

        Returns:
            result of add_to_job_method if called, or id of added component

        """
        pass

    def to_clients(
        self,
        obj: Any,
        id=None,
        **kwargs,
    ):
        """assign an object to all clients. For end users.

        Args:
            obj (Any): Object to be deployed.
            id: Optional user-defined id for the object. Defaults to `None` and ID will automatically be assigned.
            **kwargs: additional args to be passed to the object's add_to_fed_job method.

        Returns:
            result of add_to_job_method if called, or id of added component

        """
        pass

    def add_file_to(self, src_path: str, target: str, dest_dir=None, app_folder_type=None):
        """Add a file to a specific target's app directory.

        Args:
            src_path: Local path to the file to be bundled into the job.
            target: Target site name (e.g., "server", "site-1", or ALL_SITES for all clients).
            dest_dir: Optional subdirectory within the target folder to place the file.
            app_folder_type: Type of app folder to place the file. Valid values: "custom", "config".
                If not specified, defaults to "custom".
        """
        pass

    def add_file_to_server(self, src_path: str, dest_dir=None, app_folder_type=None):
        """Add a file to the server app directory.

        Args:
            src_path: Local path to the file to be bundled into the job.
            dest_dir: Optional subdirectory within the target folder to place the file.
            app_folder_type: Type of app folder to place the file. Valid values: "custom", "config".
                If not specified, defaults to "custom".
        """
        pass

    def add_file_to_clients(self, src_path: str, dest_dir=None, app_folder_type=None):
        """Add a file to all client apps' directory.

        Args:
            src_path: Local path to the file to be bundled into the job.
            dest_dir: Optional subdirectory within the target folder to place the file.
            app_folder_type: Type of app folder to place the file. Valid values: "custom", "config".
                If not specified, defaults to "custom".
        """
        pass

    def _validate_target(self, target):
        pass

    def _set_all_app(self, client_app: ClientApp, server_app: ServerApp):
        pass

    def _set_site_app(self, app: FedApp, target: str):
        pass

    def _set_all_apps(self):
        pass

    def export_job(self, job_root: str):
        """Export job config to `job_root` directory with name `self.name`.
        For end users.

        Args:
            job_root: directory to export job configuration.

        Returns:

        """
        pass

    def simulator_run(
        self,
        workspace: str,
        n_clients: Optional[int] = None,
        clients: Optional[List[str]] = None,
        threads: Optional[int] = None,
        gpu: Optional[str] = None,
        log_config: Optional[str] = None,
    ):
        """Run the job with the simulator with the `workspace` using `clients` and `threads`.
        For end users.

        Args:
            workspace: workspace directory for job.
            n_clients: number of clients.
            clients: client names.
            threads: number of threads.
            gpu: gpu assignments for simulating clients, comma separated
            log_config: log config mode ('concise', 'msg_only', 'full', 'verbose'), filepath, or level

        Returns:
        """
        pass

    def as_id(self, obj: Any) -> str:
        """Generate and return uuid for `obj`. For end users.
        If this id is referenced by another added object, this `obj` will also be added as a component.
        """
        pass

    @staticmethod
    def check_kwargs(args_to_check: dict, args_expected: dict):
        """Check kwargs for arguments. Raise Error if required arg is missing, or unexpected arg is given.

        Args:
            args_to_check (dict): kwargs dictionary to check.
            args_expected (dict): dictionary of argument name to boolean of whether argument is required (True) or optional (False).

        """
        pass


def has_add_to_job_method(obj: Any) -> bool:
    pass


def validate_object_for_job(name, obj, obj_type):
    """Check whether the specified object is valid for job.
    The object must either have the add_to_fed_job method or is valid object type.

    Args:
        name: name of the object
        obj: the object to be checked
        obj_type: the object type that the object should be, if it doesn't have the add_to_fed_job method.

    Returns: None

    """
    pass
