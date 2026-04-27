# Copyright (c) 2025, NVIDIA CORPORATION.  All rights reserved.
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

_SECURE_SCHEME_MAPPING = {"tcp": "stcp", "grpc": "grpcs", "http": "https"}
_CLEAR_SCHEME_MAPPING = {"stcp": "tcp", "grpcs": "grpc", "https": "http"}


def make_url(scheme: str, address, secure: bool) -> str:
    """Make a full URL based on specified info

    Args:
        scheme: scheme of the url
        address: host address. Multiple formats are supported:
            str: this is a string that contains host name and optionally port number (e.g. localhost:1234)
            dict: contains item "host" and optionally "port"
            tuple or list: contains 1 or 2 items for host and port
        secure: whether secure connection is required

    Returns:

    """
    pass
