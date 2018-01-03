# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from distutils.util import strtobool


def to_bool(value):
    if isinstance(value, str):
        return strtobool(value)

    if value in (False, 0):
        return False

    if value in (True, 1):
        return True

    raise TypeError('The value `{}` cannot be interpreted as boolean'.format(value))
