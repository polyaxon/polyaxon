# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os


def get_from_env(keys):
    for key in keys:
        value = os.environ.get(key)
        if value:
            return value
        # Prepend POLYAXON
        key = 'POLYAXON_{}'.format(key)
        value = os.environ.get(key)
        if value:
            return value
