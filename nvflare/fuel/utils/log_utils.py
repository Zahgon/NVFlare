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
import copy
import inspect
import json
import logging
import logging.config
import os
import re
from logging import Logger
from logging.handlers import RotatingFileHandler
from typing import Union

from nvflare.apis.workspace import Workspace

DEFAULT_LOG_JSON = "log_config.json"
FL_LOG_LEVEL = "FL_LOG_LEVEL"


class LogMode:
    RELOAD = "reload"
    FULL = "full"
    CONCISE = "concise"
    MSG_ONLY = "msg_only"
    VERBOSE = "verbose"


# Predefined log dicts based from DEFAULT_LOG_JSON
with open(os.path.join(os.path.dirname(__file__), DEFAULT_LOG_JSON), "r") as f:
    default_log_dict = json.load(f)

concise_log_dict = copy.deepcopy(default_log_dict)
concise_log_dict["formatters"]["consoleFormatter"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
concise_log_dict["handlers"]["consoleHandler"]["filters"] = ["FLFilter"]

msg_only_log_dict = copy.deepcopy(default_log_dict)
msg_only_log_dict["formatters"]["consoleFormatter"]["fmt"] = "%(message)s"
msg_only_log_dict["handlers"]["consoleHandler"]["filters"] = ["FLFilter"]

verbose_log_dict = copy.deepcopy(default_log_dict)
verbose_log_dict["formatters"]["consoleFormatter"][
    "fmt"
] = "%(asctime)s - %(identity)s - %(fullName)s - %(levelname)s - %(fl_ctx)s - %(message)s"
verbose_log_dict["loggers"]["root"]["level"] = "DEBUG"

logmode_config_dict = {
    LogMode.FULL: default_log_dict,
    LogMode.CONCISE: concise_log_dict,
    LogMode.MSG_ONLY: msg_only_log_dict,
    LogMode.VERBOSE: verbose_log_dict,
}


class ANSIColor:
    # Basic ANSI color codes
    COLORS = {
        "black": "30",
        "red": "31",
        "bold_red": "31;1",
        "green": "32",
        "yellow": "33",
        "blue": "34",
        "magenta": "35",
        "cyan": "36",
        "white": "37",
        "grey": "38",
        "reset": "0",
    }

    # Default logger level:color mappings
    DEFAULT_LEVEL_COLORS = {
        "NOTSET": COLORS["grey"],
        "DEBUG": COLORS["grey"],
        "INFO": COLORS["grey"],
        "WARNING": COLORS["yellow"],
        "ERROR": COLORS["red"],
        "CRITICAL": COLORS["bold_red"],
    }

    @classmethod
    def colorize(cls, text: str, color: str) -> str:
        """Wrap text with the given ANSI SGR color.

        Args:
            text (str): text to colorize.
            color (str): ANSI SGR color code or color name defined in ANSIColor.COLORS.

        Returns:
            colorized text
        """
        pass


class BaseFormatter(logging.Formatter):
    def __init__(self, fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt=None, style="%"):
        """Default formatter for log records.

        The following attributes are added to the record and can be configured in `fmt` with '%(<attribute>)s'
            - record.name: base name
            - record.fullName: full name
            - record.fl_ctx: bracked fl ctx key value pairs if exists in the message
            - record.identity: identity from fl_ctx if fl_ctx exists

        Args:
            fmt (str): format string which uses LogRecord attributes.
            datefmt (str): date/time format string. Defaults to '%Y-%m-%d %H:%M:%S'.
            style (str): style character '%' '{' or '$' for format string.

        """
        self.fmt = fmt
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def format(self, record):
        # make a copy of record for modification
        pass

    def remove_empty_attributes(self):
        pass


class ColorFormatter(BaseFormatter):
    def __init__(
        self,
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt=None,
        style="%",
        level_colors=ANSIColor.DEFAULT_LEVEL_COLORS,
        logger_colors={},
    ):
        """Format colors based on log levels. Optionally can provide mapping based on logger names.

        Args:
            fmt (str): format string which uses LogRecord attributes.
            datefmt (str): date/time format string. Defaults to '%Y-%m-%d %H:%M:%S'.
            style (str): style character '%' '{' or '$' for format string.
            level_colors (Dict[str, str]): dict of levelname: ANSI color. Defaults to ANSIColor.DEFAULT_LEVEL_COLORS.
            logger_colors (Dict[str, str]): dict of loggername: ANSI color. Defaults to {}.

        """
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.level_colors = level_colors
        self.logger_colors = logger_colors

    def format(self, record):
        pass


class JsonFormatter(BaseFormatter):
    def __init__(
        self,
        fmt="%(asctime)s - %(identity)s - %(name)s - %(fullName)s - %(levelname)s - %(fl_ctx)s - %(message)s",
        datefmt=None,
        style="%",
    ):
        """Format log records into JSON.

        Args:
            fmt (str): format string which uses LogRecord attributes. Attributes are used for JSON keys.
            datefmt (str): date/time format string. Defaults to '%Y-%m-%d %H:%M:%S'.
            style (str): style character '%' '{' or '$' for format string.

        """
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.fmt_dict = self.generate_fmt_dict(self.fmt)

    def generate_fmt_dict(self, fmt: str) -> dict:
        # Parse the `fmt` string and create a mapping of keys to LogRecord attributes
        pass

    def formatMessageDict(self, record) -> dict:
        pass

    def format(self, record) -> str:
        pass


class LoggerNameFilter(logging.Filter):
    def __init__(self, logger_names=["nvflare"], exclude_logger_names=[], allow_all_error_logs=True):
        """Filter log records based on logger names.

        Args:
            logger_names (List[str]): list of logger names to allow through filter
            exclude_logger_names (List[str]): list of logger names to disallow through filter (takes precedence over allowing from logger_names)
            allow_all_error_logs (bool): allow all log records with levelno > logging.INFO through filter, even if they are not from a logger in logger_names.
                Defaults to True.

        """
        super().__init__()
        self.logger_names = logger_names
        self.exclude_logger_names = exclude_logger_names
        self.allow_all_error_logs = allow_all_error_logs

    def filter(self, record):
        pass

    def matches_name(self, name, logger_names) -> bool:
        pass


def get_module_logger(module=None, name=None) -> logging.Logger:
    # Get module logger name adhering to logger hierarchy. Optionally add name as a suffix.
    pass


def get_obj_logger(obj) -> logging.Logger:
    # Get object logger name adhering to logger hierarchy.
    pass


def get_script_logger() -> logging.Logger:
    # Get script logger name adhering to logger hierarchy. Based on package and filename. If not in a package, default to custom.
    pass


def custom_logger(logger: logging.Logger) -> logging.Logger:
    # From a logger, return a new logger with "custom" prepended to the logger name
    pass


def configure_logging(workspace: Workspace, job_id: str = None, file_prefix: str = ""):
    # Read log_config.json from workspace, update with file_prefix, and apply to log_root of th workspace
    pass


def apply_log_config(dict_config, dir_path: str = "", file_prefix: str = ""):
    # Update log config dictionary with file_prefix, and apply to dir_path
    pass


def dynamic_log_config(config: Union[dict, str], dir_path: str, reload_path: str, file_prefix: str = ""):
    # Dynamically configure log given a config (dict, filepath, LogMode, or level), apply the config to the proper locations.

    pass


def validate_site_log_config(config) -> str:
    """Validate site-wide log configuration input.

    Site-wide log reconfiguration is intentionally narrower than general
    dictConfig support: only simple log levels and built-in log modes are
    allowed on this admin command path.
    """
    pass


def add_log_file_handler(log_file_name):
    pass


def print_logger_hierarchy(package_name="nvflare", level_colors=ANSIColor.DEFAULT_LEVEL_COLORS):
    def get_effective_level(logger_name):
        pass
    def print_hierarchy(logger_name, indent_level=0):
        pass
    pass


def center_message(message: str, boarder_str="=", line_width=80):
    pass
