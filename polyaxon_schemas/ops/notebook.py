# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon_schemas.ops.run import BaseRunConfig, BaseRunSchema
from polyaxon_schemas.utils import NotebookBackend


def validate_notebook_backend(backend):
    if backend and backend not in NotebookBackend.VALUES:
        raise ValidationError('Notebook backend `{}` not supported'.format(backend))


class NotebookSchema(BaseRunSchema):
    kind = fields.Str(allow_none=None, validate=validate.Equal('notebook'))
    backend = fields.Str(allow_none=True, validate=validate.OneOf(NotebookBackend.VALUES))

    @staticmethod
    def schema_config():
        return NotebookConfig

    @validates_schema
    def validate_backend(self, data):
        validate_notebook_backend(data.get('backend'))


class NotebookConfig(BaseRunConfig):
    IDENTIFIER = 'notebook'
    SCHEMA = NotebookSchema

    def __init__(self,
                 kind=None,
                 version=None,
                 logging=None,
                 tags=None,
                 environment=None,
                 build=None,
                 backend=None,
                 ):
        super(NotebookConfig, self).__init__(kind=kind,
                                             version=version,
                                             logging=logging,
                                             tags=tags,
                                             environment=environment,
                                             build=build)
        validate_notebook_backend(backend)
        self.backend = backend
