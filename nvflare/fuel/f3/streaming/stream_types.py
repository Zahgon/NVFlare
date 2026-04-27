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
import threading
from abc import ABC, abstractmethod
from typing import Any, Callable, Optional

from nvflare.fuel.f3.connection import BytesAlike

log = logging.getLogger(__name__)


class StreamError(Exception):
    """All stream API throws this error"""

    pass


class StreamCancelled(StreamError):
    """Streaming is cancelled by sender"""

    pass


class Stream(ABC):
    """A raw, read-only, seekable binary byte stream"""

    def __init__(self, size: int = 0, headers: Optional[dict] = None):
        """Constructor for stream

        Args:
            size: The total size of stream. 0 if unknown
            headers: Optional headers to be passed to the receiver
        """
        self.size = size
        self.pos = 0
        self.headers = headers
        self.closed = False

    def get_size(self) -> int:
        pass

    def get_pos(self):
        pass

    def get_headers(self) -> Optional[dict]:
        pass

    @abstractmethod
    def read(self, size: int) -> BytesAlike:
        """Read and return up to size bytes. It can return less but not more than the size.
        An empty bytes object is returned if the stream reaches the end.

        Args:
            size: Up to (but maybe less) this many bytes will be returned

        Returns:
            Binary data. If empty, it means the stream is depleted (EOS)
        """
        pass

    def close(self):
        """Close the stream"""
        pass

    def seek(self, offset: int):
        """Change the stream position to the given byte offset.
        Args:
            offset: Offset relative to the start of the stream

        Exception:
            StreamError: If the stream is not seekable
        """
        pass


class StreamTaskSpec(ABC):
    def cancel(self):
        """Cancel the task

        Returns:

        """
        pass


class StreamFuture:
    """Future class for all stream calls.

    Fashioned after concurrent.futures.Future
    """

    def __init__(self, stream_id: int, headers: Optional[dict] = None, task_handle: StreamTaskSpec = None):
        self.stream_id = stream_id
        self.headers = headers
        self.waiter = threading.Event()
        self.lock = threading.Lock()
        self.error: Optional[StreamError] = None
        self.value = None
        self.size = 0
        self.progress = 0
        self.done_callbacks = []
        self.task_handle = task_handle

    def get_stream_id(self) -> int:
        pass

    def get_headers(self) -> Optional[dict]:
        pass

    def get_size(self) -> int:
        pass

    def set_size(self, size: int):
        pass

    def get_progress(self) -> int:
        pass

    def set_progress(self, progress: int):
        pass

    def cancel(self):
        """Cancel the future if possible.

        Returns True if the future was cancelled, False otherwise. A future
        cannot be cancelled if it is running or has already completed.
        """
        pass

    def cancelled(self):
        pass

    def running(self):
        """Return True if the future is currently executing."""
        pass

    def done(self):
        """Return True of the future was cancelled or finished executing."""
        pass

    def add_done_callback(self, done_cb: Callable, *args, **kwargs):
        """Attaches a callable that will be called when the future finishes.

        Args:
            done_cb: A callable that will be called with this future completes
        """
        pass

    def result(self, timeout=None) -> Any:
        """Return the result of the call that the future represents.

        Args:
            timeout: The number of seconds to wait for the result if the future
                isn't done. If None, then there is no limit on the wait time.

        Returns:
            The final result

        Raises:
            CancelledError: If the future was cancelled.
            TimeoutError: If the future didn't finish executing before the given
                timeout.
        """
        pass

    def exception(self, timeout=None):
        """Return the exception raised by the call that the future represents.

        Args:
            timeout: The number of seconds to wait for the exception if the
                future isn't done. If None, then there is no limit on the wait
                time.

        Returns:
            The exception raised by the call that the future represents or None
            if the call completed without raising.

        Raises:
            CancelledError: If the future was cancelled.
            TimeoutError: If the future didn't finish executing before the given
                timeout.
        """
        pass

    def set_result(self, value: Any):
        """Sets the return value of work associated with the future.

        Silently ignored if the future already has an error (e.g. cancel() raced with
        a completing _read_stream). Raises StreamError if called twice with a result,
        as that is always a programming error.
        """
        pass

    def set_exception(self, exception):
        """Sets the result of the future as being the given exception.

        Idempotent: a duplicate call is logged and silently ignored because
        race conditions can legitimately produce multiple set_exception calls
        (e.g. _read_stream error racing with the outer blob_cb exception handler).
        """
        pass

    def _invoke_callbacks(self):
        pass
