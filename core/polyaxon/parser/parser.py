#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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

import json
import re

from collections.abc import Mapping
from datetime import date, datetime
from distutils.util import strtobool  # pylint:disable=import-error
from json import JSONDecodeError
from typing import Dict, Union
from urllib.parse import urlparse

from marshmallow import ValidationError, fields

from polyaxon import types
from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.logger import logger
from polyaxon.parser.constants import NO_VALUE_FOUND
from polyaxon.schemas.types import (
    V1ArtifactsType,
    V1AuthType,
    V1DockerfileType,
    V1GcsType,
    V1GitType,
    V1S3Type,
    V1UriType,
    V1WasbType,
)
from polyaxon.schemas.types.event import V1EventType


def get_int(key, value, is_list=False, is_optional=False, default=None, options=None):
    """
    Get the value corresponding to the key and converts it to `int`/`list(int)`.

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
        return _get_typed_list_value(
            key=key,
            value=value,
            target_type=int,
            type_convert=int,
            is_optional=is_optional,
            default=default,
            options=options,
        )

    return _get_typed_value(
        key=key,
        value=value,
        target_type=int,
        type_convert=int,
        is_optional=is_optional,
        default=default,
        options=options,
    )


def get_float(key, value, is_list=False, is_optional=False, default=None, options=None):
    """
    Get the value corresponding to the key and converts it to `float`/`list(float)`.

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
        return _get_typed_list_value(
            key=key,
            value=value,
            target_type=float,
            type_convert=float,
            is_optional=is_optional,
            default=default,
            options=options,
        )

    return _get_typed_value(
        key=key,
        value=value,
        target_type=float,
        type_convert=float,
        is_optional=is_optional,
        default=default,
        options=options,
    )


def get_boolean(
    key, value, is_list=False, is_optional=False, default=None, options=None
):
    """
    Get the value corresponding to the key and converts it to `bool`/`list(str)`.

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
        return _get_typed_list_value(
            key=key,
            value=value,
            target_type=bool,
            type_convert=lambda x: bool(strtobool(x)),
            is_optional=is_optional,
            default=default,
            options=options,
        )

    return _get_typed_value(
        key=key,
        value=value,
        target_type=bool,
        type_convert=lambda x: bool(strtobool(x)),
        is_optional=is_optional,
        default=default,
        options=options,
    )


def get_string(
    key, value, is_list=False, is_optional=False, default=None, options=None
):
    """
    Get the value corresponding to the key and converts it to `str`/`list(str)`.

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
        return _get_typed_list_value(
            key=key,
            value=value,
            target_type=str,
            type_convert=str,
            is_optional=is_optional,
            default=default,
            options=options,
        )

    return _get_typed_value(
        key=key,
        value=value,
        target_type=str,
        type_convert=str,
        is_optional=is_optional,
        default=default,
        options=options,
    )


def convert_to_dict(x, key):
    x = json.loads(x)
    if not isinstance(x, Mapping):
        raise PolyaxonSchemaError(
            "Cannot convert value `{}` (key: `{}`) to `dict`".format(x, key)
        )
    return x


def get_dict(key, value, is_list=False, is_optional=False, default=None, options=None):
    """
    Get the value corresponding to the key and converts it to `dict`.

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

    if is_list:
        return _get_typed_list_value(
            key=key,
            value=value,
            target_type=Mapping,
            type_convert=lambda x: convert_to_dict(x, key),
            is_optional=is_optional,
            default=default,
            options=options,
        )
    value = _get_typed_value(
        key=key,
        value=value,
        target_type=Mapping,
        type_convert=lambda x: convert_to_dict(x, key),
        is_optional=is_optional,
        default=default,
        options=options,
    )

    if not value:
        return default

    if not isinstance(value, Mapping):
        raise PolyaxonSchemaError(
            "Cannot convert value `{}` (key: `{}`) " "to `dict`".format(value, key)
        )
    return value


def get_dict_of_dicts(
    key, value, is_list=None, is_optional=False, default=None, options=None  # noqa
):
    """
    Get the value corresponding to the key and converts it to `dict`.

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
        key=key, value=value, is_optional=is_optional, default=default, options=options
    )
    if not value:
        return default

    for k in value:
        if not isinstance(value[k], Mapping):
            raise PolyaxonSchemaError(
                "`{}` must be an object. "
                "Received a non valid configuration for key `{}`.".format(value[k], key)
            )

    return value


