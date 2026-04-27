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

from nvflare.security.logging import secure_format_exception


class State(object):
    def __init__(self, name: str):
        if not isinstance(name, str):
            raise TypeError(f"name must be str but got {type(name)}")
        name = name.strip()
        if len(name) <= 0:
            raise ValueError("name must not be empty")
        self.name = name
        self.fsm = None

    def execute(self, **kwargs):
        pass

    def leave(self):
        pass

    def enter(self):
        pass


class FSM(object):

    STATE_NAME_EXIT = "__exit__"

    def __init__(self, name: str):
        self.name = name
        self.props = {}
        self.states = {}  # state name => State
        self.current_state = None
        self.error = None

    def set_prop(self, name, value):
        pass

    def get_prop(self, name, default=None):
        pass

    def add_state(self, state: State):
        pass

    def set_current_state(self, name: str):
        pass

    def get_current_state(self):
        pass

    def execute(self, **kwargs) -> State:
        pass

    def _try_execute(self, **kwargs) -> State:
        pass
