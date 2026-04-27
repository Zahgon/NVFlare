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

import json
import os
import time
from typing import List, Optional

from nvflare.apis.fl_constant import AdminCommandNames
from nvflare.apis.job_def import DEFAULT_STUDY, JobMetaKey
from nvflare.apis.utils.format_check import name_check
from nvflare.apis.workspace import Workspace
from nvflare.fuel.common.excepts import ConfigError
from nvflare.fuel.hci.client.api import AdminAPI, APIStatus, ResultKey
from nvflare.fuel.hci.client.api_spec import AdminConfigKey, UidSource
from nvflare.fuel.hci.client.config import secure_load_admin_config
from nvflare.fuel.hci.cmd_arg_utils import (
    join_args,
    process_targets_into_str,
    validate_file_string,
    validate_options_string,
    validate_path_string,
    validate_required_target_string,
)
from nvflare.fuel.hci.proto import MetaKey, MetaStatusValue, ProtoKey, ReplyKeyword
from nvflare.fuel.utils.log_utils import get_obj_logger, validate_site_log_config

from .api_spec import (
    AuthenticationError,
    AuthorizationError,
    ClientInfo,
    ClientsStillRunning,
    CommandError,
    InternalError,
    InvalidArgumentError,
    InvalidJobDefinition,
    InvalidTarget,
    JobInfo,
    JobNotDone,
    JobNotFound,
    JobNotRunning,
    JobTimeout,
    MonitorReturnCode,
    NoClientsAvailable,
    NoConnection,
    NoReply,
    ServerInfo,
    SessionClosed,
    SessionSpec,
    SystemInfo,
    TargetType,
)

_VALID_TARGET_TYPES = [TargetType.ALL, TargetType.SERVER, TargetType.CLIENT]

__all__ = ["NoConnection", "NoReply", "SystemInfo", "TargetType"]


def _validate_target_strs(targets: List[str]) -> None:
    """Validate that each item in ``targets`` is a well-formed target name.

    Wraps :func:`process_targets_into_str` for its validation side-effect only —
    the joined string it returns is intentionally discarded because callers then
    do ``parts.extend(targets)`` so that every name becomes its own command
    argument. If the joined string were appended instead, :func:`join_args`
    would wrap the whitespace-containing element in double quotes, and the
    server's ``shlex.split`` in ``parse_command_line`` would collapse multiple
    names back into a single token (see NVBug 6098943).
    """
    pass