def get_uri(key, value, is_list=False, is_optional=False, default=None, options=None):
    """
    Get the value corresponding to the key and converts it to `V1UriType`.

    Args
        key: the dict key.
        value: the value to parse.
        is_list: If this is one element or a list of elements.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
         `V1UriType`: value corresponding to the key.
    """
    if is_list:
        return _get_typed_list_value(
            key=key,
            value=value,
            target_type=V1UriType,
            type_convert=parse_uri_spec,
            is_optional=is_optional,
            default=default,
            options=options,
            base_types=(str, Mapping),
        )

    return _get_typed_value(
        key=key,
        value=value,
        target_type=V1UriType,
        type_convert=parse_uri_spec,
        is_optional=is_optional,
        default=default,
        options=options,
        base_types=(str, Mapping),
    )


def get_auth(
    key, value, is_list=False, is_optional=False, default=None, options=None
) -> V1AuthType:
    """
    Get the value corresponding to the key and converts it to `V1AuthType`.

    Args
        key: the dict key.
        value: the value to parse.
        is_list: If this is one element or a list of elements.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
         `V1AuthType`: value corresponding to the key.
    """
    if is_list:
        return _get_typed_list_value(
            key=key,
            value=value,
            target_type=V1AuthType,
            type_convert=parse_auth_spec,
            is_optional=is_optional,
            default=default,
            options=options,
            base_types=(str, Mapping),
        )

    return _get_typed_value(
        key=key,
        value=value,
        target_type=V1AuthType,
        type_convert=parse_auth_spec,
        is_optional=is_optional,
        default=default,
        options=options,
        base_types=(str, Mapping),
    )


