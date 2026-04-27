# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
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

from typing import List, Optional


def repeat_to_length(string_to_expand, length):
    """Repeats string_to_expand to fill up a string of the provided length.

    Args:
        string_to_expand: string to repeat
        length: length of string to return

    Returns: generated string of provided length

    """
    pass


class Table(object):
    def __init__(self, headers: Optional[List[str]] = None, meta_rows=None):
        """A structure with header and rows of records.

        Note:
            The header will be converted to capital letters.

        Args:
            headers: headers of the table
        """
        self.rows = []
        self.meta_rows = meta_rows
        if headers and len(headers) > 0:
            new_headers = []
            for h in headers:
                new_headers.append(h.upper())
            self.rows.append(new_headers)

    def set_rows(self, rows, meta_rows=None):
        """Sets the rows of records."""
        pass

    def add_row(self, row: List[str], meta: Optional[dict] = None):
        """Adds a record."""
        pass

    def write(self, writer):
        # compute the number of cols
        pass
