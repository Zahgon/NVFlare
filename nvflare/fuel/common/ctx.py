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

import threading


class SimpleContext(object):
    def __init__(self):
        """A simple context containing a props dictionary of key value pairs and convenience methods."""
        self.props = {}

    def set_prop(self, key, value):
        pass

    def set_props(self, props: dict):
        pass

    def len(self):
        pass

    def get_prop(self, key, default=None):
        pass

    def clear_props(self):
        pass


class BaseContext(SimpleContext):
    def __init__(self):
        """A SimpleContext with threading locks.

        This context class enables thread-safe set/get on top of SimpleContext."""
        SimpleContext.__init__(self)
        self._update_lock = threading.Lock()

    def set_prop(self, key, value):
        pass

    def set_props(self, props: dict):
        pass

    def len(self):
        pass

    def get_prop(self, key, default=None):
        pass

    def clear_props(self):
        pass
