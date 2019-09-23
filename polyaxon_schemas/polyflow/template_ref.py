# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from marshmallow import ValidationError, fields, validates_schema

from polyaxon_schemas.base import BaseConfig, BaseSchema


def validate_template(**kwargs):
    if len([i for i in six.itervalues(kwargs) if i is not None and i != ""]) != 1:
        raise ValidationError(
            "Template requires one and only one param: "
            "name, url, path, or hub."
        )


class TemplateRefSchema(BaseSchema):
    name = fields.Str(allow_none=True)
    url = fields.Str(allow_none=True)
    path = fields.Str(allow_none=True)
    hub = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return TemplateRefConfig

    @validates_schema
    def validate_template(self, values):
        validate_template(
            name=values.get("name"),
            url=values.get("url"),
            path=values.get("path"),
            hub=values.get("hub"),
        )


class TemplateRefConfig(BaseConfig):
    SCHEMA = TemplateRefSchema
    IDENTIFIER = "template"
    REDUCED_ATTRIBUTES = ["name", "url", "path", "hub"]

    def __init__(self, name=None, url=None, path=None, hub=None):
        validate_template(name=name, url=url, path=path, hub=hub)
        self.name = name
        self.url = url
        self.path = path
        self.hub = hub
