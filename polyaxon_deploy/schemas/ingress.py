# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_deploy.schemas.base import BaseConfig, BaseSchema


class IngressSchema(BaseSchema):
    enabled = fields.Bool(allow_none=True)
    hostName = fields.Str(allow_none=True)
    path = fields.Str(allow_none=True)
    tls = fields.List(fields.Dict(allow_none=True), allow_none=True)
    annotations = fields.Dict(allow_none=True)

    @staticmethod
    def schema_config():
        return IngressConfig


class IngressConfig(BaseConfig):
    SCHEMA = IngressSchema
    REDUCED_ATTRIBUTES = ['enabled', 'hostName', 'tls', 'annotations', 'path']

    def __init__(self,  # noqa
                 enabled=None,
                 hostName=None,
                 path=None,
                 tls=None,
                 annotations=None,):
        self.enabled = enabled
        self.hostName = hostName
        self.path = path
        self.tls = tls
        self.annotations = annotations
