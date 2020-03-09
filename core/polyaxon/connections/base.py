#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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


class BaseService:
    def __init__(self, connection=None, **kwargs):
        self._connection = connection
        self._connection_type = kwargs.get("connection_type")

    @property
    def connection_type(self):
        return self._connection_type

    @property
    def connection(self):
        if self._connection is None:
            # Create connection with defaults
            self.set_connection()
        return self._connection

    def set_connection(self, **kwargs):
        raise NotImplementedError
