# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from functools import wraps, WRAPPER_ASSIGNMENTS

import tensorflow as tf


class TfTemplate(object):
    """This decorator wraps a method with `tf.make_template`. For example,

    Examples:
    ```python
    >>> @tf_template('socpe_name')
    ... my_method():
    ...     # Creates variables
    ```
    """

    def __init__(self, scope):
        self.scope = scope

    @staticmethod
    def available_attrs(fn):
        """
        Return the list of functools-wrappable attributes on a callable.
        This is required as a workaround for http://bugs.python.org/issue3445
        under Python 2.
        """
        if six.PY3:
            return WRAPPER_ASSIGNMENTS
        else:
            return tuple(a for a in WRAPPER_ASSIGNMENTS if hasattr(fn, a))

    def __call__(self, func):
        this = self
        templated_func = tf.make_template(this.scope, func)

        @wraps(func, assigned=TfTemplate.available_attrs(func))
        def inner(*args, **kwargs):
            return templated_func(*args, **kwargs)

        return inner


tf_template = TfTemplate
