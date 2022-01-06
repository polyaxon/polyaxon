#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class ManagerInterface:
    def __init__(self):
        self._state = {}

    @property
    def state(self):
        return self._state

    def _get_state_data(self, obj):
        raise NotImplementedError

    def subscribe(self, obj):
        key, value = self._get_state_data(obj)
        self._subscribe(key=key, value=value)

    def _subscribe(self, key, value):
        if key in self.state:
            assert self.state[key] == value
        else:
            self.state[key] = value

    def knows(self, key):
        return key in self.state

    def get(self, key):
        return self.state.get(key)

    @property
    def keys(self):
        return self.state.keys()

    @property
    def values(self):
        return self.state.values()

    @property
    def items(self):
        return self.state.items()
