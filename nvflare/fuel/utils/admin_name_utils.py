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
import uuid

_NAME_PREFIX = "_admin_"
_NAME_PREFIX_LEN = len(_NAME_PREFIX)


def new_admin_client_name():
    """Create a unique name for a new admin client session.
    Note that we cannot use the admin user's login name because the same user could have multiple
    admin sessions at the same time. The admin client name is also the FQCN of the client when connecting
    to the server.

    The admin client name is created with this pattern:
        <prefix><uid>

    where the prefix is fixed, whereas uid is a unique ID.

    Returns: a unique name

    """
    pass


def _is_valid_uid(data: str) -> bool:
    """Check whether the specified data is a valid uid

    Args:
        data: the data to be checked

    Returns: whether the data is a valid uid.

    """
    pass


def is_valid_admin_client_name(name: str) -> bool:
    """Check whether the specified name is a valid admin client name.

    Args:
        name: the name to be checked.

    Returns: whether the name is valid admin client name

    """
    pass
