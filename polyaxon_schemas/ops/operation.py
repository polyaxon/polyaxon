# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import re
import warnings

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon_schemas.base import NAME_REGEX, BaseConfig, BaseSchema
from polyaxon_schemas.ops import params as ops_params
from polyaxon_schemas.ops.environments.pods import EnvironmentSchema
from polyaxon_schemas.ops.io import IOSchema
from polyaxon_schemas.ops.logging import LoggingSchema
from polyaxon_schemas.ops.params import get_param_display_value

PARAM_REGEX = re.compile(r'{{\s*([^\s]*)\s*}}')


def validate_declarations(values):
    if values.get('declarations') and values.get('params'):
        raise ValidationError('You should only use `params`.')

    if values.get('declarations'):
        warnings.warn(
            'The `declarations` parameter is deprecated and will be removed in next release, '
            'please use `params` instead',
            DeprecationWarning)
        values['params'] = values.pop('declarations')

    return values


class BaseOpSchema(BaseSchema):
    version = fields.Int(allow_none=True)
    kind = fields.Str(allow_none=True)
    logging = fields.Nested(LoggingSchema, allow_none=True)
    name = fields.Str(validate=validate.Regexp(regex=NAME_REGEX), allow_none=True)
    description = fields.Str(allow_none=True)
    tags = fields.List(fields.Str(), allow_none=True)
    environment = fields.Nested(EnvironmentSchema, allow_none=True)
    params = fields.Raw(allow_none=True)
    declarations = fields.Raw(allow_none=True)
    inputs = fields.Nested(IOSchema, allow_none=True, many=True)
    outputs = fields.Nested(IOSchema, allow_none=True, many=True)

    @staticmethod
    def schema_config():
        return BaseOpConfig

    @validates_schema
    def validate_declarations(self, values):
        validate_declarations(values)

    @validates_schema
    def validate_params(self, values):
        ops_params.validate_params(params=values.get('params'),
                                   inputs=values.get('inputs'),
                                   outputs=values.get('outputs'),
                                   is_template=True,
                                   is_run=True)


class BaseOpConfig(BaseConfig):
    SCHEMA = BaseOpSchema
    IDENTIFIER = 'operation'
    REDUCED_ATTRIBUTES = [
        'version',
        'kind',
        'logging',
        'name',
        'description',
        'tags',
        'environment',
        'params',
        'inputs',
        'outputs',
    ]

    def __init__(self,
                 version=None,
                 kind=None,
                 logging=None,
                 name=None,
                 description=None,
                 tags=None,
                 environment=None,
                 params=None,
                 declarations=None,
                 inputs=None,
                 outputs=None):
        self.version = version
        self.kind = kind
        self.logging = logging
        self.name = name
        self.description = description
        self.tags = tags
        self.environment = environment
        validate_declarations({'params': params, 'declarations': declarations})
        self.params = params or declarations
        self._validated_params = ops_params.validate_params(params=self.params,
                                                            inputs=inputs,
                                                            outputs=outputs,
                                                            is_template=True,
                                                            is_run=True)
        self.inputs = inputs
        self.outputs = outputs

    def get_params(self, context):
        """Return all params: Merge params if passed, if not default values."""
        if not self._validated_params:
            return self.params

        params = {}
        for param in self._validated_params:
            if not param.entity_ref:
                value = param.value
            else:
                value = context[param.value.replace('.', '__')]
            params[param.name] = get_param_display_value(param=param, value=value)

        return params

    def get_params_with_refs(self):
        return [param for param in self._validated_params if param.entity_ref]