def get_list(
    key, value, is_list=None, is_optional=False, default=None, options=None  # noqa
):
    """
    Get the value corresponding to the key and converts comma separated values to a list.

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
        parts = v.split(",")
        results = []
        for part in parts:
            part = part.strip()
            if part:
                results.append(part)
        return results

    return _get_typed_value(
        key=key,
        value=value,
        target_type=list,
        type_convert=parse_list,
        is_optional=is_optional,
        default=default,
        options=options,
    )


def get_wasbs_path(
    key, value, is_list=False, is_optional=False, default=None, options=None
) -> V1WasbType:
    """
    Get the value corresponding to the key and converts it to `V1WasbType`.

    Args
        key: the dict key.
        value: the value to parse.
        is_list: If this is one element or a list of elements.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
         `V1WasbType`: value corresponding to the key.
    """
    if is_list:
        return _get_typed_list_value(
            key=key,
            value=value,
            target_type=V1WasbType,
            type_convert=parse_wasbs_path,
            is_optional=is_optional,
            default=default,
            options=options,
            base_types=(str, Mapping),
        )

    return _get_typed_value(
        key=key,
        value=value,
        target_type=V1WasbType,
        type_convert=parse_wasbs_path,
        is_optional=is_optional,
        default=default,
        options=options,
        base_types=(str, Mapping),
    )


def get_gcs_path(
    key, value, is_list=False, is_optional=False, default=None, options=None
):
    """
    Get the value corresponding to the key and converts it to `V1GcsType`.

    Args
        key: the dict key.
        value: the value to parse.
        is_list: If this is one element or a list of elements.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
         `V1GcsType`: value corresponding to the key.
    """
    if is_list:
        return _get_typed_list_value(
            key=key,
            value=value,
            target_type=V1GcsType,
            type_convert=parse_gcs_path,
            is_optional=is_optional,
            default=default,
            options=options,
            base_types=(str, Mapping),
        )

    return _get_typed_value(
        key=key,
        value=value,
        target_type=V1GcsType,
        type_convert=parse_gcs_path,
        is_optional=is_optional,
        default=default,
        options=options,
        base_types=(str, Mapping),
    )


def get_s3_path(
    key, value, is_list=False, is_optional=False, default=None, options=None
):
    """
    Get the value corresponding to the key and converts it to `V1S3Type`.

    Args
        key: the dict key.
        value: the value to parse.
        is_list: If this is one element or a list of elements.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
         `V1S3Type`: value corresponding to the key.
    """
    if is_list:
        return _get_typed_list_value(
            key=key,
            value=value,
            target_type=V1S3Type,
            type_convert=parse_s3_path,
            is_optional=is_optional,
            default=default,
            options=options,
            base_types=(str, Mapping),
        )

    return _get_typed_value(
        key=key,
        value=value,
        target_type=V1S3Type,
        type_convert=parse_s3_path,
        is_optional=is_optional,
        default=default,
        options=options,
        base_types=(str, Mapping),
    )


def get_date(key, value, is_list=False, is_optional=False, default=None, options=None):
    """
    Get the value corresponding to the key and converts it to `date`/`list(date)`.

    Args:
        key: the dict key.
        value: the value to parse.
        is_list: If this is one element or a list of elements.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
        `date`: value corresponding to the key.
    """
    if is_list:
        return _get_typed_list_value(
            key=key,
            value=value,
            target_type=date,
            type_convert=fields.Date().deserialize,
            is_optional=is_optional,
            default=default,
            options=options,
        )

    return _get_typed_value(
        key=key,
        value=value,
        target_type=date,
        type_convert=fields.Date().deserialize,
        is_optional=is_optional,
        default=default,
        options=options,
    )


def get_datetime(
    key, value, is_list=False, is_optional=False, default=None, options=None
):
    """
    Get the value corresponding to the key and converts it to `datetime`/`list(datetime)`.

    Args:
        key: the dict key.
        value: the value to parse.
        is_list: If this is one element or a list of elements.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
        `date`: value corresponding to the key.
    """
    if is_list:
        return _get_typed_list_value(
            key=key,
            value=value,
            target_type=datetime,
            type_convert=fields.DateTime().deserialize,
            is_optional=is_optional,
            default=default,
            options=options,
        )

    return _get_typed_value(
        key=key,
        value=value,
        target_type=datetime,
        type_convert=fields.DateTime().deserialize,
        is_optional=is_optional,
        default=default,
        options=options,
    )


def get_dockerfile_init(
    key, value, is_list=False, is_optional=False, default=None, options=None
):
    """
    Get the value corresponding to the key and converts
    it to `V1DockerfileType`/`list(V1DockerfileType)`.

    Args:
        key: the dict key.
        value: the value to parse.
        is_list: If this is one element or a list of elements.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
        `date`: value corresponding to the key.
    """

    def convert_to_dockerfile_init(x):
        if not isinstance(x, Mapping):
            x = convert_to_dict(x, key)
        return V1DockerfileType.from_dict(x)

    if is_list:
        return _get_typed_list_value(
            key=key,
            value=value,
            target_type=V1DockerfileType,
            type_convert=convert_to_dockerfile_init,
            is_optional=is_optional,
            default=default,
            options=options,
            base_types=(str, Mapping),
        )

    return _get_typed_value(
        key=key,
        value=value,
        target_type=V1DockerfileType,
        type_convert=convert_to_dockerfile_init,
        is_optional=is_optional,
        default=default,
        options=options,
        base_types=(str, Mapping),
    )


def get_image_init(
    key, value, is_list=False, is_optional=False, default=None, options=None
):
    """
    Get the value corresponding to the key and converts
    it to `str`/`list(str)`.

    Args:
        key: the dict key.
        value: the value to parse.
        is_list: If this is one element or a list of elements.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
        `date`: value corresponding to the key.
    """

    def convert_to_image_init(x):
        if isinstance(x, Mapping):
            if "name" not in x:
                raise PolyaxonSchemaError(
                    "Polyaxon received an image that does not contain an image"
                )
            logger.info(
                "Polyaxon received a legacy image format. "
                "The operation will not run correctly"
            )
            return x.get("name")
        if not isinstance(x, Mapping):
            try:
                x = convert_to_dict(x, key)
            except:
                return x

        if "name" not in x:
            raise PolyaxonSchemaError(
                "Polyaxon received an image that does not contain an image"
            )
        logger.info(
            "Polyaxon received a legacy image format. "
            "The operation will not run correctly"
        )
        return x.get("name")

    if is_list:
        return _get_typed_list_value(
            key=key,
            value=value,
            target_type=str,
            type_convert=convert_to_image_init,
            is_optional=is_optional,
            default=default,
            options=options,
            base_types=(str, Mapping),
        )

    return _get_typed_value(
        key=key,
        value=value,
        target_type=str,
        type_convert=convert_to_image_init,
        is_optional=is_optional,
        default=default,
        options=options,
        base_types=(str, Mapping),
    )


def get_event_init(
    key, value, is_list=False, is_optional=False, default=None, options=None
):
    """
    Get the value corresponding to the key and converts
    it to `V1EventType`/`list(V1EventType)`.

    Args:
        key: the dict key.
        value: the value to parse.
        is_list: If this is one element or a list of elements.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
        `date`: value corresponding to the key.
    """

    def convert_to_event_init(x):
        if not isinstance(x, Mapping):
            x = convert_to_dict(x, key)
        return V1EventType.from_dict(x)

    if is_list:
        return _get_typed_list_value(
            key=key,
            value=value,
            target_type=V1EventType,
            type_convert=convert_to_event_init,
            is_optional=is_optional,
            default=default,
            options=options,
            base_types=(str, Mapping),
        )

    return _get_typed_value(
        key=key,
        value=value,
        target_type=V1EventType,
        type_convert=convert_to_event_init,
        is_optional=is_optional,
        default=default,
        options=options,
        base_types=(str, Mapping),
    )


def get_git_init(
    key, value, is_list=False, is_optional=False, default=None, options=None
):
    """
    Get the value corresponding to the key and converts
    it to `V1GitType`/`list(V1GitType)`.

    Args:
        key: the dict key.
        value: the value to parse.
        is_list: If this is one element or a list of elements.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
        `date`: value corresponding to the key.
    """

    def convert_to_git_init(x):
        if not isinstance(x, Mapping):
            x = convert_to_dict(x, key)
        return V1GitType.from_dict(x)

    if is_list:
        return _get_typed_list_value(
            key=key,
            value=value,
            target_type=V1GitType,
            type_convert=convert_to_git_init,
            is_optional=is_optional,
            default=default,
            options=options,
            base_types=(str, Mapping),
        )

    return _get_typed_value(
        key=key,
        value=value,
        target_type=V1GitType,
        type_convert=convert_to_git_init,
        is_optional=is_optional,
        default=default,
        options=options,
        base_types=(str, Mapping),
    )


def get_artifacts_init(
    key, value, is_list=False, is_optional=False, default=None, options=None
):
    """
    Get the value corresponding to the key and converts
    it to `V1ArtifactsType`/`list(V1ArtifactsType)`.

    Args:
        key: the dict key.
        value: the value to parse.
        is_list: If this is one element or a list of elements.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.

    Returns:
        `date`: value corresponding to the key.
    """

    def convert_to_artifacts_init(x):
        if not isinstance(x, Mapping):
            x = convert_to_dict(x, key)
        return V1ArtifactsType.from_dict(x)

    if is_list:
        return _get_typed_list_value(
            key=key,
            value=value,
            target_type=V1ArtifactsType,
            type_convert=convert_to_artifacts_init,
            is_optional=is_optional,
            default=default,
            options=options,
            base_types=(str, Mapping),
        )

    return _get_typed_value(
        key=key,
        value=value,
        target_type=V1ArtifactsType,
        type_convert=convert_to_artifacts_init,
        is_optional=is_optional,
        default=default,
        options=options,
        base_types=(str, Mapping),
    )


def _check_options(key, value, options):
    if options and value not in options:
        raise PolyaxonSchemaError(
            "The value `{}` provided for key `{}` "
            "is not one of the possible values.".format(value, key)
        )


def _get_typed_value(
    key,
    value,
    target_type,
    type_convert,
    is_optional=False,
    default=None,
    options=None,
    base_types=None,
):
    """
    Return the value corresponding to the key converted to the given type.

    Args:
        key: the dict key.
        target_type: The type we expect the variable or key to be in.
        type_convert: A lambda expression that converts the key to the desired type.
        is_optional: To raise an error if key was not found.
        default: default value if is_optional is True.
        options: list/tuple if provided, the value must be one of these values.
        base_types: the base types to check for conversion

    Returns:
        The corresponding value of the key converted.
    """
    if value is None or value == NO_VALUE_FOUND:
        if not is_optional:
            raise PolyaxonSchemaError(
                "No value was provided for the non optional key `{}`.".format(key)
            )
        return default

    base_types = base_types or str
    if isinstance(value, base_types):
        try:
            # _add_key(key, is_secret=is_secret, is_local=is_local)
            _check_options(key=key, value=value, options=options)
            return type_convert(value)
        except (ValueError, ValidationError):
            raise PolyaxonSchemaError(
                "Cannot convert value `{}` (key: `{}`) "
                "to `{}`".format(value, key, target_type)
            )

    if isinstance(value, target_type):
        # _add_key(key, is_secret=is_secret, is_local=is_local)
        _check_options(key=key, value=value, options=options)
        return value
    raise PolyaxonSchemaError(
        "Cannot convert value `{}` (key: `{}`) "
        "to `{}`".format(value, key, target_type)
    )


def _get_typed_list_value(
    key,
    value,
    target_type,
    type_convert,
    is_optional=False,
    default=None,
    options=None,
    base_types=None,
):
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
        base_types: the base types to check for conversion
    """

    try:
        value = _get_typed_value(
            key=key,
            value=value,
            target_type=list,
            type_convert=json.loads,
            is_optional=is_optional,
            default=default,
            options=options,
        )
    except PolyaxonSchemaError as e:
        # We try to parsing a list from a string
        value = get_list(
            key=key,
            value=value,
            is_optional=is_optional,
            default=default,
            options=options,
        )
        if len(value) <= 1:
            raise e

    if not value:
        return default

    raise_type = "dict" if target_type == Mapping else target_type
    base_types = base_types or str

    if not isinstance(value, list):
        raise PolyaxonSchemaError(
            "Cannot convert value `{}` (key: `{}`) "
            "to `{}`".format(value, key, raise_type)
        )
    # If we are here the value must be a list
    result = []
    for v in value:
        if isinstance(v, base_types):
            try:
                result.append(type_convert(v))
            except (ValueError, ValidationError):
                raise PolyaxonSchemaError(
                    "Cannot convert value `{}` (found in list key: `{}`) "
                    "to `{}`".format(v, key, raise_type)
                )
        elif isinstance(v, target_type):
            result.append(v)

        else:
            raise PolyaxonSchemaError(
                "Cannot convert value `{}` (found in list key: `{}`) "
                "to `{}`".format(v, key, raise_type)
            )
    return result


