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
from threading import Lock
from typing import Any, Dict, Optional, Union

from nvflare.apis.analytix import AnalyticsDataType
from nvflare.app_common.abstract.fl_model import FLModel

# this import is to let existing scripts import client.api
from .api_context import ClientAPIType  # noqa: F401
from .api_context import APIContext

global_context_lock = Lock()
context_dict = {}
default_context = None


def get_context(ctx: Optional[APIContext] = None) -> APIContext:
    """Gets an APIContext.

    Args:
        ctx (Optional[APIContext]): The context to use,
            if None means use default context. Defaults to None.

    Raises:
        RuntimeError: if can't get a valid APIContext.

    Returns:
        An APIContext.
    """
    pass


def init(rank: Optional[Union[str, int]] = None, config_file: Optional[str] = None) -> APIContext:
    """Initializes NVFlare Client API environment.

    Args:
        rank (str): local rank of the process.
            It is only useful when the training script has multiple worker processes. (for example multi GPU)
        config_file (str): client api configuration.

    Returns:
        APIContext
    """
    pass


def receive(timeout: Optional[float] = None, ctx: Optional[APIContext] = None) -> Optional[FLModel]:
    """Receives model from NVFlare side.

    Returns:
        An FLModel received.
    """
    pass


def send(model: FLModel, clear_cache: bool = True, ctx: Optional[APIContext] = None) -> None:
    """Sends the model to NVFlare side.

    Args:
        model (FLModel): The FLModel object to be sent.
        clear_cache (bool): Whether to clear the cache after send.
    """
    pass


def system_info(ctx: Optional[APIContext] = None) -> Dict:
    """Gets NVFlare system information.

    System information will be available after a valid FLModel is received.
    It does not retrieve information actively.

    Note:
        system information includes job id and site name.

    Returns:
       A dict of system information.

    """
    pass


def get_config(ctx: Optional[APIContext] = None) -> Dict:
    """Gets the ClientConfig dictionary.

    Returns:
        A dict of the configuration used in Client API.
    """
    pass


def get_job_id(ctx: Optional[APIContext] = None) -> str:
    """Gets job id.

    Returns:
        The current job id.
    """
    pass


def get_site_name(ctx: Optional[APIContext] = None) -> str:
    """Gets site name.

    Returns:
        The site name of this client.
    """
    pass


def get_task_name(ctx: Optional[APIContext] = None) -> str:
    """Gets task name.

    Returns:
        The task name.
    """
    pass


def is_running(ctx: Optional[APIContext] = None) -> bool:
    """Returns whether the NVFlare system is up and running.

    Returns:
        True, if the system is up and running. False, otherwise.
    """
    pass


def is_train(ctx: Optional[APIContext] = None) -> bool:
    """Returns whether the current task is a training task.

    Returns:
        True, if the current task is a training task. False, otherwise.
    """
    pass


def is_evaluate(ctx: Optional[APIContext] = None) -> bool:
    """Returns whether the current task is an evaluate task.

    Returns:
        True, if the current task is an evaluate task. False, otherwise.
    """
    pass


def is_submit_model(ctx: Optional[APIContext] = None) -> bool:
    """Returns whether the current task is a submit_model task.

    Returns:
        True, if the current task is a submit_model. False, otherwise.
    """
    pass


def log(key: str, value: Any, data_type: AnalyticsDataType, ctx: Optional[APIContext] = None, **kwargs):
    """Logs a key value pair.

    We suggest users use the high-level APIs in nvflare/client/tracking.py

    Args:
        key (str): key string.
        value (Any): value to log.
        data_type (AnalyticsDataType): the data type of the "value".
        kwargs: additional arguments to be included.

    Returns:
        whether the key value pair is logged successfully
    """
    pass


def clear(ctx: Optional[APIContext] = None):
    """Clears the cache."""
    pass


def shutdown(ctx: Optional[APIContext] = None):
    """Releases all threads and resources used by the API and stops operation."""
    pass
