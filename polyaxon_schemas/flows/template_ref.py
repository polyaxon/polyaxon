# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from marshmallow import ValidationError, fields, validates_schema

from polyaxon_schemas.base import BaseConfig, BaseSchema


def validate_template(**kwargs):
    if len([i for i in six.itervalues(kwargs) if i is not None and i != '']) != 1:
        raise ValidationError(
            'Template requires one and only one param: '
            'name, url, path, action, or event.')


class TemplateRefSchema(BaseSchema):
    name = fields.Str(allow_none=True)
    url = fields.Str(allow_none=True)
    path = fields.Str(allow_none=True)
    action = fields.Str(allow_none=True)
    event = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return TemplateRefConfig

    @validates_schema
    def validate_template(self, values):
        validate_template(name=values.get('name'),
                          url=values.get('url'),
                          path=values.get('path'),
                          action=values.get('action'),
                          event=values.get('event'))


class TemplateRefConfig(BaseConfig):
    SCHEMA = TemplateRefSchema
    IDENTIFIER = 'template'
    REDUCED_ATTRIBUTES = ['name', 'url', 'path', 'action', 'event']

    def __init__(self, name=None, url=None, path=None, action=None, event=None):
        validate_template(name=name, url=url, path=path, action=action, event=event)
        self.name = name
        self.url = url
        self.path = path
        self.action = action
        self.event = event
