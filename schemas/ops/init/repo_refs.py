# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from schemas.base import BaseConfig, BaseSchema


class RepoRefSchema(BaseSchema):
    name = fields.Str(allow_none=True)
    commit = fields.Str(allow_none=True)
    branch = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return RepoRefConfig


class RepoRefConfig(BaseConfig):
    IDENTIFIER = "repo_ref"
    SCHEMA = RepoRefSchema
    REDUCED_ATTRIBUTES = ["name", "commit", "branch"]

    def __init__(self, name, commit=None, branch=None):
        self.name = name
        self.commit = commit
        self.branch = branch