def parse_uri_spec(uri_spec) -> V1UriType:
    if isinstance(uri_spec, V1UriType):
        return uri_spec

    if isinstance(uri_spec, Mapping):
        return V1UriType.from_dict(uri_spec)

    try:
        auth_spec = convert_to_dict(uri_spec, "")
        return V1UriType.from_dict(auth_spec)
    except (PolyaxonSchemaError, JSONDecodeError):
        pass

    parts = uri_spec.split("@")
    if len(parts) != 2:
        raise PolyaxonSchemaError(
            "Received invalid uri_spec `{}`. "
            "The uri must be in the format `user:pass@host`".format(uri_spec)
        )

    user_pass, host = parts
    user_pass = user_pass.split(":")
    if len(user_pass) != 2:
        raise PolyaxonSchemaError(
            "Received invalid uri_spec `{}`. `user:host` is not conform."
            "The uri must be in the format `user:pass@host`".format(uri_spec)
        )

    return V1UriType(user=user_pass[0], password=user_pass[1], host=host)


def parse_auth_spec(auth_spec: Union[str, Dict, V1AuthType]) -> V1AuthType:
    if isinstance(auth_spec, V1AuthType):
        return auth_spec

    if isinstance(auth_spec, Mapping):
        return V1AuthType.from_dict(auth_spec)

    try:
        auth_spec = convert_to_dict(auth_spec, "")
        return V1AuthType.from_dict(auth_spec)
    except (PolyaxonSchemaError, JSONDecodeError):
        pass

    user_pass = auth_spec.split(":")
    if len(user_pass) != 2:
        raise PolyaxonSchemaError(
            "Received invalid uri_spec `{}`. `user:host` is not conform."
            "The uri must be in the format `user:pass`".format(auth_spec)
        )

    return V1AuthType(user=user_pass[0], password=user_pass[1])


