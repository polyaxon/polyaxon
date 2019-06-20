# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import ValidationError, fields, validates_schema
from polyaxon_deploy.schemas.base import BaseConfig, BaseSchema


def validate_security_context(user, group):
    if any([user, group]) and not all([user, group]):
        raise ValidationError(
            "Security context requires both `user` and `group` or none.")


class SecurityContextSchema(BaseSchema):
    enabled = fields.Bool(allow_none=True)
    user = fields.Int(allow_none=True)
    group = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return SecurityContextConfig

    @validates_schema
    def validate_security_context(self, data):
        validate_security_context(data.get('user'), data.get('group'))


class SecurityContextConfig(BaseConfig):
    SCHEMA = SecurityContextSchema
    REDUCED_ATTRIBUTES = ['enabled', 'user', 'group']

    def __init__(self, enabled=None, user=None, group=None):
        validate_security_context(user, group)
        self.enabled = enabled
        self.user = user
        self.group = group
