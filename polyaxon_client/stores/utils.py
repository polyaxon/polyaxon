# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime
import os

from contextlib import contextmanager
from decimal import Decimal

from polyaxon_client.logger import logger
from polyaxon_client.stores.exceptions import PolyaxonStoresException


def get_from_env(keys):
    """
    Returns an environment variable from one of the list of keys.
    Args:
        keys: list(str). list of keys to check in the environment

    Returns:
        str | None
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


def is_protected_type(obj):
    """
    A check for preserving a type as-is when passed to force_text(strings_only=True).
    """
    return isinstance(obj, (
        type(None), int, float, Decimal, datetime.datetime, datetime.date, datetime.time,))


def force_bytes(value, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Resolve any value to strings.

    If `strings_only` is True, skip protected objects.
    """
    # Handle the common case first for performance reasons.
    if isinstance(value, bytes):
        if encoding == 'utf-8':
            return value
        return value.decode('utf-8', errors).encode(encoding, errors)
    if strings_only and is_protected_type(value):
        return value
    if isinstance(value, memoryview):
        return bytes(value)
    return value.encode(encoding, errors)


def append_basename(path, filename):
    """
    Adds the basename of the filename to the path.

    Args:
        path: `str`. The path to append the basename to.
        filename: `str`. The filename to extract the base name from.

    Returns:
         str
    """
    return os.path.join(path, os.path.basename(filename))


def check_dirname_exists(path, is_dir=False):
    if not is_dir:
        path = os.path.dirname(os.path.abspath(path))
    if not os.path.isdir(path):
        raise PolyaxonStoresException('The parent path is not a directory {}'.format(path))


@contextmanager
def get_files_in_current_directory(path):
    """
    Gets all the files under a certain path.

    Args:
        path: `str`. The path to traverse for collecting files.

    Returns:
         list of files collected under the path.
    """
    result_files = []

    for root, dirs, files in os.walk(path):
        logger.debug("Root:%s, Dirs:%s", root, dirs)

        for file_name in files:
            result_files.append(os.path.join(root, file_name))

    yield result_files