def parse_wasbs_path(wasbs_path):
    if isinstance(wasbs_path, V1WasbType):
        return wasbs_path

    if isinstance(wasbs_path, Mapping):
        return V1WasbType.from_dict(wasbs_path)

    parsed_url = urlparse(wasbs_path)
    if parsed_url.scheme != "wasbs":
        raise PolyaxonSchemaError("Received an invalid url `{}`".format(wasbs_path))
    match = re.match("([^@]+)@([^.]+)\\.blob\\.core\\.windows\\.net", parsed_url.netloc)
    if match is None:
        raise PolyaxonSchemaError(
            "wasbs url must be of the form <container>@<account>.blob.core.windows.net"
        )

    container = match.group(1)
    storage_account = match.group(2)
    path = parsed_url.path
    if path.startswith("/"):
        path = path[1:]
    return V1WasbType(container, storage_account, path)


def parse_gcs_path(gcs_path):
    """
    Parses and validates a google cloud storage url.

    Returns:
        tuple(bucket_name, blob).
    """
    if isinstance(gcs_path, V1GcsType):
        return gcs_path

    if isinstance(gcs_path, Mapping):
        return V1GcsType.from_dict(gcs_path)

    parsed_url = urlparse(gcs_path)
    if not parsed_url.netloc:
        raise PolyaxonSchemaError("Received an invalid GCS url `{}`".format(gcs_path))
    if parsed_url.scheme != "gs":
        raise PolyaxonSchemaError("Received an invalid url GCS `{}`".format(gcs_path))
    blob = parsed_url.path.lstrip("/")
    return V1GcsType(parsed_url.netloc, blob)


