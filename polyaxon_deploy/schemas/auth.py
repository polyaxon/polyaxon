# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import ValidationError, fields, validates_schema
from polyaxon_deploy.schemas.base import BaseConfig, BaseSchema


def validate_auth(enabled, clientId, clientSecret):  # noqa
    if enabled:
        if not all([clientId, clientSecret]):
            raise ValidationError(
                "The auth backend config requires a clientId and a clientSecret.")


class BaseAuthSchema(BaseSchema):
    enabled = fields.Bool(allow_none=True)
    clientId = fields.Str(allow_none=True)
    clientSecret = fields.Str(allow_none=True)
    tenantId = fields.Str(allow_none=True)
    url = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return BaseAuthConfig

    @validates_schema
    def validate_auth(self, data):
        validate_auth(data.get('enabled'), data.get('clientId'), data.get('clientSecret'))


class BaseAuthConfig(BaseConfig):
    SCHEMA = BaseAuthSchema
    REDUCED_ATTRIBUTES = ['enabled', 'clientId', 'clientSecret', 'tenantId', 'url']

    def __init__(self,  # noqa
                 enabled=None,
                 clientId=None,
                 clientSecret=None,
                 tenantId=None,
                 url=None):
        validate_auth(enabled, clientId, clientSecret)

        self.enabled = enabled
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.tenantId = tenantId
        self.url = url


class AuthSchema(BaseSchema):
    github = fields.Nested(BaseAuthSchema, allow_none=True)
    gitlab = fields.Nested(BaseAuthSchema, allow_none=True)
    bitbucket = fields.Nested(BaseAuthSchema, allow_none=True)
    azure = fields.Nested(BaseAuthSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return AuthConfig


class AuthConfig(BaseConfig):
    SCHEMA = AuthSchema
    REDUCED_ATTRIBUTES = ['github', 'gitlab', 'bitbucket', 'azure']

    def __init__(self, github=None, gitlab=None, bitbucket=None, azure=None):
        self.github = github
        self.gitlab = gitlab
        self.bitbucket = bitbucket
        self.azure = azure