class Session(SessionSpec):
    def __init__(
        self,
        username: str,
        startup_path: str,
        secure_mode: bool = True,
        debug: bool = False,
        study: str = DEFAULT_STUDY,
    ):
        """Initializes a session with the NVFLARE system.

        Args:
            username (str): string of username to log in with
            startup_path (str): path to the provisioned startup kit, which contains endpoint of the system
            secure_mode (bool): whether to log in with secure mode
            debug (bool): turn on debug or not
            study (str): active study context for submitted jobs and session-scoped job listing; defaults to
                "default"
        """
        assert isinstance(username, str), "username must be str"
        assert isinstance(startup_path, str), "startup_path must be str"
        assert isinstance(study, str), "study must be str"
        assert os.path.isdir(startup_path), f"startup kit does not exist at {startup_path}"

        workspace = Workspace(root_dir=startup_path)
        conf = secure_load_admin_config(workspace)
        admin_config = conf.get_admin_config()
        if not admin_config:
            raise ConfigError("Missing admin section in fed_admin configuration.")

        if not secure_mode:
            admin_config[AdminConfigKey.UID_SOURCE] = UidSource.CERT

        self.username = username
        upload_dir = admin_config.get(AdminConfigKey.UPLOAD_DIR)
        download_dir = admin_config.get(AdminConfigKey.DOWNLOAD_DIR)
        if not os.path.isdir(download_dir):
            os.makedirs(download_dir)

        self.api = AdminAPI(
            admin_config=admin_config,
            user_name=username,
            debug=debug,
            event_handlers=conf.handlers,
            study=study,
        )
        self.upload_dir = upload_dir
        self.download_dir = download_dir
        self._study = study
        if name_check(self._study, "study")[0]:
            raise ValueError(
                f"study name '{self._study}' contains unsupported characters. Use only lowercase letters, numbers, underscores, and hyphens."
            )

    def close(self):
        """Close the session."""
        pass

    def try_connect(self, timeout):
        pass

    def _do_command(self, command: str, enforce_meta=True, props=None):
        pass

    @staticmethod
    def _validate_job_id(job_id: str):
        pass

    def clone_job(self, job_id: str) -> str:
        """Create a new job by cloning a specified job.

        Args:
            job_id: job to be cloned

        Returns: ID of the new job

        """
        pass

    def submit_job(self, job_definition_path: str) -> str:
        """Submit a predefined job to the NVFLARE system.

        Args:
            job_definition_path: path to the folder that defines a NVFLARE job

        Returns: the job id if accepted by the system

        If the submission fails, an exception will be raised.

        """
        pass

    def get_job_meta(self, job_id: str) -> dict:
        """Get the meta info of the specified job.

        Args:
            job_id: ID of the job

        Returns: a dict of job metadata

        """
        pass

    def list_jobs(
        self,
        detailed: bool = False,
        limit: Optional[int] = None,
        id_prefix: Optional[str] = None,
        name_prefix: Optional[str] = None,
        reverse: bool = False,
        **kwargs,
    ) -> List[dict]:
        """Get the job info from the server.

        Args:
            detailed (bool): True to get the detailed information for each job, False by default
            limit (int, optional): maximum number of jobs to show, with 0 or None to show all (defaults to None to show all)
            id_prefix (str): if included, only return jobs with the beginning of the job ID matching the id_prefix
            name_prefix (str): if included, only return jobs with the beginning of the job name matching the name_prefix
            reverse (bool): if specified, list jobs in the reverse order of submission times
            **kwargs: deprecated legacy aliases accepted for compatibility

        Returns: a list of job metadata

        """
        pass

    def download_job_result(self, job_id: str, destination: str = None) -> str:
        """Download result of the job.

        Args:
            job_id (str): ID of the job
            destination (str): optional directory to move the downloaded result into.
                If not specified, result is left in the download_dir from the admin config.

        Returns: folder path to the location of the job result

        """
        pass

    def list_job_components(self, job_id: str) -> List[str]:
        """Get the list of additional job components for the specified job.

        Args:
            job_id (str): ID of the job

        Returns: a list of the additional job components

        """
        pass

    def download_job_components(self, job_id: str) -> str:
        """Download additional job components (e.g., ERRORLOG_site-1) for a specified job.

        Args:
            job_id (str): ID of the job

        Returns: folder path to the location of the downloaded additional job components

        """
        pass

    def abort_job(self, job_id: str):
        """Abort the specified job.

        Args:
            job_id (str): job to be aborted

        Returns:
            str: the message from the server

        If the job is already done, no effect;
        If job is not started yet, it will be cancelled and won't be scheduled.
        If the job is being executed, it will be aborted.

        """
        pass

    def delete_job(self, job_id: str):
        """Delete the specified job completely from the system.

        Args:
            job_id (str): job to be deleted

        Returns:
            None

        The job will be deleted from the job store if the job is not currently running.

        """
        pass

    def get_system_info(self):
        """Get general system information.

        Returns: a SystemInfo object

        """
        pass

    def _do_get_system_info(self, cmd: str):
        pass

    def get_client_job_status(self, client_names: List[str] = None) -> List[dict]:
        """Get job status info of specified FL clients.

        Args:
            client_names (List[str]): names of the clients to get status info

        Returns: A list of jobs running on the clients. Each job is described by a dict of: id, app name and status.
        If there are multiple jobs running on one client, the list contains one entry for each job for that client.
        If no FL clients are connected or the server failed to communicate to them, this method returns None.

        """
        pass

    def restart(self, target_type: str, client_names: Optional[List[str]] = None) -> dict:
        """Restart the server, specific clients, or all participants.

        Args:
            target_type: ``server``, ``client``, or ``all``
            client_names: when target_type is ``client``, restrict to these clients (empty = all clients)

        Returns: a dict with detailed info about the restart request.
        """
        pass

    def shutdown(self, target_type: str, client_names: Optional[List[str]] = None) -> dict:
        """Shut down the server, specific clients, or all participants.

        Args:
            target_type: ``server``, ``client``, or ``all``
            client_names: when target_type is ``client``, restrict to these clients (empty = all clients)

        Returns: a dict with detailed info about the shutdown request.
        """
        pass

    def set_timeout(self, value: float):
        """Set a session-specific command timeout.

        This is the amount of time the server will wait for responses after sending commands to FL clients.

        Note that this value is only effective for the current API session.

        Args:
            value (float): a positive float number for the timeout in seconds

        Returns: None

        """
        pass

    def unset_timeout(self):
        """Unset the session-specific command timeout.

        Once unset, the FL Admin Server's default timeout will be used.

        Returns: None

        """
        pass

    def get_available_apps_to_upload(self):
        """Get defined FLARE app folders from the upload folder on the machine the FLARE API is running.

        Returns: a list of app folders

        """
        pass

    def shutdown_system(self):
        """Shutdown the whole NVFLARE system including FL server, and all FL clients.

        Returns: None

        Note: the user must be a Project Admin to use this method; otherwise the NOT_AUTHORIZED exception will be raised.

        """
        pass

    def ls_target(self, target: str, options: Optional[str] = None, path: Optional[str] = None) -> str:
        """Run the "ls" command on the specified target and return the result.

        Args:
            target: the target (server or a client name) the command will be run on
            options: options of the "ls" command
            path: the optional file path

        Returns: result of "ls" command

        """
        pass

    def cat_target(self, target: str, options: Optional[str] = None, file: Optional[str] = None) -> str:
        """Run the "cat" command on the specified target and return the result.

        Args:
            target: the target (server or a client name) the command will be run on
            options: options of the "cat" command
            file: the file that the "cat" command will run against

        Returns: result of "cat" command

        """
        pass

    def tail_target(self, target: str, options: Optional[str] = None, file: Optional[str] = None) -> str:
        """Run the "tail" command on the specified target and return the result.

        Args:
            target: the target (server or a client name) the command will be run on
            options: options of the "tail" command
            file: the file that the "tail" command will run against

        Returns: result of "tail" command

        """
        pass

    def tail_target_log(self, target: str, options: Optional[str] = None) -> str:
        """Run the "tail log.txt" command on the specified target and return the result.

        Args:
            target: the target (server or a client name) the command will be run on
            options: options of the "tail" command

        Returns: result of "tail" command

        """
        pass

    def head_target(self, target: str, options: Optional[str] = None, file: Optional[str] = None) -> str:
        """Run the "head" command on the specified target and return the result.

        Args:
            target: the target (server or a client name) the command will be run on
            options: options of the "head" command
            file: the file that the "head" command will run against

        Returns: result of "head" command

        """
        pass

    def head_target_log(self, target: str, options: Optional[str] = None) -> str:
        """Run the "head log.txt" command on the specified target and return the result.

        Args:
            target: the target (server or a client name) the command will be run on
            options: options of the "head" command

        Returns: result of "head" command

        """
        pass

    def grep_target(
        self, target: str, options: Optional[str] = None, pattern: Optional[str] = None, file: Optional[str] = None
    ) -> str:
        """Run the "grep" command on the specified target and return the result.

        Args:
            target: the target (server or a client name) the command will be run on
            options: options of the "grep" command
            pattern: the grep pattern
            file: the file that the "grep" command will run against

        Returns: result of "grep" command

        """
        pass

    def get_working_directory(self, target: str) -> str:
        """Get the working directory of the specified target.

        Args:
            target (str): the target (server of a client name)

        Returns: current working directory of the specified target

        """
        pass

    def _shell_command_on_target(
        self,
        cmd: str,
        target: str,
        options,
        fp,
        pattern=None,
        pattern_required=False,
        fp_required=False,
        fp_type="path",
    ) -> str:
        pass

    @staticmethod
    def _get_string_data(reply: dict) -> str:
        pass

    @staticmethod
    def _get_dict_data(reply: dict) -> dict:
        pass

    @staticmethod
    def _get_study_payload(reply: dict) -> dict:
        pass

    @staticmethod
    def _validate_study_name(study: str):
        pass

    @staticmethod
    def _validate_study_sites(sites: List[str]):
        pass

    @staticmethod
    def _validate_study_user(user: str):
        pass

    @staticmethod
    def _validate_study_site_orgs(site_orgs: List[str]):
        pass

    def register_study(
        self, study: str, sites: Optional[List[str]] = None, site_orgs: Optional[List[str]] = None
    ) -> dict:
        pass

    def add_study_site(
        self, study: str, sites: Optional[List[str]] = None, site_orgs: Optional[List[str]] = None
    ) -> dict:
        pass

    def remove_study_site(
        self, study: str, sites: Optional[List[str]] = None, site_orgs: Optional[List[str]] = None
    ) -> dict:
        pass

    def remove_study(self, study: str) -> dict:
        pass

    def list_studies(self) -> dict:
        pass

    def show_study(self, study: str) -> dict:
        pass

    def add_study_user(self, study: str, user: str) -> dict:
        pass

    def remove_study_user(self, study: str, user: str) -> dict:
        pass

    def show_stats(self, job_id: str, target_type: str, targets: Optional[List[str]] = None) -> dict:
        """Show processing stats of specified job on specified targets.

        Args:
            job_id (str): ID of the job
            target_type (str): type of target (server or client)
            targets: list of client names if target type is "client". All clients if not specified.

        Returns: a dict that contains job stats on specified targets. The key of the dict is target name. The value is
        a dict of stats reported by different system components (ServerRunner or ClientRunner).

        """
        pass

    def show_errors(self, job_id: str, target_type: str, targets: Optional[List[str]] = None) -> dict:
        """Show processing errors of specified job on specified targets.

        Args:
            job_id (str): ID of the job
            target_type (str): type of target (server or client)
            targets: list of client names if target type is "client". All clients if not specified.

        Returns: a dict that contains job errors (if any) on specified targets. The key of the dict is target name.
        The value is a dict of errors reported by different system components (ServerRunner or ClientRunner).

        """
        pass

    def reset_errors(self, job_id: str):
        """Clear errors for all system targets for the specified job.

        Args:
            job_id (str): ID of the job

        Returns: None

        """
        pass

    def _collect_info(self, cmd: str, job_id: str, target_type: str, targets=None) -> dict:
        pass

    def check_status(self, target_type: str, targets=None) -> dict:
        """Get status of specified system target(s).

        Args:
            target_type (str): type of target (server, client, or all)
            targets: list of client names if target type is "client". All clients if not specified.

        Returns: a dict with status information

        """
        pass

    def report_resources(self, target_type: str, targets=None) -> dict:
        """Report resources of specified system target(s).

        Args:
            target_type (str): type of target (server, client, or all)
            targets: list of client names if target type is "client". All clients if not specified.

        Returns: a dict with resource information.

        Notes:
            The underlying admin protocol currently returns this data as a table-shaped payload.
            Session normalizes the current table layout into a simpler site->value dict for CLI
            consumers. If the server-side table shape changes in the future, this adapter needs to
            be updated alongside that protocol change.

        """
        pass

    def report_version(self, target_type: str, targets: Optional[List[str]] = None) -> dict:
        """Report NVFlare version for specified system target(s).

        Args:
            target_type (str): type of target (server, client, or all)
            targets: list of client names if target type is "client". All clients if not specified.

        Returns: a dict with version information per site

        """
        pass

    def remove_client(self, client_name: str) -> None:
        """Remove a client from the system.

        Args:
            client_name (str): name of the client to remove

        Returns: None

        """
        pass

    def get_job_logs(
        self, job_id: str, target: str = "server", tail_lines: int = None, grep_pattern: str = None
    ) -> dict:
        """Retrieve job logs from server workspace.

        Args:
            job_id (str): ID of the job
            target (str): target site name. Only "server" is currently supported.
            tail_lines (int): optional number of tail lines to retrieve
            grep_pattern (str): optional grep pattern to filter log lines

        Returns: dict with "logs" keys mapping site name to log text.

        """
        pass

    def configure_job_log(self, job_id: str, config, target: str = "all") -> None:
        """Configure logging for a running job.

        Args:
            job_id (str): ID of the job (must be RUNNING)
            config: str (level or LogMode), dict (dictConfig), or file path
            target (str): "all", "server", or a client site name. Any value
                other than "all" or "server" is sent through the client-targeted
                admin command path.

        Returns: None

        """
        pass

    def configure_site_log(self, config, target: str = "all") -> None:
        """Configure site-level logging.

        Args:
            config: str log level or built-in LogMode
            target (str): target site name or "all"

        Returns: None

        """
        pass

    def wait_for_job(self, job_id: str, timeout: float = 0.0, poll_interval: float = 2.0) -> dict:
        """Block until job reaches a terminal state.

        Args:
            job_id (str): ID of the job to wait for
            timeout (float): how long to wait; 0 means wait indefinitely
            poll_interval (float): seconds between status polls

        Returns: final job meta dict

        Raises: JobTimeout if timeout is exceeded before job finishes

        """
        pass

    def do_app_command(self, job_id: str, topic: str, cmd_data) -> dict:
        """Ask a running job to execute an app command

        Args:
            job_id: the ID of the running job
            topic: topic of the command
            cmd_data: the data of the command. Must be JSON serializable.

        Returns: result of the app command

        If the job is not currently running, an exception will occur. User must make sure that the job is running when
        calling this method.

        """
        pass

    def get_connected_client_list(self) -> List[ClientInfo]:
        """Get the list of connected clients.

        Returns: a list of ClientInfo objects

        """
        pass

    def get_client_env(self, client_names=None):
        """Get running environment values for specified clients. The env includes values of client name,
        workspace directory, root url of the FL server, and secure mode or not.

        These values can be used for 3rd-party system configuration (e.g. CellPipe to connect to the FLARE system).

        Args:
            client_names: clients to get env from. None means all clients.

        Returns: list of env info for specified clients.

        Raises: InvalidTarget exception, if no clients are connected or an invalid client name is specified

        """
        pass

    def do_command(self, command: str, props=None):
        """Execute an admin command.

        Args:
            command: the command to be executed
            props: extra properties passed with the command

        Returns:

        """
        pass

    def get_job_status(self, job_id: str) -> Optional[str]:
        """Get the status of a job.

        Args:
            job_id: ID of the job

        Returns: status of the job

        """
        pass

    def monitor_job_and_return_job_meta(
        self, job_id: str, timeout: float = 0.0, poll_interval: float = 2.0, cb=None, *cb_args, **cb_kwargs
    ) -> (MonitorReturnCode, Optional[dict]):
        """Monitor the job progress.

        Monitors until one of the conditions occurs:
            - job is done
            - timeout
            - the status_cb returns False

        Args:
            job_id (str): the job to be monitored
            timeout (float): how long to monitor. If 0, never time out.
            poll_interval (float): how often to poll job status
            cb: if provided, callback to be called after each status poll

        Returns: a tuple of (MonitorReturnCode, job meta dict)

        Every time the cb is called, it must return a bool indicating whether the monitor
        should continue. If False, this method ends.

        """
        pass


