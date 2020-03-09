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
from typing import Any, List

import polyaxon_sdk

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon import types
from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.parser import parser
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig


def validate_io_value(
    name: str,
    iotype: str,
    value: Any,
    default: Any,
    is_optional: bool,
    is_list: bool,
    options: List[Any],
    parse: bool = True,
):
    try:
        parsed_value = parser.TYPE_MAPPING[iotype](
            key=name,
            value=value,
            is_list=is_list,
            is_optional=is_optional,
            default=default,
            options=options,
        )
        if parse:
            return parsed_value
        # Return the original value, the parser will return specs sometimes
        if value is not None:
            return value
        return default
    except PolyaxonSchemaError as e:
        raise ValidationError(
            "Could not parse value `%s`, an error was encountered: %s" % (value, e)
        )


def validate_io(name, iotype, value, is_optional, is_list, is_flag, options):
    if iotype and value:
        validate_io_value(
            name=name,
            iotype=iotype,
            value=value,
            default=None,
            is_list=is_list,
            is_optional=is_optional,
            options=options,
        )

    if not is_optional and value:
        raise ValidationError(
            "IO `{}` is not optional and has default value `{}`. "
            "Please either make it optional or remove the default value.".format(
                name, value
            )
        )

    if is_flag and iotype != types.BOOL:
        raise ValidationError(
            "IO type `{}` cannot be a flag, iut must be a `{}`".format(
                iotype, types.BOOL
            )
        )


class IOSchema(BaseCamelSchema):
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    iotype = fields.Str(
        allow_none=True, data_key="type", validate=validate.OneOf(types.VALUES)
    )
    value = fields.Raw(allow_none=True)
    is_optional = fields.Bool(allow_none=True)
    is_list = fields.Bool(allow_none=True)
    is_flag = fields.Bool(allow_none=True)
    delay_validation = fields.Bool(allow_none=True)
    options = fields.List(fields.Raw(), allow_none=True)

    @staticmethod
    def schema_config():
        return V1IO

    @validates_schema
    def validate_io(self, values, **kwargs):
        validate_io(
            name=values.get("name"),
            iotype=values.get("iotype"),
            value=values.get("value"),
            is_list=values.get("is_list"),
            is_optional=values.get("is_optional"),
            is_flag=values.get("is_flag"),
            options=values.get("options"),
        )


class V1IO(BaseConfig, polyaxon_sdk.V1IO):
    SCHEMA = IOSchema
    IDENTIFIER = "io"
    REDUCED_ATTRIBUTES = [
        "description",
        "type",
        "value",
        "isOptional",
        "isFlag",
        "isList",
        "delayValidation",
        "options",
    ]

    def validate_value(self, value: Any, parse: bool = True):
        if self.iotype is None:
            return value

        return validate_io_value(
            name=self.name,
            iotype=self.iotype,
            value=value,
            default=self.value,
            is_list=self.is_list,
            is_optional=self.is_optional,
            options=self.options,
            parse=parse,
        )

    def get_repr_from_value(self, value):
        """A string representation that is used to create hash cache"""
        value = self.validate_value(value=value, parse=False)
        io_dict = self.to_light_dict(include_attrs=["name", "type"])
        io_dict["value"] = value
        return io_dict

    def get_repr(self):
        """A string representation that is used to create hash cache"""
        io_dict = self.to_light_dict(include_attrs=["name", "type", "value"])
        return io_dict
