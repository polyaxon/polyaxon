# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import ValidationError, fields, validate, validates_schema

from polyaxon_schemas.ops.notebook.backends import NotebookBackend
from polyaxon_schemas.ops.run import BaseRunConfig, BaseRunSchema


def validate_notebook_backend(backend):
    if backend and backend not in NotebookBackend.VALUES:
        raise ValidationError('Notebook backend `{}` not supported'.format(backend))


class NotebookSchema(BaseRunSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal('notebook'))
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
    REDUCED_ATTRIBUTES = BaseRunConfig.REDUCED_ATTRIBUTES + ['backend']

    def __init__(self,
                 version=None,
                 kind=None,
                 logging=None,
                 name=None,
                 description=None,
                 tags=None,
                 environment=None,
                 params=None,
                 declarations=None,
                 inputs=None,
                 outputs=None,
                 build=None,
                 backend=None,
                 ):
        super(NotebookConfig, self).__init__(
            version=version,
            kind=kind,
            logging=logging,
            name=name,
            description=description,
            tags=tags,
            environment=environment,
            params=params,
            declarations=declarations,
            inputs=inputs,
            outputs=outputs,
            build=build
        )
        validate_notebook_backend(backend)
        self.backend = backend
