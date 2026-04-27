# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
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
import os
import sys
import traceback

SECURE_LOGGING_VAR_NAME = "NVFLARE_SECURE_LOGGING"


def is_secure() -> bool:
    """Checks if logging is set to secure mode.

    This is controlled by the system environment variable NVFLARE_SECURE_LOGGING.
    To set secure mode, set this var to 'true' or '1'.

    Returns:
        A boolean indicates whether logging is set in secure mode.
    """
    pass


class _Frame(object):
    def __init__(self, line_text):
        self.line_text = line_text
        self.count = 1


def _format_exc_securely() -> str:
    """Mimics traceback.format_exc() but exclude detailed call info and exception detail since
    they might contain sensitive info.

    Returns:
        A formatted string of current exception and call stack.

    """
    pass


def secure_format_traceback() -> str:
    """Formats the traceback of the current exception and returns a string without sensitive info.

    If secure mode is set, only include file names, line numbers and func names.
    Exception info only includes the type of the exception.
    If secure mode is not set, return the result of traceback.format_exc().

    Returns:
        A formatted string
    """
    pass


def secure_log_traceback(logger: logging.Logger = None):
    """Logs the traceback.

    If secure mode is set, the traceback only includes file names, line numbers and func names;
    and only the type of the exception.
    If secure mode is not set, the traceback will be logged normally as traceback.print_exc().

    Args:
       logger: if not None, this logger is used to log the traceback detail. If None, the root logger will be used.

    """
    pass


def secure_format_exception(e: Exception) -> str:
    """Formats the specified exception and return a string without sensitive info.

    If secure mode is set, only return the type of the exception;
    If secure mode is not set, return the result of str(e).

    Args:
       e: the exception to be formatted

    Returns:
        A formatted exception string.
    """
    pass
