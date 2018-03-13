# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from distutils.util import strtobool

from django.utils.crypto import salted_hmac

from polyaxon_schemas.utils import to_list


def to_bool(value):
    if isinstance(value, str):
        value = strtobool(value)

    if value in (False, 0):
        return False

    if value in (True, 1):
        return True

    raise TypeError('The value `{}` cannot be interpreted as boolean'.format(value))


def get_hmac(key_salt, value):
    return salted_hmac(key_salt, value).hexdigest()


def get_list(values):
    return to_list(values) if values is not None else []
