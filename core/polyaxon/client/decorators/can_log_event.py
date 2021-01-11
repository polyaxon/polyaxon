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

from polyaxon.logger import logger


def can_log_events(f):
    """
    The `can_log_events` is a decorator to check if there's an event logger instance on the object.

    This decorator only works with run instances.

    usage example with class method:
        @can_log_events
        def my_func(self, *args, **kwargs):
            ...
            return ...

    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if args:
            self_arg = args[0]
            if (  # pylint:disable=protected-access
                not hasattr(self_arg, "_event_logger") or self_arg._event_logger is None
            ):
                logger.warning(
                    "You should set an event logger before calling: {}".format(repr(f))
                )
        return f(*args, **kwargs)

    return wrapper
