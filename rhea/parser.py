# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import re
import six

from collections import Mapping
from distutils.util import strtobool  # pylint:disable=import-error
from six.moves import urllib  # pylint:disable=ungrouped-imports

from rhea import types
from rhea.constants import NO_VALUE_FOUND
from rhea.exceptions import RheaError
from rhea.specs import AuthSpec, GCSSpec, S3Spec, UriSpec, WasbsSpec


def get_int(key,
            value,
            is_list=False,
            is_optional=False,
            default=None,
            options=None):
    """
    Get a the value corresponding to the key and converts it to `int`/`list(int)`.

    Args:
        key: the dict key.
        value: the value to parse.
        is_list: If this is one element or a list of elements.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
         `int`: value corresponding to the key.
    """
    if is_list:
        return _get_typed_list_value(key=key,
                                     value=value,
                                     target_type=int,
                                     type_convert=int,
                                     is_optional=is_optional,
                                     default=default,
                                     options=options)

    return _get_typed_value(key=key,
                            value=value,
                            target_type=int,
                            type_convert=int,
                            is_optional=is_optional,
                            default=default,
                            options=options)


def get_float(key,
              value,
              is_list=False,
              is_optional=False,
              default=None,
              options=None):
    """
    Get a the value corresponding to the key and converts it to `float`/`list(float)`.

    Args:
        key: the dict key.
        value: the value to parse.
        is_list: If this is one element or a list of elements.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
         `float`: value corresponding to the key.
    """
    if is_list:
        return _get_typed_list_value(key=key,
                                     value=value,
                                     target_type=float,
                                     type_convert=float,
                                     is_optional=is_optional,
                                     default=default,
                                     options=options)

    return _get_typed_value(key=key,
                            value=value,
                            target_type=float,
                            type_convert=float,
                            is_optional=is_optional,
                            default=default,
                            options=options)


def get_boolean(key,
                value,
                is_list=False,
                is_optional=False,
                default=None,
                options=None):
    """
    Get a the value corresponding to the key and converts it to `bool`/`list(str)`.

    Args:
        key: the dict key.
        value: the value to parse.
        is_list: If this is one element or a list of elements.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
        `bool`: value corresponding to the key.
    """
    if is_list:
        return _get_typed_list_value(key=key,
                                     value=value,
                                     target_type=bool,
                                     type_convert=lambda x: bool(strtobool(x)),
                                     is_optional=is_optional,
                                     default=default,
                                     options=options)

    return _get_typed_value(key=key,
                            value=value,
                            target_type=bool,
                            type_convert=lambda x: bool(strtobool(x)),
                            is_optional=is_optional,
                            default=default,
                            options=options)


def get_string(key,
               value,
               is_list=False,
               is_optional=False,
               default=None,
               options=None):
    """
    Get a the value corresponding to the key and converts it to `str`/`list(str)`.

    Args:
        key: the dict key.
        value: the value to parse.
        is_list: If this is one element or a list of elements.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
        `str`: value corresponding to the key.
    """
    if is_list:
        return _get_typed_list_value(key=key,
                                     value=value,
                                     target_type=str,
                                     type_convert=str,
                                     is_optional=is_optional,
                                     default=default,
                                     options=options)

    return _get_typed_value(key=key,
                            value=value,
                            target_type=str,
                            type_convert=str,
                            is_optional=is_optional,
                            default=default,
                            options=options)


def get_dict(key,
             value,
             is_list=False,
             is_optional=False,
             default=None,
             options=None):
    """
    Get a the value corresponding to the key and converts it to `dict`.

    Args:
        key: the dict key.
        value: the value to parse.
        is_list: If this is one element or a list of elements.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
        `dict`: value corresponding to the key.
    """

    def convert_to_dict(x):
        x = json.loads(x)
        if not isinstance(x, Mapping):
            raise RheaError("Cannot convert value `{}` (key: `{}`) to `dict`".format(x, key))
        return x

    if is_list:
        return _get_typed_list_value(key=key,
                                     value=value,
                                     target_type=Mapping,
                                     type_convert=convert_to_dict,
                                     is_optional=is_optional,
                                     default=default,
                                     options=options)
    value = _get_typed_value(key=key,
                             value=value,
                             target_type=Mapping,
                             type_convert=convert_to_dict,
                             is_optional=is_optional,
                             default=default,
                             options=options)

    if not value:
        return default

    if not isinstance(value, Mapping):
        raise RheaError("Cannot convert value `{}` (key: `{}`) "
                        "to `dict`".format(value, key))
    return value


