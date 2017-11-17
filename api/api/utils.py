# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import six

from distutils.util import strtobool

from polyaxon_schemas.polyaxonfile import reader
from unipath import Path


def base_directory():
    return Path(__file__).ancestor(3)


ROOT_DIR = base_directory()
DATA_DIR = ROOT_DIR.child('data')
ENV_VARS_DIR = ROOT_DIR.child('api').child('api').child('env_vars')
TESTING = bool(strtobool(os.getenv("TESTING", "0")))


class SettingConfig(object):
    def __init__(self, **params):
        self._params = params

    @classmethod
    def read_configs(cls, config_values):
        config = reader.read(config_values)
        return cls(**config) if config else None

    def get_int(self, key, is_optional=False):
        """Get a the value corresponding to the key and converts it to `int`.

        Args:
            key: the dict key.
            is_optional: To raise  an error if key was not found.
        Return:
            `int`: value corresponding to the key.
        """
        return self._get_typed_value(key, int, lambda x: int(x), is_optional)

    def get_float(self, key, is_optional=False):
        """Get a the value corresponding to the key and converts it to `float`.

        Args:
            key: the dict key.
            is_optional: To raise  an error if key was not found.
        Return:
            `float`: value corresponding to the key.
        """
        return self._get_typed_value(key, float, lambda x: float(x), is_optional)

    def get_boolean(self, key, is_optional=False):
        """Get a the value corresponding to the key and converts it to `bool`.

        Args:
            key: the dict key.
            is_optional: To raise  an error if key was not found.
        Return:
            `bool`: value corresponding to the key.
        """
        return self._get_typed_value(key, bool, lambda x: bool(strtobool(x)), is_optional)

    def get_string(self, key, is_optional=False):
        """Get a the value corresponding to the key and converts it to `str`.

        Args:
            key: the dict key.
            is_optional: To raise  an error if key was not found.
        Return:
            `str`: value corresponding to the key.
        """
        return self._get_typed_value(key, str, lambda x: str(x), is_optional)

    def _get(self, key):
        """Gets key from the dictionary made out of the configs passed.

        Args:
            key: the dict key.
        Returns:
            The corresponding value of the key if found.
        Raises:
            KeyError
        """
        return self._params[key]

    def _get_typed_value(self, key, target_type, type_convert, is_optional=False):
        """Returns the value corresponding to the key converted to the given type.

        Args:
            key: the dict key.
            target_type: The type we expect the variable or key to be in.
            type_convert: A lambda expression that converts the key to the desired type.
            is_optional: To raise  an error if key was not found.

        Returns:
            The corresponding value of the key converted.
        """
        try:
            value = self._get(key)
        except KeyError:
            if not is_optional:
                raise
            return None

        if isinstance(value, six.string_types):
            try:
                return type_convert(value)
            except ValueError:
                raise ValueError("Cannot convert value `{}` (key: `{}`) "
                                 "to `{}`".format(value, key, target_type))

        if isinstance(value, target_type):
            return value
        raise TypeError(key, value, target_type)


config = SettingConfig.read_configs([
    '{}/defaults.json'.format(ENV_VARS_DIR),
    '{}/test.json'.format(ENV_VARS_DIR) if TESTING else '{}/local.json'.format(ENV_VARS_DIR),
    os.environ,
])
