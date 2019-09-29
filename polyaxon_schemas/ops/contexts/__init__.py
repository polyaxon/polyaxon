# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.ops.contexts.artifact_refs import ArtifactRefSchema
from polyaxon_schemas.ops.contexts.build_context import BuildContextSchema
from polyaxon_schemas.ops.contexts.k8s_resource_refs import K8SResourceRefSchema
from polyaxon_schemas.ops.contexts.outputs_context import OutputsContextSchema
from polyaxon_schemas.ops.contexts.repo_refs import RepoRefSchema


class ContextsSchema(BaseSchema):
    secrets = fields.Nested(K8SResourceRefSchema, many=True, allow_none=True)
    config_maps = fields.Nested(K8SResourceRefSchema, many=True, allow_none=True)
    artifacts = fields.Nested(ArtifactRefSchema, many=True, allow_none=True)
    repos = fields.Nested(RepoRefSchema, many=True, allow_none=True)
    registry = fields.Str(allow_none=True)
    outputs = fields.Nested(OutputsContextSchema, allow_none=True)
    build = fields.Nested(BuildContextSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return ContextsConfig


class ContextsConfig(BaseConfig):
    """
    Context config.
    """

    IDENTIFIER = "contexts"
    SCHEMA = ContextsSchema
    REDUCED_ATTRIBUTES = [
        "secrets",
        "config_maps",
        "artifacts",
        "repos",
        "registry",
        "outputs",
        "build",
    ]

    def __init__(
        self,
        secrets=None,
        config_maps=None,
        artifacts=None,
        repos=None,
        registry=None,
        outputs=None,
        build=None,
    ):
        self.secrets = secrets
        self.config_maps = config_maps
        self.artifacts = artifacts
        self.repos = repos
        self.registry = registry
        self.outputs = outputs
        self.build = build
