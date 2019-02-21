# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_client import settings


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

    def wrapper(*args, **kwargs):
        if settings.NO_OP:
            return None
        return f(*args, **kwargs)

    return wrapper
