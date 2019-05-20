# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import ValidationError, fields, validate, validates_schema
from rhea import RheaError, parser

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.ops.io.types import IOTypes


def validate_io(name, iotype, default, is_optional, is_list, is_flag):
    if iotype and default:
        try:
            parser.TYPE_MAPPING[iotype](
                key=name,
                value=default,
                is_list=is_list,
                is_optional=is_optional,
                default=None,
                options=None)

        except RheaError as e:
            raise ValidationError('IO `%s` Could not parse default value `%s`, '
                                  'an error was encountered: %s' % (name, default, e))

    if not is_optional and default:
        raise ValidationError('IO `%s` is not optional and has default value `%s`. '
                              'Please either make it optional or remove the default value.')

    if is_flag and iotype != IOTypes.BOOL:
        raise ValidationError('IO type `{}` cannot be a flag, iut must be a `{}`'.format(
            iotype, IOTypes.BOOL
        ))


class IOSchema(BaseSchema):
    name = fields.Str()
    description = fields.Str(allow_none=True)
    iotype = fields.Str(allow_none=True,
                        data_key="type",
                        validate=validate.OneOf(IOTypes.VALUES))
    default = fields.Raw(allow_none=True)
    is_optional = fields.Bool(allow_none=True)
    is_list = fields.Bool(allow_none=True)
    is_flag = fields.Bool(allow_none=True)
    options = fields.List(fields.Raw(), allow_none=True)

    @staticmethod
    def schema_config():
        return IOConfig

    @validates_schema
    def validate_io(self, values):
        validate_io(name=values.get('name'),
                    iotype=values.get('iotype'),
                    default=values.get('default'),
                    is_list=values.get('is_list'),
                    is_optional=values.get('is_optional'),
                    is_flag=values.get('is_flag'))


class IOConfig(BaseConfig):
    SCHEMA = IOSchema
    IDENTIFIER = 'io'
    REDUCED_ATTRIBUTES = [
        'description',
        'type',
        'default',
        'is_optional',
        'is_flag',
        'is_list',
        'options']

    def __init__(self,
                 name,
                 description=None,
                 iotype=None,
                 default=None,
                 is_optional=None,
                 is_list=None,
                 is_flag=None,
                 options=None):
        validate_io(name=name,
                    iotype=iotype,
                    default=default,
                    is_optional=is_optional,
                    is_list=is_list,
                    is_flag=is_flag)

        self.name = name
        self.description = description
        self.iotype = iotype
        self.default = default
        self.is_optional = is_optional
        self.is_list = is_list
        self.is_flag = is_flag
        self.options = options

    def validate_value(self, value):
        if self.iotype is None:
            return value

        try:
            return parser.TYPE_MAPPING[self.iotype](
                key=self.name,
                value=value,
                is_list=self.is_list,
                is_optional=self.is_optional,
                default=self.default,
                options=self.options)
        except RheaError as e:
            raise ValidationError('Could not parse value `%s`, '
                                  'an error was encountered: %s' % (value, e))
