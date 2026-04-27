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
import threading
import time
from threading import Lock
from typing import List, Optional, Tuple, Union

from nvflare.apis.client import Client
from nvflare.apis.controller_spec import ClientTask, SendOrder, Task, TaskCompletionStatus
from nvflare.apis.event_type import EventType
from nvflare.apis.fl_component import FLComponent
from nvflare.apis.fl_constant import ConfigVarName, FLContextKey, SystemConfigs
from nvflare.apis.fl_context import FLContext
from nvflare.apis.job_def import job_from_meta
from nvflare.apis.shareable import ReservedHeaderKey, Shareable, make_copy
from nvflare.apis.signal import Signal
from nvflare.apis.wf_comm_spec import WFCommSpec
from nvflare.fuel.utils.config_service import ConfigService
from nvflare.fuel.utils.msg_root_utils import delete_msg_root
from nvflare.security.logging import secure_format_exception
from nvflare.widgets.info_collector import GroupInfoCollector, InfoCollector

from .any_relay_manager import AnyRelayTaskManager
from .bcast_manager import BcastForeverTaskManager, BcastTaskManager
from .send_manager import SendTaskManager
from .seq_relay_manager import SequentialRelayTaskManager
from .task_manager import TaskCheckStatus, TaskManager

_TASK_KEY_ENGINE = "___engine"
_TASK_KEY_MANAGER = "___mgr"
_TASK_KEY_DONE = "___done"


def _check_positive_int(name, value):
    pass


def _check_inputs(task: Task, fl_ctx: FLContext, targets: Union[List[Client], List[str], None]):
    pass


def _get_client_task(target, task: Task):
    pass


class _DeadClientStatus:
    def __init__(self):
        self.report_time = time.time()
        self.disconnect_time = None


