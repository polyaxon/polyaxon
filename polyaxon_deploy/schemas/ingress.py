# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields
from polyaxon_schemas.environments import K8SContainerResourcesSchema

from polyaxon_deploy.schemas.base import BaseConfig, BaseSchema


class IngressSchema(BaseSchema):
    enabled = fields.Bool(allow_none=True)
    tls = fields.Dict(allow_none=True)
    annotations = fields.Dict(allow_none=True)
    resources = fields.Nested(K8SContainerResourcesSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return IngressConfig


class IngressConfig(BaseConfig):
    SCHEMA = IngressSchema
    REDUCED_ATTRIBUTES = ['enabled', 'tls', 'annotations', 'resources']

    def __init__(self,
                 enabled=None,
                 tls=None,
                 annotations=None,
                 resources=None):
        self.enabled = enabled
        self.tls = tls
        self.annotations = annotations
        self.resources = resources
