# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from schemas.base import BaseConfig, BaseSchema
from schemas.ops.init.build_context import BuildContextSchema
from schemas.ops.init.repo_refs import RepoRefSchema
from schemas.ops.mounts import ArtifactRefSchema


class InitSchema(BaseSchema):
    repos = fields.Nested(RepoRefSchema, many=True, allow_none=True)
    artifacts = fields.Nested(ArtifactRefSchema, many=True, allow_none=True)
    build = fields.Nested(BuildContextSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return InitConfig


class InitConfig(BaseConfig):
    """
    Init config.
    """

    IDENTIFIER = "init"
    SCHEMA = InitSchema
    REDUCED_ATTRIBUTES = [
        "repos",
        "artifacts",
        "build",
    ]

    def __init__(
        self,
        repos=None,
        artifacts=None,
        build=None,
    ):
        self.repos = repos
        self.artifacts = artifacts
        self.build = build
