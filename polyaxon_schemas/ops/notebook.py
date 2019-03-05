# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import ValidationError, fields, validates_schema

from polyaxon_schemas.ops.environments.base import EnvironmentConfig, EnvironmentSchema
from polyaxon_schemas.utils import NotebookBackend


def validate_notebook_backend(backend):
    if backend and backend not in NotebookBackend.VALUES:
        raise ValidationError('Notebook backend `{}` not supported'.format(backend))


class NotebookSchema(EnvironmentSchema):
    backend = fields.Str(allow_none=True)

    @staticmethod
    def schema_config():
        return NotebookConfig

    @validates_schema
    def validate_backend(self, data):
        validate_notebook_backend(data.get('backend'))


class NotebookConfig(EnvironmentConfig):
    """
    Environment config.

    Args:
        cluster_uuid: `str`. The cluster uuid.
        persistence: `PersistenceConfig`. The persistence config definition.
        outputs: `OutputsConfig`. The outputs config definition.
        resources: `PodResourcesConfig`. The resources config definition.
        node_selector: `dict`.
        affinity: `dict`.
        tolerations: `list(dict)`.
        backend: `str`.
    """
    IDENTIFIER = 'notebook'
    SCHEMA = NotebookSchema

    def __init__(self,
                 cluster_uuid=None,
                 persistence=None,
                 outputs=None,
                 resources=None,
                 secret_refs=None,
                 configmap_refs=None,
                 node_selector=None,
                 affinity=None,
                 tolerations=None,
                 backend=None):
        super(NotebookConfig, self).__init__(
            cluster_uuid=cluster_uuid,
            persistence=persistence,
            outputs=outputs,
            resources=resources,
            secret_refs=secret_refs,
            configmap_refs=configmap_refs,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
        )
        validate_notebook_backend(backend)
        self.backend = backend