def get_dict_of_dicts(key,
                      value,
                      is_list=None,  # noqa
                      is_optional=False,
                      default=None,
                      options=None):
    """
    Get a the value corresponding to the key and converts it to `dict`.

    Add an extra validation that all keys have a dict as values.

    Args:
        key: the dict key.
        value: the value to parse.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
        `dict or dict`: value corresponding to the key.
    """
    value = get_dict(
        key=key,
        value=value,
        is_optional=is_optional,
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


def get_uri(key,
            value,
            is_list=False,
            is_optional=False,
            default=None,
            options=None):
    """
    Get a the value corresponding to the key and converts it to `UriSpec`.

    Args
        key: the dict key.
        value: the value to parse.
        is_list: If this is one element or a list of elements.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
         `UriSpec`: value corresponding to the key.
    """
    if is_list:
        return _get_typed_list_value(key=key,
                                     value=value,
                                     target_type=UriSpec,
                                     type_convert=parse_uri_spec,
                                     is_optional=is_optional,
                                     default=default,
                                     options=options)

    return _get_typed_value(key=key,
                            value=value,
                            target_type=UriSpec,
                            type_convert=parse_uri_spec,
                            is_optional=is_optional,
                            default=default,
                            options=options)


def get_auth(key,
             value,
             is_list=False,
             is_optional=False,
             default=None,
             options=None):
    """
    Get a the value corresponding to the key and converts it to `AuthSpec`.

    Args
        key: the dict key.
        value: the value to parse.
        is_list: If this is one element or a list of elements.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
         `AuthSpec`: value corresponding to the key.
    """
    if is_list:
        return _get_typed_list_value(key=key,
                                     value=value,
                                     target_type=AuthSpec,
                                     type_convert=parse_auth_spec,
                                     is_optional=is_optional,
                                     default=default,
                                     options=options)

    return _get_typed_value(key=key,
                            value=value,
                            target_type=AuthSpec,
                            type_convert=parse_auth_spec,
                            is_optional=is_optional,
                            default=default,
                            options=options)


def get_list(key,
             value,
             is_list=None,  # noqa
             is_optional=False,
             default=None,
             options=None):
    """
    Get a the value corresponding to the key and converts comma separated values to a list.

    Args:
        key: the dict key.
        value: the value to parse.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
         `list`: value corresponding to the key.
    """

    def parse_list(v):
        parts = v.split(',')
        results = []
        for part in parts:
            part = part.strip()
            if part:
                results.append(part)
        return results

    return _get_typed_value(key=key,
                            value=value,
                            target_type=list,
                            type_convert=parse_list,
                            is_optional=is_optional,
                            default=default,
                            options=options)


def get_wasbs_path(key,
                   value,
                   is_list=False,
                   is_optional=False,
                   default=None,
                   options=None):
    """
    Get a the value corresponding to the key and converts it to `WasbsSpec`.

    Args
        key: the dict key.
        value: the value to parse.
        is_list: If this is one element or a list of elements.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
         `WasbsSpec`: value corresponding to the key.
    """
    if is_list:
        return _get_typed_list_value(key=key,
                                     value=value,
                                     target_type=WasbsSpec,
                                     type_convert=parse_wasbs_path,
                                     is_optional=is_optional,
                                     default=default,
                                     options=options)

    return _get_typed_value(key=key,
                            value=value,
                            target_type=WasbsSpec,
                            type_convert=parse_wasbs_path,
                            is_optional=is_optional,
                            default=default,
                            options=options)


def get_gcs_path(key,
                 value,
                 is_list=False,
                 is_optional=False,
                 default=None,
                 options=None):
    """
    Get a the value corresponding to the key and converts it to `GCSSpec`.

    Args
        key: the dict key.
        value: the value to parse.
        is_list: If this is one element or a list of elements.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
         `GCSSpec`: value corresponding to the key.
    """
    if is_list:
        return _get_typed_list_value(key=key,
                                     value=value,
                                     target_type=GCSSpec,
                                     type_convert=parse_gcs_path,
                                     is_optional=is_optional,
                                     default=default,
                                     options=options)

    return _get_typed_value(key=key,
                            value=value,
                            target_type=GCSSpec,
                            type_convert=parse_gcs_path,
                            is_optional=is_optional,
                            default=default,
                            options=options)


def get_s3_path(key,
                value,
                is_list=False,
                is_optional=False,
                default=None,
                options=None):
    """
    Get a the value corresponding to the key and converts it to `S3Spec`.

    Args
        key: the dict key.
        value: the value to parse.
        is_list: If this is one element or a list of elements.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
         `S3Spec`: value corresponding to the key.
    """
    if is_list:
        return _get_typed_list_value(key=key,
                                     value=value,
                                     target_type=S3Spec,
                                     type_convert=parse_s3_path,
                                     is_optional=is_optional,
                                     default=default,
                                     options=options)

    return _get_typed_value(key=key,
                            value=value,
                            target_type=S3Spec,
                            type_convert=parse_s3_path,
                            is_optional=is_optional,
                            default=default,
                            options=options)


def _check_options(key, value, options):
    if options and value not in options:
        raise RheaError(
            'The value `{}` provided for key `{}` '
            'is not one of the possible values.'.format(value, key))


def _get_typed_value(key,
                     value,
                     target_type,
                     type_convert,
                     is_optional=False,
                     default=None,
                     options=None):
    """
    Return the value corresponding to the key converted to the given type.

    Args:
        key: the dict key.
        target_type: The type we expect the variable or key to be in.
        type_convert: A lambda expression that converts the key to the desired type.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
        The corresponding value of the key converted.
    """
    if value is None or value == NO_VALUE_FOUND:
        if not is_optional:
            raise RheaError(
                'No value was provided for the non optional key `{}`.'.format(key))
        return default

    if isinstance(value, six.string_types):
        try:
            # _add_key(key, is_secret=is_secret, is_local=is_local)
            _check_options(key=key, value=value, options=options)
            return type_convert(value)
        except ValueError:
            raise RheaError("Cannot convert value `{}` (key: `{}`) "
                            "to `{}`".format(value, key, target_type))

    if isinstance(value, target_type):
        # _add_key(key, is_secret=is_secret, is_local=is_local)
        _check_options(key=key, value=value, options=options)
        return value
    raise RheaError("Cannot convert value `{}` (key: `{}`) "
                    "to `{}`".format(value, key, target_type))


def _get_typed_list_value(key,
                          value,
                          target_type,
                          type_convert,
                          is_optional=False,
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
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.
    """

    value = _get_typed_value(key=key,
                             value=value,
                             target_type=list,
                             type_convert=json.loads,
                             is_optional=is_optional,
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


def parse_uri_spec(uri_spec):
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


def parse_auth_spec(auth_spec):
    user_pass = auth_spec.split(':')
    if len(user_pass) != 2:
        raise RheaError(
            'Received invalid uri_spec `{}`. `user:host` is not conform.'
            'The uri must be in the format `user:pass`'.format(auth_spec))

    return AuthSpec(user=user_pass[0], password=user_pass[1])


def parse_wasbs_path(wasbs_path):
    parsed_url = urllib.parse.urlparse(wasbs_path)
    if parsed_url.scheme != "wasbs":
        raise RheaError('Received an invalid url `{}`'.format(wasbs_path))
    match = re.match("([^@]+)@([^.]+)\\.blob\\.core\\.windows\\.net", parsed_url.netloc)
    if match is None:
        raise RheaError(
            'wasbs url must be of the form <container>@<account>.blob.core.windows.net')

    container = match.group(1)
    storage_account = match.group(2)
    path = parsed_url.path
    if path.startswith('/'):
        path = path[1:]
    return WasbsSpec(container, storage_account, path)


def parse_gcs_path(gcs_path):
    """
    Parses and validates a google cloud storage url.

    Returns:
        tuple(bucket_name, blob).
    """
    parsed_url = urllib.parse.urlparse(gcs_path)
    if not parsed_url.netloc:
        raise RheaError('Received an invalid GCS url `{}`'.format(gcs_path))
    if parsed_url.scheme != 'gs':
        raise RheaError('Received an invalid url GCS `{}`'.format(gcs_path))
    blob = parsed_url.path.lstrip('/')
    return GCSSpec(parsed_url.netloc, blob)


def parse_s3_path(s3_path):
    """
    Parses and validates an S3 url.

    Returns:
         tuple(bucket_name, key).
    """
    parsed_url = urllib.parse.urlparse(s3_path)
    if not parsed_url.netloc:
        raise RheaError('Received an invalid S3 url `{}`'.format(s3_path))
    else:
        bucket_name = parsed_url.netloc
        key = parsed_url.path.strip('/')
        return S3Spec(bucket_name, key)


TYPE_MAPPING = {
    types.INT: get_int,
    types.FLOAT: get_float,
    types.BOOL: get_boolean,
    types.STR: get_string,
    types.DICT: get_dict,
    types.DICT_OF_DICTS: get_dict_of_dicts,
    types.URI: get_uri,
    types.AUTH: get_auth,
    types.LIST: get_list,
    types.GCS_PATH: get_gcs_path,
    types.S3_PATH: get_s3_path,
    types.AZURE_PATH: get_wasbs_path,
    types.PATH: get_string,
    types.METRIC: get_float,
    types.METADATA: get_dict
}