class WFCommServer(FLComponent, WFCommSpec):
    def __init__(self, task_check_period=0.2):
        """Manage life cycles of tasks and their destinations.

        Args:
            task_check_period (float, optional): interval for checking status of tasks. Defaults to 0.2.
        """
        super().__init__()
        self.controller = None
        self._engine = None
        self._tasks = []  # list of standing tasks
        self._client_task_map = {}  # client_task_id => client_task
        self._all_done = False
        self._task_lock = Lock()
        self._task_monitor = threading.Thread(target=self._monitor_tasks, args=(), name="wf_task", daemon=True)
        self._task_check_period = task_check_period
        self._dead_client_grace = 60.0
        self._dead_clients = {}  # clients reported dead: name => _DeadClientStatus
        self._dead_clients_lock = Lock()  # need lock since dead_clients can be modified from different threads
        # make sure check_tasks, process_task_request, process_submission does not interfere with each other
        self._controller_lock = Lock()

    def initialize_run(self, fl_ctx: FLContext):
        """Called by runners to initialize controller with information in fl_ctx.

        .. attention::

            Controller subclasses must not overwrite this method.

        Args:
            fl_ctx (FLContext): FLContext information
        """
        pass

    def _try_again(self) -> Tuple[str, str, Optional[Shareable]]:
        # TODO: how to tell client no shareable available now?
        pass

    def _set_stats(self, fl_ctx: FLContext):
        """Called to set stats into InfoCollector.

        Args:
            fl_ctx (FLContext): info collector is retrieved from fl_ctx with InfoCollector.CTX_KEY_STATS_COLLECTOR key
        """
        pass

    def handle_event(self, event_type: str, fl_ctx: FLContext):
        """Called when events are fired.

        Args:
            event_type (str): all event types, including AppEventType and EventType
            fl_ctx (FLContext): FLContext information with current event type
        """
        pass

    def process_dead_client_report(self, client_name: str, fl_ctx: FLContext):
        pass

    def process_task_request(self, client: Client, fl_ctx: FLContext) -> Tuple[str, str, Shareable]:
        """Called by runner when a client asks for a task.

        .. note::

            This is called in a separate thread.

        Args:
            client (Client): The record of one client requesting tasks
            fl_ctx (FLContext): The FLContext associated with this request

        Raises:
            TypeError: when client is not an instance of Client
            TypeError: when fl_ctx is not an instance of FLContext
            TypeError: when any standing task containing an invalid client_task

        Returns:
            Tuple[str, str, Shareable]: task_name, an id for the client_task, and the data for this request
        """
        pass

    def _do_process_task_request(self, client: Client, fl_ctx: FLContext) -> Tuple[str, str, Shareable]:
        pass

    def handle_exception(self, task_id: str, fl_ctx: FLContext) -> None:
        """Called to cancel one task as its client_task is causing exception at upper level.

        Args:
            task_id (str): an id to the failing client_task
            fl_ctx (FLContext): FLContext associated with this client_task
        """
        pass

    def process_task_check(self, task_id: str, fl_ctx: FLContext):
        pass

    def process_submission(self, client: Client, task_name: str, task_id: str, result: Shareable, fl_ctx: FLContext):
        """Called to process a submission from one client.

        .. note::

            This method is called by a separate thread.

        Args:
            client (Client): the client that submitted this task
            task_name (str): the task name associated this submission
            task_id (str): the id associated with the client_task
            result (Shareable): the actual submitted data from the client
            fl_ctx (FLContext): the FLContext associated with this submission

        Raises:
            TypeError: when client is not an instance of Client
            TypeError: when fl_ctx is not an instance of FLContext
            TypeError: when result is not an instance of Shareable
            ValueError: task_name is not found in the client_task
        """
        pass

    def _do_process_submission(
        self, client: Client, task_name: str, task_id: str, result: Shareable, fl_ctx: FLContext
    ):
        pass

    def _schedule_task(
        self,
        task: Task,
        fl_ctx: FLContext,
        manager: TaskManager,
        targets: Union[List[Client], List[str], None],
        allow_dup_targets: bool = False,
    ):
        pass

    def broadcast(
        self,
        task: Task,
        fl_ctx: FLContext,
        targets: Union[List[Client], List[str], None] = None,
        min_responses: int = 1,
        wait_time_after_min_received: int = 0,
    ):
        """Schedule a broadcast task.  This is a non-blocking call.

        The task is scheduled into a task list.
        Clients can request tasks and controller will dispatch the task to eligible clients.

        Note:
            task.data is deep copied once, after before_task_sent_cb runs for the first client, to protect
            against data corruption from concurrent in-place modifications. This copy is then reused
            for all subsequent clients. As a result:
            - Modifications to task.data in before_task_sent_cb ARE captured in the copy, but only for the
              first client whose callback runs before the snapshot is taken.
            - Modifications to task.data AFTER broadcast returns (e.g., in-place aggregation) do NOT
              affect clients - they receive the protected copy.
            - Per-client data customization in before_task_sent_cb is NOT supported: although the callback
              runs for every client, only modifications from the first client's callback are reflected in the
              shared snapshot, and all clients receive that same snapshot.

        Args:
            task (Task): the task to be scheduled
            fl_ctx (FLContext): FLContext associated with this task
            targets (Union[List[Client], List[str], None], optional): the list of eligible clients or client names
                or None (all clients). Defaults to None.
            min_responses (int, optional): the condition to mark this task as completed because enough clients
                respond with submission. Defaults to 1.
            wait_time_after_min_received (int, optional): a grace period for late clients to contribute their
                submission.  0 means no grace period.
              Submission of late clients in the grace period are still collected as valid submission. Defaults to 0.

        Raises:
            ValueError: min_responses is greater than the length of targets since this condition will make the task,
                if allowed to be scheduled, never exit.
        """
        pass

    def broadcast_and_wait(
        self,
        task: Task,
        fl_ctx: FLContext,
        targets: Union[List[Client], List[str], None] = None,
        min_responses: int = 1,
        wait_time_after_min_received: int = 0,
        abort_signal: Optional[Signal] = None,
    ):
        """Schedule a broadcast task.  This is a blocking call.

        The task is scheduled into a task list.  Clients can request tasks and controller will dispatch the task
        to eligible clients.

        Args:
            task (Task): the task to be scheduled
            fl_ctx (FLContext): FLContext associated with this task
            targets (Union[List[Client], List[str], None], optional): the list of eligible clients or client names
                or None (all clients). Defaults to None.
            min_responses (int, optional): the condition to mark this task as completed because enough clients
                respond with submission. Defaults to 1.
            wait_time_after_min_received (int, optional): a grace period for late clients to contribute their
                submission.  0 means no grace period.
            Submission of late clients in the grace period are still collected as valid submission. Defaults to 0.
            abort_signal (Optional[Signal], optional): as this is a blocking call, this abort_signal informs
                this method to return. Defaults to None.
        """
        pass

    def broadcast_forever(self, task: Task, fl_ctx: FLContext, targets: Union[List[Client], List[str], None] = None):
        """Schedule a broadcast task.  This is a non-blocking call.

        The task is scheduled into a task list.  Clients can request tasks and controller will dispatch
        the task to eligible clients.

        This broadcast will not end.

        Note:
            task.data is deep copied after before_task_sent_cb runs for the first client to protect
            against data corruption from concurrent in-place modifications. This copy is then reused
            for all subsequent clients. As a result:
            - Modifications to task.data in before_task_sent_cb ARE captured in the copy (for first client only)
            - Modifications to task.data after the first client receives the task do NOT affect clients
            - Per-client data customization in before_task_sent_cb is NOT supported (all clients get same copy)

        Args:
            task (Task): the task to be scheduled
            fl_ctx (FLContext): FLContext associated with this task
            targets (Union[List[Client], List[str], None], optional): the list of eligible clients or client names
                or None (all clients). Defaults to None.
        """
        pass

    def send(
        self,
        task: Task,
        fl_ctx: FLContext,
        targets: Union[List[Client], List[str], None] = None,
        send_order: SendOrder = SendOrder.SEQUENTIAL,
        task_assignment_timeout: int = 0,
    ):
        """Schedule a single task to targets.  This is a non-blocking call.

        The task is scheduled into a task list.  Clients can request tasks and controller will dispatch the task
        to eligible clients based on the send_order.

        Args:
            task (Task): the task to be scheduled
            fl_ctx (FLContext): FLContext associated with this task
            targets (Union[List[Client], List[str], None], optional): the list of eligible clients or client names
                or None (all clients). Defaults to None.
            send_order (SendOrder, optional): the order for clients to become eligible.
                SEQUENTIAL means the order in targets is enforced.
                ANY means clients in targets and haven't received task are eligible for task.
                Defaults to SendOrder.SEQUENTIAL.
            task_assignment_timeout (int, optional): how long to wait for one client to pick the task. Defaults to 0.

        Raises:
            ValueError: when task_assignment_timeout is greater than task's timeout.
            TypeError: send_order is not defined in SendOrder
            ValueError: targets is None or an empty list
        """
        pass

    def send_and_wait(
        self,
        task: Task,
        fl_ctx: FLContext,
        targets: Union[List[Client], List[str], None] = None,
        send_order: SendOrder = SendOrder.SEQUENTIAL,
        task_assignment_timeout: int = 0,
        abort_signal: Signal = None,
    ):
        """Schedule a single task to targets.  This is a blocking call.

        The task is scheduled into a task list.  Clients can request tasks and controller will dispatch the task
        to eligible clients based on the send_order.

        Args:
            task (Task): the task to be scheduled
            fl_ctx (FLContext): FLContext associated with this task
            targets (Union[List[Client], List[str], None], optional): the list of eligible clients or client names
                or None (all clients). Defaults to None.
            send_order (SendOrder, optional): the order for clients to become eligible.
                SEQUENTIAL means the order in targets is enforced.
                ANY means clients in targets and haven't received task are eligible for task.
                Defaults to SendOrder.SEQUENTIAL.
            task_assignment_timeout (int, optional): how long to wait for one client to pick the task. Defaults to 0.
            abort_signal (Optional[Signal], optional): as this is a blocking call, this abort_signal informs this
                method to return. Defaults to None.

        """
        pass

    def get_num_standing_tasks(self) -> int:
        """Get the number of tasks that are currently standing.

        Returns:
            int: length of the list of standing tasks
        """
        pass

    def cancel_task(
        self, task: Task, completion_status=TaskCompletionStatus.CANCELLED, fl_ctx: Optional[FLContext] = None
    ):
        """Cancel the specified task.

        Change the task completion_status, which will inform task monitor to clean up this task

        note::

            We only mark the task as completed and leave it to the task monitor to clean up.
            This is to avoid potential deadlock of task_lock.

        Args:
            task (Task): the task to be cancelled
            completion_status (str, optional): the completion status for this cancellation.
                Defaults to TaskCompletionStatus.CANCELLED.
            fl_ctx (Optional[FLContext], optional): FLContext associated with this cancellation. Defaults to None.
        """
        pass

    def cancel_all_tasks(self, completion_status=TaskCompletionStatus.CANCELLED, fl_ctx: Optional[FLContext] = None):
        """Cancel all standing tasks in this controller.

        Args:
            completion_status (str, optional): the completion status for this cancellation.
                Defaults to TaskCompletionStatus.CANCELLED.
            fl_ctx (Optional[FLContext], optional): FLContext associated with this cancellation. Defaults to None.
        """
        pass

    def finalize_run(self, fl_ctx: FLContext):
        """Do cleanup of the coordinator implementation.

        .. attention::

            Subclass controllers should not overwrite finalize_run.

        Args:
            fl_ctx (FLContext): FLContext associated with this action
        """
        pass

    def relay(
        self,
        task: Task,
        fl_ctx: FLContext,
        targets: Union[List[Client], List[str], None] = None,
        send_order: SendOrder = SendOrder.SEQUENTIAL,
        task_assignment_timeout: int = 0,
        task_result_timeout: int = 0,
        dynamic_targets: bool = True,
    ):
        """Schedule a single task to targets in one-after-another style.  This is a non-blocking call.

        The task is scheduled into a task list.  Clients can request tasks and controller will dispatch the task
        to eligible clients based on the send_order.

        Args:
            task (Task): the task to be scheduled
            fl_ctx (FLContext): FLContext associated with this task
            targets (Union[List[Client], List[str], None], optional): the list of eligible clients or client names
                or None (all clients). Defaults to None.
            send_order (SendOrder, optional): the order for clients to become eligible.
              SEQUENTIAL means the order in targets is enforced.
              ANY means any clients that are inside the targets and haven't received the task are eligible.
              Defaults to SendOrder.SEQUENTIAL.
            task_assignment_timeout (int, optional): how long to wait for one client to pick the task. Defaults to 0.
            task_result_timeout (int, optional): how long to wait for current working client to reply its result.
                Defaults to 0.
            dynamic_targets (bool, optional): allow clients not in targets to join at the end of targets list.
                Defaults to True.

        Raises:
            ValueError: when task_assignment_timeout is greater than task's timeout
            ValueError: when task_result_timeout is greater than task's timeout
            TypeError: send_order is not defined in SendOrder
            TypeError: when dynamic_targets is not a boolean variable
            ValueError: targets is None or an empty list but dynamic_targets is False
        """
        pass

    def relay_and_wait(
        self,
        task: Task,
        fl_ctx: FLContext,
        targets: Union[List[Client], List[str], None] = None,
        send_order=SendOrder.SEQUENTIAL,
        task_assignment_timeout: int = 0,
        task_result_timeout: int = 0,
        dynamic_targets: bool = True,
        abort_signal: Optional[Signal] = None,
    ):
        """Schedule a single task to targets in one-after-another style.  This is a blocking call.

        The task is scheduled into a task list.  Clients can request tasks and controller will dispatch the task
        to eligible clients based on the send_order.

        Args:
            task (Task): the task to be scheduled
            fl_ctx (FLContext): FLContext associated with this task
            targets (Union[List[Client], List[str], None], optional): the list of eligible clients or client names
                or None (all clients). Defaults to None.
            send_order (SendOrder, optional): the order for clients to become eligible.
                SEQUENTIAL means the order in targets is enforced.
                ANY means clients in targets and haven't received task are eligible for task.
                Defaults to SendOrder.SEQUENTIAL.
            task_assignment_timeout (int, optional): how long to wait for one client to pick the task. Defaults to 0.
            task_result_timeout (int, optional): how long to wait for current working client to reply its result.
                Defaults to 0.
            dynamic_targets (bool, optional): allow clients not in targets to join at the end of targets list.
                Defaults to True.
            abort_signal (Optional[Signal], optional): as this is a blocking call, this abort_signal informs
                this method to return. Defaults to None.
        """
        pass

    def _check_dead_clients(self):
        pass

    def _monitor_tasks(self):
        pass

    def check_tasks(self):
        pass

    def _do_check_tasks(self):
        pass

    def _get_task_dead_clients(self, task: Task):
        """
        See whether the task is only waiting for response from a dead client
        """
        pass

    @staticmethod
    def _process_finished_task(task, func):
        def wrap(*args, **kwargs):
            pass
        pass

    def wait_for_task(self, task: Task, abort_signal: Signal):
        pass

    def _job_policy_violated(self):
        pass

    def client_is_active(self, client_name: str, reason: str, fl_ctx: FLContext):
        pass

    def get_client_disconnect_time(self, client_name: str):
        """Get the time that the client was deemed disconnected

        Args:
            client_name: name of the client

        Returns: time at which the client was deemed disconnected; or None if the client is not disconnected

        """
        pass
