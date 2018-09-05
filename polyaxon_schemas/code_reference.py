# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_dump, post_load

from polyaxon_schemas.base import BaseConfig


class CodeReferenceSchema(Schema):
    id = fields.Int(allow_none=True)
    commit = fields.Str(allow_none=True)
    head = fields.Str(allow_none=True)
    branch = fields.Str(allow_none=True)
    git_url = fields.Str(allow_none=True)
    is_dirty = fields.Boolean(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return CodeReferenceConfig(**data)

    @post_dump
    def unmake(self, data):
        return CodeReferenceConfig.remove_reduced_attrs(data)


class CodeReferenceConfig(BaseConfig):
    SCHEMA = CodeReferenceSchema
    IDENTIFIER = 'CodeReference'
    DEFAULT_EXCLUDE_ATTRIBUTES = ['id']

    def __init__(self,
                 id=None,  # pylint:disable=redefined-builtin
                 commit=None,
                 head=None,
                 branch=None,
                 git_url=None,
                 is_dirty=None,
                 ):
        self.id = id
        self.commit = commit
        self.head = head
        self.branch = branch
        self.git_url = git_url
        self.is_dirty = is_dirty
