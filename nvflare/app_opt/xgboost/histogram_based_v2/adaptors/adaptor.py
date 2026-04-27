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
import multiprocessing
import sys
import threading
import time
from abc import ABC, abstractmethod
from typing import Tuple

from xgboost.core import XGBoostError

from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_context import FLContext
from nvflare.apis.signal import Signal
from nvflare.apis.workspace import Workspace
from nvflare.app_opt.xgboost.histogram_based_v2.defs import Constant
from nvflare.app_opt.xgboost.histogram_based_v2.runners.xgb_runner import AppRunner
from nvflare.fuel.utils.log_utils import configure_logging, get_obj_logger
from nvflare.fuel.utils.validation_utils import check_object_type
from nvflare.security.logging import secure_format_exception, secure_log_traceback


class _RunnerStarter:
    """This small class is used to start XGB client runner. It is used when running the runner in a thread
    or in a separate process.

    """

    def __init__(self, app_name: str, runner, in_process: bool, workspace: Workspace, job_id: str):
        self.app_name = app_name
        self.runner = runner
        self.in_process = in_process
        self.workspace = workspace
        self.job_id = job_id
        self.error = None
        self.started = True
        self.stopped = False
        self.exit_code = 0
        self.logger = get_obj_logger(self)

    def start(self, ctx: dict):
        """Start the runner and wait for it to finish.

        Args:
            ctx:

        Returns:

        """
        pass


class AppAdaptor(ABC, FLComponent):
    """AppAdaptors are used to integrate FLARE with App Target (Server or Client) in run time."""

    def __init__(self, app_name: str, in_process: bool):
        """Constructor of AppAdaptor.

        Args:
            app_name (str): The name of the application.
            in_process (bool): Whether to call the `AppRunner.run()` in the same process or not.
        """
        FLComponent.__init__(self)
        self.abort_signal = None
        self.app_runner = None
        self.app_name = app_name
        self.in_process = in_process
        self.starter = None
        self.process = None

    def set_runner(self, runner: AppRunner):
        """Set the App Runner that will be used to run app processing logic.
        Note that the adaptor is only responsible for starting the runner appropriately (in a thread or in a
        separate process).

        Args:
            runner (AppRunner): the runner to be set

        Returns: None

        """
        pass

    def set_abort_signal(self, abort_signal: Signal):
        """Called by XGB Controller/Executor to set the abort_signal.

        The abort_signal is assigned by FLARE's XGB Controller/Executor. It is used by the Controller/Executor
        to tell the adaptor that the job has been aborted.

        Args:
            abort_signal: the abort signal assigned by the caller.

        Returns: None

        """
        pass

    def initialize(self, fl_ctx: FLContext):
        """Called by the Controller/Executor to initialize the adaptor.

        Args:
            fl_ctx: the FL context

        Returns: None

        """
        pass

    @abstractmethod
    def start(self, fl_ctx: FLContext):
        """Called by XGB Controller/Executor to start the target.
        If any error occurs when starting the target, this method should raise an exception.

        Args:
            fl_ctx: the FL context.

        Returns: None

        """
        pass

    @abstractmethod
    def stop(self, fl_ctx: FLContext):
        """Called by XGB Controller/Executor to stop the target.
        If any error occurs when stopping the target, this method should raise an exception.

        Args:
            fl_ctx: the FL context.

        Returns: None

        """
        pass

    @abstractmethod
    def configure(self, config: dict, fl_ctx: FLContext):
        """Called by XGB Controller/Executor to configure the adaptor.
        If any error occurs, this method should raise an exception.

        Args:
            config: config data
            fl_ctx: the FL context

        Returns: None

        """
        pass

    @abstractmethod
    def _is_stopped(self) -> Tuple[bool, int]:
        """Called by the adaptor's monitor to know whether the target is stopped.
        Note that this method is not called by XGB Controller/Executor.

        Returns: a tuple of: whether the target is stopped, and return code (if stopped)

        Note that a non-zero return code is considered abnormal completion of the target.

        """
        pass

    def _monitor(self, fl_ctx: FLContext, target_stopped_cb):
        pass

    def monitor_target(self, fl_ctx: FLContext, target_stopped_cb):
        """Called by XGB Controller/Executor to monitor the health of the target.

        The monitor periodically checks the abort signal. Once set, it calls the adaptor's stop() method
        to stop the running of the target.

        The monitor also periodically checks whether the target is already stopped (by calling the is_stopped
        method). If the target is stopped, the monitor will call the specified target_stopped_cb.

        Args:
            fl_ctx: FL context
            target_stopped_cb: the callback function to be called when the target is stopped.

        Returns: None

        """
        pass

    def start_runner(self, run_ctx: dict, fl_ctx: FLContext):
        pass

    def stop_runner(self):
        pass

    def is_runner_stopped(self) -> Tuple[bool, int]:
        pass
