# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.ops.environments.outputs import OutputsSchema
from polyaxon_schemas.ops.environments.persistence import PersistenceSchema
from polyaxon_schemas.ops.environments.pods import PodEnvironmentConfig, PodEnvironmentSchema
from polyaxon_schemas.utils import UUID


class EnvironmentSchema(PodEnvironmentSchema):
    cluster_uuid = UUID(allow_none=True)
    persistence = fields.Nested(PersistenceSchema, allow_none=True)
    outputs = fields.Nested(OutputsSchema, allow_none=True)
    secret_refs = fields.List(fields.Str(), allow_none=True)
    configmap_refs = fields.List(fields.Str(), allow_none=True)

    @staticmethod
    def schema_config():
        return EnvironmentConfig


class EnvironmentConfig(PodEnvironmentConfig):
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
    """
    IDENTIFIER = 'environment'
    SCHEMA = EnvironmentSchema

    def __init__(self,
                 cluster_uuid=None,
                 persistence=None,
                 outputs=None,
                 resources=None,
                 secret_refs=None,
                 configmap_refs=None,
                 node_selector=None,
                 affinity=None,
                 tolerations=None):
        self.cluster_uuid = cluster_uuid
        self.persistence = persistence
        self.outputs = outputs
        self.secret_refs = secret_refs
        self.configmap_refs = configmap_refs
        super(EnvironmentConfig, self).__init__(
            resources=resources,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
        )
