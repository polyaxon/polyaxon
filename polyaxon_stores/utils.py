import datetime
import os
from contextlib import contextmanager

from decimal import Decimal

from polyaxon_stores.logger import logger


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

    :param path: The path to append the basename to.
    :type path: str
    :param filename: The filename to extract the base name from.
    :type filename: str
    :return: str
    """
    return os.path.join(path, os.path.basename(filename))


@contextmanager
def get_files_in_current_directory(path):
    """
    Gets all the files under a certain path.

    :param path: The path to traverse for collecting files.
    :type path: str
    :return: list of files collected under the path.
    """
    result_files = []

    for root, dirs, files in os.walk(path):
        logger.debug("Root:%s, Dirs:%s", root, dirs)

        for file_name in files:
            result_files.append(os.path.join(root, file_name))

    return result_files
