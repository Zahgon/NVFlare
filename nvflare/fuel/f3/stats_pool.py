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

import csv
import json
import sys
import threading
import time
from typing import List, Tuple, Union

_KEY_MAX = "max"
_KEY_MIN = "min"
_KEY_NAME = "name"
_KEY_DESC = "description"
_KEY_TOTAL = "total"
_KEY_COUNT = "count"
_KEY_UNIT = "unit"
_KEY_MARKS = "marks"
_KEY_COUNTER_NAMES = "counter_names"
_KEY_CAT_DATA = "cat_data"


class StatsMode:

    COUNT = "count"
    PERCENT = "percent"
    AVERAGE = "avg"
    MIN = "min"
    MAX = "max"


VALID_HIST_MODES = [StatsMode.COUNT, StatsMode.PERCENT, StatsMode.AVERAGE, StatsMode.MAX, StatsMode.MIN]


def format_value(v: float, n=3):
    pass


class _Bin:
    def __init__(self, count=0, total_value=0.0, min_value=None, max_value=None):
        self.count = count
        self.total = total_value
        self.min = min_value
        self.max = max_value

    def record_value(self, value: float):
        pass

    def get_content(self, mode=StatsMode.COUNT, total_count=0):
        pass

    def to_dict(self) -> dict:
        pass

    @staticmethod
    def from_dict(d: dict):
        pass


class StatsPool:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def to_dict(self) -> dict:
        pass

    def get_table(self, mode):
        pass

    @staticmethod
    def from_dict(d: dict):
        pass


class RecordWriter:
    def write(self, pool_name: str, category: str, value: float, report_time: float):
        pass

    def close(self):
        pass


class HistPool(StatsPool):
    def __init__(self, name: str, description: str, marks: Union[List[float], Tuple], unit: str, record_writer=None):
        if record_writer:
            if not isinstance(record_writer, RecordWriter):
                raise TypeError(f"record_writer must be RecordWriter but got {type(record_writer)}")

        StatsPool.__init__(self, name, description)
        self.update_lock = threading.Lock()
        self.unit = unit
        self.marks = marks
        self.record_writer = record_writer  # used for writing raw records
        self.cat_bins = {}  # category name => list of bins

        if not marks:
            raise ValueError("marks not specified")
        if len(marks) < 2:
            raise ValueError(f"marks must have at least two numbers but got {len(marks)}")

        for i in range(1, len(marks)):
            if marks[i] <= marks[i - 1]:
                raise ValueError(f"marks must contain increasing values, but got {marks}")

        # A range is defined: left <= N < right  [...)
        # [..., M1) [M1, M2) [M2, M3) [M3, ...)
        m = sys.float_info.max
        self.ranges = [(-m, marks[0])]
        self.range_names = [f"<{marks[0]}"]
        for i in range(len(marks) - 1):
            self.ranges.append((marks[i], marks[i + 1]))
            self.range_names.append(f"{marks[i]}-{marks[i + 1]}")
        self.ranges.append((marks[-1], m))
        self.range_names.append(f">={marks[-1]}")

    def record_value(self, category: str, value: float):
        pass

    def get_table(self, mode=StatsMode.COUNT):
        pass

    def to_dict(self):
        pass

    @staticmethod
    def from_dict(d: dict):
        pass


class CounterPool(StatsPool):
    def __init__(self, name: str, description: str, counter_names: List[str], dynamic_counter_name=True):
        if not counter_names and not dynamic_counter_name:
            raise ValueError("counter_names cannot be empty")
        StatsPool.__init__(self, name, description)
        self.counter_names = counter_names
        self.cat_counters = {}  # dict of cat_name => counter dict (counter_name => int)
        self.dynamic_counter_name = dynamic_counter_name
        self.update_lock = threading.Lock()

    def increment(self, category: str, counter_name: str, amount=1):
        pass

    def get_table(self, mode=""):
        pass

    def to_dict(self):
        pass

    @staticmethod
    def from_dict(d: dict):
        pass


def new_time_pool(name: str, description="", marks=None, record_writer=None) -> HistPool:
    pass


def new_message_size_pool(name: str, description="", marks=None, record_writer=None) -> HistPool:
    pass


def parse_hist_mode(mode: str) -> str:
    pass


class StatsPoolManager:

    _CONFIG_KEY_SAVE_POOLS = "save_pools"

    lock = threading.Lock()
    pools = {}  # name => pool
    pool_config = {}
    record_writer = None

    @classmethod
    def _check_name(cls, name, scope):
        pass

    @classmethod
    def set_pool_config(cls, config: dict):
        pass

    @classmethod
    def set_record_writer(cls, record_writer: RecordWriter):
        pass

    @classmethod
    def _keep_hist_records(cls, name):
        pass

    @classmethod
    def add_time_hist_pool(cls, name: str, description: str, marks=None, scope=None):
        # check pool config
        pass

    @classmethod
    def add_msg_size_pool(cls, name: str, description: str, marks=None, scope=None):
        pass

    @classmethod
    def add_counter_pool(cls, name: str, description: str, counter_names: list, scope=None):
        pass

    @classmethod
    def get_pool(cls, name: str):
        pass

    @classmethod
    def delete_pool(cls, name: str):
        pass

    @classmethod
    def get_table(cls):
        pass

    @classmethod
    def to_dict(cls):
        pass

    @classmethod
    def from_dict(cls, d: dict):
        pass

    @classmethod
    def dump_summary(cls, file_name: str):
        pass

    @classmethod
    def close(cls):
        pass


class CsvRecordHandler(RecordWriter):
    def __init__(self, file_name):
        self.file = open(file_name, "w")
        self.writer = csv.writer(self.file)
        self.lock = threading.Lock()

    def write(self, pool_name: str, category: str, value: float, report_time: float):
        pass

    def close(self):
        pass

    @staticmethod
    def read_records(csv_file_name: str):
        pass


class StatsRecord:
    def __init__(self, pool_name, category, report_time, value):
        self.pool_name = pool_name
        self.category = category
        self.report_time = report_time
        self.value = value


class CsvRecordReader:
    def __init__(self, csv_file_name: str):
        self.csv_file_name = csv_file_name
        self.file = open(csv_file_name)
        self.reader = csv.reader(self.file)

    def __iter__(self):
        return self

    def __next__(self):
        row = next(self.reader)
        if len(row) != 4:
            raise ValueError(f"'{self.csv_file_name}' is not a valid stats pool record file: bad row length {len(row)}")
        pool_name = row[0]
        cat_name = row[1]
        report_time = float(row[2])
        value = float(row[3])
        return StatsRecord(pool_name, cat_name, report_time, value)
