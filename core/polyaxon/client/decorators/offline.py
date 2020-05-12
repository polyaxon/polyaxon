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
import functools

from polyaxon import settings


def check_offline(f):
    """
    The `check_offline` is a decorator to ignore any decorated function when
    POLYAXON_IS_OFFLINE env var is found.

    usage example with class method:
        @check_offline
        def my_func(self, *args, **kwargs):
            ...
            return ...

    usage example with a function:
        @check_offline
        def my_func(arg1, arg2):
            ...
            return ...
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if settings.CLIENT_CONFIG.is_offline:
            return None
        return f(*args, **kwargs)

    return wrapper
