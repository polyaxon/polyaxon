#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from polyaxon.config_reader.spec import ConfigSpec
from polyaxon.parser import parser
from polyaxon.parser.constants import NO_VALUE_FOUND
from polyaxon.schemas.types import V1AuthType, V1UriType


class ConfigManager:
    def __init__(self, **data):
        self._data = data
        self._requested_keys = set()
        self._secret_keys = set()
        self._local_keys = set()

    @classmethod
    def read_configs(cls, config_values):  # pylint:disable=redefined-outer-name
        config = ConfigSpec.read_from(
            config_values
        )  # pylint:disable=redefined-outer-name
        return cls(**config) if config else None

    def keys_startswith(self, term):
        return [k for k in self._data if k.startswith(term)]

    def keys_endswith(self, term):
        return [k for k in self._data if k.endswith(term)]

    def has_key(self, key):
        return key in self._data

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

    def get_requested_data(
        self, include_secrets=False, include_locals=False, to_str=False
    ):
        data = {}
        for key in self._requested_keys:
            if not include_secrets and key in self._secret_keys:
                continue
            if not include_locals and key in self._local_keys:
                continue
            value = self._data[key]
            data[key] = "{}".format(value) if to_str else value
        return data

    def get_int(
        self,
        key,
        is_list=False,
        is_optional=False,
        is_secret=False,
        is_local=False,
        default=None,
        options=None,
    ):
        """
        Get the value corresponding to the key and converts it to `int`/`list(int)`.

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
        return self._get(
            key=key,
            parser_fct=parser.get_int,
            is_list=is_list,
            is_optional=is_optional,
            is_secret=is_secret,
            is_local=is_local,
            default=default,
            options=options,
        )

    def get_float(
        self,
        key,
        is_list=False,
        is_optional=False,
        is_secret=False,
        is_local=False,
        default=None,
        options=None,
    ):
        """
        Get the value corresponding to the key and converts it to `float`/`list(float)`.

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
        return self._get(
            key=key,
            parser_fct=parser.get_float,
            is_list=is_list,
            is_optional=is_optional,
            is_secret=is_secret,
            is_local=is_local,
            default=default,
            options=options,
        )

    def get_boolean(
        self,
        key,
        is_list=False,
        is_optional=False,
        is_secret=False,
        is_local=False,
        default=None,
        options=None,
    ):
        """
        Get the value corresponding to the key and converts it to `bool`/`list(str)`.

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
        return self._get(
            key=key,
            parser_fct=parser.get_boolean,
            is_list=is_list,
            is_optional=is_optional,
            is_secret=is_secret,
            is_local=is_local,
            default=default,
            options=options,
        )

    def get_string(
        self,
        key,
        is_list=False,
        is_optional=False,
        is_secret=False,
        is_local=False,
        default=None,
        options=None,
    ):
        """
        Get the value corresponding to the key and converts it to `str`/`list(str)`.

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
        return self._get(
            key=key,
            parser_fct=parser.get_string,
            is_list=is_list,
            is_optional=is_optional,
            is_secret=is_secret,
            is_local=is_local,
            default=default,
            options=options,
        )

    def get_dict(
        self,
        key,
        is_list=False,
        is_optional=False,
        is_secret=False,
        is_local=False,
        default=None,
        options=None,
    ):
        """
        Get the value corresponding to the key and converts it to `dict`.

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

        return self._get(
            key=key,
            parser_fct=parser.get_dict,
            is_list=is_list,
            is_optional=is_optional,
            is_secret=is_secret,
            is_local=is_local,
            default=default,
            options=options,
        )

    def get_dict_of_dicts(
        self,
        key,
        is_optional=False,
        is_secret=False,
        is_local=False,
        default=None,
        options=None,
    ):
        """
        Get the value corresponding to the key and converts it to `dict`.

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
        return self._get(
            key=key,
            parser_fct=parser.get_dict_of_dicts,
            is_list=None,
            is_optional=is_optional,
            is_secret=is_secret,
            is_local=is_local,
            default=default,
            options=options,
        )

    def get_uri(
        self,
        key,
        is_list=False,
        is_optional=False,
        is_secret=False,
        is_local=False,
        default=None,
        options=None,
    ) -> V1UriType:
        """
        Get the value corresponding to the key and converts it to `V1UriType`.

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
        return self._get(
            key=key,
            parser_fct=parser.get_uri,
            is_list=is_list,
            is_optional=is_optional,
            is_secret=is_secret,
            is_local=is_local,
            default=default,
            options=options,
        )

    def get_auth(
        self,
        key,
        is_list=False,
        is_optional=False,
        is_secret=False,
        is_local=False,
        default=None,
        options=None,
    ) -> V1AuthType:
        """
        Get the value corresponding to the key and converts it to `V1AuthType`.

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
        return self._get(
            key=key,
            parser_fct=parser.get_auth,
            is_list=is_list,
            is_optional=is_optional,
            is_secret=is_secret,
            is_local=is_local,
            default=default,
            options=options,
        )

    def get_list(
        self,
        key,
        is_optional=False,
        is_secret=False,
        is_local=False,
        default=None,
        options=None,
    ):
        """
        Get the value corresponding to the key and converts comma separated values to a list.

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

        return self._get(
            key=key,
            parser_fct=parser.get_list,
            is_list=None,
            is_optional=is_optional,
            is_secret=is_secret,
            is_local=is_local,
            default=default,
            options=options,
        )

    def _get(
        self,
        key,
        parser_fct,
        is_list,
        is_optional,
        is_secret,
        is_local,
        default,
        options,
    ):
        """
        Get key from the dictionary made out of the configs passed.

        Args:
            key: the dict key.

        Returns:
             The corresponding value of the key if found.

        Raises:
            KeyError
        """
        value = self._data.get(key, NO_VALUE_FOUND)
        parsed_value = parser_fct(
            key=key,
            value=value,
            is_list=is_list,
            is_optional=is_optional,
            default=default,
            options=options,
        )
        self._add_key(key, is_secret=is_secret, is_local=is_local)
        return parsed_value

    def _add_key(self, key, is_secret=False, is_local=False):
        self._requested_keys.add(key)
        if is_secret:
            self._secret_keys.add(key)
        if is_local:
            self._local_keys.add(key)
