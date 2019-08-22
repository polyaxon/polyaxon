# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client import settings


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

    def wrapper(*args, **kwargs):
        if settings.IS_OFFLINE:
            return None
        return f(*args, **kwargs)

    return wrapper