def basic_cb_with_print(session: Session, job_id: str, job_meta, *cb_args, **cb_kwargs) -> bool:
    """This is a sample callback to use with monitor_job.

    This demonstrates how a custom callback can be used.

    When the CLI output helper is available, use it so human progress updates follow the CLI
    stdout/stderr routing policy. Non-CLI callers still get a plain print() fallback.

    """
    pass


def new_session(
    username: str,
    startup_kit_location: str,
    secure_mode: bool = True,
    debug: bool = False,
    timeout: float = 10.0,
    study: str = DEFAULT_STUDY,
    command_timeout: float = None,
    auto_login_max_tries: int = None,
) -> Session:
    pass


def new_secure_session(
    username: str,
    startup_kit_location: str,
    debug: bool = False,
    timeout: float = 10.0,
    study: str = DEFAULT_STUDY,
    command_timeout: float = None,
    auto_login_max_tries: int = None,
) -> Session:
    """Create a new secure FLARE API session with the NVFLARE system.

    Args:
        username (str): username assigned to the user
        startup_kit_location (str): path to the provisioned startup folder, the root admin dir containing the startup folder
        debug (bool): enable debug mode
        timeout (float): how long to try to establish the session, in seconds
        study (str): active study context for submitted jobs and session-scoped job listing; defaults to "default"
        command_timeout (float): optional per-session command timeout sent to the admin server
        auto_login_max_tries (int): optional cap on API auto-login retries before connect

    Returns: a Session object

    """
    pass


def new_insecure_session(
    startup_kit_location: str,
    debug: bool = False,
    timeout: float = 10.0,
    study: str = DEFAULT_STUDY,
) -> Session:
    """Create a new insecure FLARE API session with the NVFLARE system.

    Args:
        startup_kit_location (str): path to the provisioned startup folder
        debug (bool): enable debug mode
        timeout (float): how long to try to establish the session, in seconds
        study (str): active study context for submitted jobs and session-scoped job listing; defaults to "default"

    Returns: a Session object

    The username for insecure session is always "admin".

    """
    pass
