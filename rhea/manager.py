# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import six

from collections import Mapping
from distutils.util import strtobool  # pylint:disable=import-error

from rhea import reader
from rhea.exceptions import RheaError
from rhea.specs import UriSpec


class Rhea(object):
    def __init__(self, **data):
        self._data = data
        self._requested_keys = set()
        self._secret_keys = set()
        self._local_keys = set()

    @classmethod
    def read_configs(cls, config_values):  # pylint:disable=redefined-outer-name
        config = reader.read(config_values)  # pylint:disable=redefined-outer-name
        return cls(**config) if config else None

    def keys_startswith(self, term):
        return [k for k in self._data if k.startswith(term)]

    def keys_endswith(self, term):
        return [k for k in self._data if k.endswith(term)]

    @property
    def data(self):
        return self._data

    @property
    def requested_keys(self):
        return self._requested_keys

    @property
    def secret_keys(self):
        return self._secret_keys

    @property
    def local_keys(self):
        return self._local_keys

    def get_requested_data(self, include_secrets=False, include_locals=False, to_str=False):
        data = {}
        for key in self._requested_keys:
            if not include_secrets and key in self._secret_keys:
                continue
            if not include_locals and key in self._local_keys:
                continue
            value = self._data[key]
            data[key] = '{}'.format(value) if to_str else value
        return data

    def get_int(self,
                key,
                is_list=False,
                is_optional=False,
                is_secret=False,
                is_local=False,
                default=None,
                options=None):
        """
        Get a the value corresponding to the key and converts it to `int`/`list(int)`.

        Args:
            key: the dict key.
            is_list: If this is one element or a list of elements.
            is_optional: To raise an error if key was not found.
            is_secret: If the key is a secret.
            is_local: If the key is a local to this service.
            default: default value if is_optional is True.
            options: list/tuple if provided, the value must be one of these values.

        Returns:
             `int`: value corresponding to the key.
        """
        if is_list:
            return self._get_typed_list_value(key=key,
                                              target_type=int,
                                              type_convert=int,
                                              is_optional=is_optional,
                                              is_secret=is_secret,
                                              is_local=is_local,
                                              default=default,
                                              options=options)

        return self._get_typed_value(key=key,
                                     target_type=int,
                                     type_convert=int,
                                     is_optional=is_optional,
                                     is_secret=is_secret,
                                     is_local=is_local,
                                     default=default,
                                     options=options)

    def get_float(self,
                  key,
                  is_list=False,
                  is_optional=False,
                  is_secret=False,
                  is_local=False,
                  default=None,
                  options=None):
        """
        Get a the value corresponding to the key and converts it to `float`/`list(float)`.

        Args:
            key: the dict key.
            is_list: If this is one element or a list of elements.
            is_optional: To raise an error if key was not found.
            is_secret: If the key is a secret.
            is_local: If the key is a local to this service.
            default: default value if is_optional is True.
            options: list/tuple if provided, the value must be one of these values.

        Returns:
             `float`: value corresponding to the key.
        """
        if is_list:
            return self._get_typed_list_value(key=key,
                                              target_type=float,
                                              type_convert=float,
                                              is_optional=is_optional,
                                              is_secret=is_secret,
                                              is_local=is_local,
                                              default=default,
                                              options=options)

        return self._get_typed_value(key=key,
                                     target_type=float,
                                     type_convert=float,
                                     is_optional=is_optional,
                                     is_secret=is_secret,
                                     is_local=is_local,
                                     default=default,
                                     options=options)

    def get_boolean(self,
                    key,
                    is_list=False,
                    is_optional=False,
                    is_secret=False,
                    is_local=False,
                    default=None,
                    options=None):
        """
        Get a the value corresponding to the key and converts it to `bool`/`list(str)`.

        Args:
            key: the dict key.
            is_list: If this is one element or a list of elements.
            is_optional: To raise an error if key was not found.
            is_secret: If the key is a secret.
            is_local: If the key is a local to this service.
            default: default value if is_optional is True.
            options: list/tuple if provided, the value must be one of these values.

        Returns:
            `bool`: value corresponding to the key.
        """
        if is_list:
            return self._get_typed_list_value(key=key,
                                              target_type=bool,
                                              type_convert=lambda x: bool(strtobool(x)),
                                              is_optional=is_optional,
                                              is_secret=is_secret,
                                              is_local=is_local,
                                              default=default,
                                              options=options)

        return self._get_typed_value(key=key,
                                     target_type=bool,
                                     type_convert=lambda x: bool(strtobool(x)),
                                     is_optional=is_optional,
                                     is_secret=is_secret,
                                     is_local=is_local,
                                     default=default,
                                     options=options)

    def get_string(self,
                   key,
                   is_list=False,
                   is_optional=False,
                   is_secret=False,
                   is_local=False,
                   default=None,
                   options=None):
        """
        Get a the value corresponding to the key and converts it to `str`/`list(str)`.

        Args:
            key: the dict key.
            is_list: If this is one element or a list of elements.
            is_optional: To raise an error if key was not found.
            is_secret: If the key is a secret.
            is_local: If the key is a local to this service.
            default: default value if is_optional is True.
            options: list/tuple if provided, the value must be one of these values.

        Returns:
            `str`: value corresponding to the key.
        """
        if is_list:
            return self._get_typed_list_value(key=key,
                                              target_type=str,
                                              type_convert=str,
                                              is_optional=is_optional,
                                              is_secret=is_secret,
                                              is_local=is_local,
                                              default=default,
                                              options=options)

        return self._get_typed_value(key=key,
                                     target_type=str,
                                     type_convert=str,
                                     is_optional=is_optional,
                                     is_secret=is_secret,
                                     is_local=is_local,
                                     default=default,
                                     options=options)

    def get_dict(self,
                 key,
                 is_list=False,
                 is_optional=False,
                 is_secret=False,
                 is_local=False,
                 default=None,
                 options=None):
        """
        Get a the value corresponding to the key and converts it to `dict`.

        Args:
            key: the dict key.
            is_list: If this is one element or a list of elements.
            is_optional: To raise an error if key was not found.
            is_secret: If the key is a secret.
            is_local: If the key is a local to this service.
            default: default value if is_optional is True.
            options: list/tuple if provided, the value must be one of these values.

        Returns:
            `str`: value corresponding to the key.
        """

        def convert_to_dict(x):
            x = json.loads(x)
            if not isinstance(x, Mapping):
                raise RheaError("Cannot convert value `{}` (key: `{}`) to `dict`".format(x, key))
            return x

        if is_list:
            return self._get_typed_list_value(key=key,
                                              target_type=Mapping,
                                              type_convert=convert_to_dict,
                                              is_optional=is_optional,
                                              is_secret=is_secret,
                                              is_local=is_local,
                                              default=default,
                                              options=options)
        value = self._get_typed_value(key=key,
                                      target_type=Mapping,
                                      type_convert=convert_to_dict,
                                      is_optional=is_optional,
                                      is_secret=is_secret,
                                      is_local=is_local,
                                      default=default,
                                      options=options)

        if not value:
            return default

        if not isinstance(value, Mapping):
            raise RheaError("Cannot convert value `{}` (key: `{}`) "
                            "to `dict`".format(value, key))
        return value

    def get_dict_of_dicts(self,
                          key,
                          is_optional=False,
                          is_secret=False,
                          is_local=False,
                          default=None,
                          options=None):
        """
        Get a the value corresponding to the key and converts it to `dict`.

        Add an extra validation that all keys have a dict as values.

        Args:
            key: the dict key.
            is_optional: To raise an error if key was not found.
            is_secret: If the key is a secret.
            is_local: If the key is a local to this service.
            default: default value if is_optional is True.
            options: list/tuple if provided, the value must be one of these values.

        Returns:
            `str`: value corresponding to the key.
        """
        value = self.get_dict(
            key=key,
            is_optional=is_optional,
            is_secret=is_secret,
            is_local=is_local,
            default=default,
            options=options,
        )
        if not value:
            return default

        for k in value:
            if not isinstance(value[k], Mapping):
                raise RheaError(
                    "`{}` must be an object. "
                    "Received a non valid configuration for key `{}`.".format(value[k], key))

        return value

    def get_uri(self,
                key,
                is_list=False,
                is_optional=False,
                is_secret=False,
                is_local=False,
                default=None,
                options=None):
        """
        Get a the value corresponding to the key and converts it to `UriSpec`.

        Args
            key: the dict key.
            is_list: If this is one element or a list of elements.
            is_optional: To raise an error if key was not found.
            is_secret: If the key is a secret.
            is_local: If the key is a local to this service.
            default: default value if is_optional is True.
            options: list/tuple if provided, the value must be one of these values.

        Returns:
             `str`: value corresponding to the key.
        """
        if is_list:
            return self._get_typed_list_value(key=key,
                                              target_type=UriSpec,
                                              type_convert=self.parse_uri_spec,
                                              is_optional=is_optional,
                                              is_secret=is_secret,
                                              is_local=is_local,
                                              default=default,
                                              options=options)

        return self._get_typed_value(key=key,
                                     target_type=UriSpec,
                                     type_convert=self.parse_uri_spec,
                                     is_optional=is_optional,
                                     is_secret=is_secret,
                                     is_local=is_local,
                                     default=default,
                                     options=options)

    def get_list(self,
                 key,
                 is_optional=False,
                 is_secret=False,
                 is_local=False,
                 default=None,
                 options=None):
        """
        Get a the value corresponding to the key and converts comma separated values to a list.

        Args:
            key: the dict key.
            is_optional: To raise an error if key was not found.
            is_secret: If the key is a secret.
            is_local: If the key is a local to this service.
            default: default value if is_optional is True.
            options: list/tuple if provided, the value must be one of these values.

        Returns:
             `str`: value corresponding to the key.
        """

        def parse_list(v):
            parts = v.split(',')
            results = []
            for part in parts:
                part = part.strip()
                if part:
                    results.append(part)
            return results

        return self._get_typed_value(key=key,
                                     target_type=list,
                                     type_convert=parse_list,
                                     is_optional=is_optional,
                                     is_secret=is_secret,
                                     is_local=is_local,
                                     default=default,
                                     options=options)

    def _get(self, key):
        """
        Get key from the dictionary made out of the configs passed.

        Args:
            key: the dict key.

        Returns:
             The corresponding value of the key if found.

        Raises:
            KeyError
        """
        return self._data[key]

    def _add_key(self, key, is_secret=False, is_local=False):
        self._requested_keys.add(key)
        if is_secret:
            self._secret_keys.add(key)
        if is_local:
            self._local_keys.add(key)

    @staticmethod
    def _check_options(key, value, options):
        if options and value not in options:
            raise RheaError(
                'The value `{}` provided for key `{}` '
                'is not one of the possible values.'.format(value, key))

    def _get_typed_value(self,
                         key,
                         target_type,
                         type_convert,
                         is_optional=False,
                         is_secret=False,
                         is_local=False,
                         default=None,
                         options=None):
        """
        Return the value corresponding to the key converted to the given type.

        Args:
            key: the dict key.
            target_type: The type we expect the variable or key to be in.
            type_convert: A lambda expression that converts the key to the desired type.
            is_optional: To raise an error if key was not found.
            is_secret: If the key is a secret.
            is_local: If the key is a local to this service.
            default: default value if is_optional is True.
            options: list/tuple if provided, the value must be one of these values.

        Returns:
            The corresponding value of the key converted.
        """
        try:
            value = self._get(key)
        except KeyError:
            if not is_optional:
                raise RheaError(
                    'No value was provided for the non optional key `{}`.'.format(key))
            return default

        if isinstance(value, six.string_types):
            try:
                self._add_key(key, is_secret=is_secret, is_local=is_local)
                self._check_options(key=key, value=value, options=options)
                return type_convert(value)
            except ValueError:
                raise RheaError("Cannot convert value `{}` (key: `{}`) "
                                "to `{}`".format(value, key, target_type))

        if isinstance(value, target_type):
            self._add_key(key, is_secret=is_secret, is_local=is_local)
            self._check_options(key=key, value=value, options=options)
            return value
        raise RheaError("Cannot convert value `{}` (key: `{}`) "
                        "to `{}`".format(value, key, target_type))

    def _get_typed_list_value(self,
                              key,
                              target_type,
                              type_convert,
                              is_optional=False,
                              is_secret=False,
                              is_local=False,
                              default=None,
                              options=None):
        """
        Return the value corresponding to the key converted first to list
        than each element to the given type.

        Args:
            key: the dict key.
            target_type: The type we expect the variable or key to be in.
            type_convert: A lambda expression that converts the key to the desired type.
            is_optional: To raise an error if key was not found.
            is_secret: If the key is a secret.
            is_local: If the key is a local to this service.
            default: default value if is_optional is True.
            options: list/tuple if provided, the value must be one of these values.
        """

        value = self._get_typed_value(key=key,
                                      target_type=list,
                                      type_convert=json.loads,
                                      is_optional=is_optional,
                                      is_secret=is_secret,
                                      is_local=is_local,
                                      default=default,
                                      options=options)

        if not value:
            return default

        raise_type = 'dict' if target_type == Mapping else target_type

        if not isinstance(value, list):
            raise RheaError("Cannot convert value `{}` (key: `{}`) "
                            "to `{}`".format(value, key, raise_type))
        # If we are here the value must be a list
        result = []
        for v in value:
            if isinstance(v, six.string_types):
                try:
                    result.append(type_convert(v))
                except ValueError:
                    raise RheaError("Cannot convert value `{}` (found in list key: `{}`) "
                                    "to `{}`".format(v, key, raise_type))
            elif isinstance(v, target_type):
                result.append(v)

            else:
                raise RheaError("Cannot convert value `{}` (found in list key: `{}`) "
                                "to `{}`".format(v, key, raise_type))
        return result

    def parse_uri_spec(self, uri_spec):
        parts = uri_spec.split('@')
        if len(parts) != 2:
            raise RheaError(
                'Received invalid uri_spec `{}`. '
                'The uri must be in the format `user:pass@host`'.format(uri_spec))

        user_pass, host = parts
        user_pass = user_pass.split(':')
        if len(user_pass) != 2:
            raise RheaError(
                'Received invalid uri_spec `{}`. `user:host` is not conform.'
                'The uri must be in the format `user:pass@host`'.format(uri_spec))

        return UriSpec(user=user_pass[0], password=user_pass[1], host=host)
