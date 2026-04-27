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

import argparse
import os

from nvflare.fuel.f3.stats_pool import CsvRecordReader

"""
This tool can be used to compute the total time spent on communication for a job.

NOTE: if all processes (server and clients) are run on the same host, then the computed results are accurate.
If processes are run on different hosts, then these hosts must be synchronized with NTP (Network Time Protocol).

Before starting this tool, you must collect the stats_pool_records.csv files of all the processes into a folder.
These files must all have the suffix of ".csv". For FL clients, these files are located in their workspaces.
For FL server, you need to download the job first (using admin console or flare api) and then find it in the downloaded
workspace of the job.

Since these files have the same name in their workspaces, you must rename them when copying into the same folder.
You can simply use the client names for clients and "server" for server file.

Once you have all the csv files in the same folder, you can start this tool with the following args:

    -d: the directory that contains the csv files. Required.
    -o: the output file that will contain the result. Optional.

If the output file name is not specified, it will be default to "comm.txt".
The result is printed to the screen and written to the output file.

The output file will be placed into the same folder that contains the csv files.
Do not name your output file with the suffix ".csv"!

"""


def _print(data: str, out_file):
    pass


def _compute_time(file_name: str, pool_name: str, out_file):
    pass


def main():
    pass


if __name__ == "__main__":
    main()
