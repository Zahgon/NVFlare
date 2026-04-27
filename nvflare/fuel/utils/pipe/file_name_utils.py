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

from nvflare.fuel.utils.pipe.pipe import Message


def message_to_file_name(msg: Message) -> str:
    """Produce the file name that encodes the meta info of the message

    Args:
        msg: message for which the file name is to be produced

    Returns:

    """
    pass


def file_name_to_message(file_name: str) -> Message:
    """Decode the file name to produce the meta info of the message.

    Args:
        file_name: the file name to be decoded.

    Returns: a Message object that contains meta info.

    """
    pass