def parse_s3_path(s3_path):
    """
    Parses and validates an S3 url.

    Returns:
         tuple(bucket_name, key).
    """
    if isinstance(s3_path, V1S3Type):
        return s3_path

    if isinstance(s3_path, Mapping):
        return V1S3Type.from_dict(s3_path)

    parsed_url = urlparse(s3_path)
    if not parsed_url.netloc:
        raise PolyaxonSchemaError("Received an invalid S3 url `{}`".format(s3_path))
    else:
        bucket_name = parsed_url.netloc
        key = parsed_url.path.strip("/")
        return V1S3Type(bucket_name, key)


TYPE_MAPPING = {
    types.ANY: lambda x: x,
    types.INT: get_int,
    types.FLOAT: get_float,
    types.BOOL: get_boolean,
    types.STR: get_string,
    types.DICT: get_dict,
    types.DICT_OF_DICTS: get_dict_of_dicts,
    types.URI: get_uri,
    types.AUTH: get_auth,
    types.LIST: get_list,
    types.GCS: get_gcs_path,
    types.S3: get_s3_path,
    types.WASB: get_wasbs_path,
    types.PATH: get_string,
    types.METRIC: get_float,
    types.METADATA: get_dict,
    types.DATE: get_date,
    types.DATETIME: get_datetime,
    types.DOCKERFILE: get_dockerfile_init,
    types.GIT: get_git_init,
    types.IMAGE: get_image_init,
    types.EVENT: get_event_init,
    types.ARTIFACTS: get_artifacts_init,
}
