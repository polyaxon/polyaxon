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
import functools

from polyaxon import settings


def check_no_op(f):
    """
    The `NoOpDecorator` is a decorator to ignore any decorated function when NO_OP env var is found.

    usage example with class method:
        @check_no_op
        def my_func(self, *args, **kwargs):
            ...
            return ...

    usage example with a function:
        @check_no_op
        def my_func(arg1, arg2):
            ...
            return ...
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if settings.CLIENT_CONFIG.no_op:
            return None
        return f(*args, **kwargs)

    return wrapper
