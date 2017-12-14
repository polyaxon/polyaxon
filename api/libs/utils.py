# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function


def to_bool(value):
    if value in ('false', 'False', 'no', False, 0, '0'):
        return False
    if value in ('true', 'True', 'yes', True, 1, '1'):
        return True
    raise TypeError('The value `{}` cannot be interpreted as boolean'.format(value))
