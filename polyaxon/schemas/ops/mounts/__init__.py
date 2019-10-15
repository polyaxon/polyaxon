# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.schemas.ops.mounts.artifact_refs import ArtifactRefSchema
from polyaxon.schemas.ops.mounts.k8s_resource_refs import K8SResourceRefSchema


class MountsSchema(BaseSchema):
    secrets = fields.Nested(K8SResourceRefSchema, many=True, allow_none=True)
    config_maps = fields.Nested(K8SResourceRefSchema, many=True, allow_none=True)
    artifacts = fields.Nested(ArtifactRefSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return MountsConfig


class MountsConfig(BaseConfig):
    """
    Mounts config.
    """

    IDENTIFIER = "mounts"
    SCHEMA = MountsSchema
    REDUCED_ATTRIBUTES = ["secrets", "config_maps", "artifacts"]

    def __init__(self, secrets=None, config_maps=None, artifacts=None):
        self.secrets = secrets
        self.config_maps = config_maps
        self.artifacts = artifacts
