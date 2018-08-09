# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os


def get_from_env(keys):
    """
    Returns an environment variable from one of the list of keys.

    :param keys: list of keys to check in the environment
    :type keys: list(str)
    :return: str | None
    """
    keys = keys or []
    if not isinstance(keys, (list, tuple)):
        keys = [keys]
    for key in keys:
        value = os.environ.get(key)
        if value:
            return value
        # Prepend POLYAXON
        key = 'POLYAXON_{}'.format(key)
        value = os.environ.get(key)
        if value:
            return value

    return None
