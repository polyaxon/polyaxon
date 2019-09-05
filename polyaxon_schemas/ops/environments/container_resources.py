# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseSchema


class ContainerResourcesSchema(BaseSchema):
    limits = fields.Dict(allow_none=True)
    requests = fields.Dict(allow_none=True)

    @staticmethod
    def schema_config():
        return ContainerResourcesConfig


class ContainerResourcesConfig(BaseConfig):
    """
    K8S container resources config.

    Args:
        limits: `K8SResourcesEntry`.
        requests: `K8SResourcesEntry`.
    """

    IDENTIFIER = "resources"
    SCHEMA = ContainerResourcesSchema
    REDUCED_ATTRIBUTES = ["limits", "requests"]

    def __init__(self, limits=None, requests=None):
        self.limits = limits
        self.requests = requests
