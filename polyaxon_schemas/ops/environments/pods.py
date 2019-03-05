# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.ops.environments.resources import PodResourcesSchema


class PodEnvironmentSchema(BaseSchema):
    # To indicate which worker/ps index this session config belongs to
    index = fields.Int(allow_none=True)
    resources = fields.Nested(PodResourcesSchema, allow_none=True)
    node_selector = fields.Dict(allow_none=True)
    affinity = fields.Dict(allow_none=True)
    tolerations = fields.List(fields.Dict(), allow_none=True)

    @staticmethod
    def schema_config():
        return PodEnvironmentConfig


class PodEnvironmentConfig(BaseConfig):
    """
    Pod environment config.

    Args:
        index: `int | None`. The index of the pod.
        resources: `PodResourcesConfig`.
        node_selector: `dict`.
        affinity: `dict`.
        tolerations: `list(dict)`.
    """
    IDENTIFIER = 'pod_environment'
    SCHEMA = PodEnvironmentSchema
    REDUCED_ATTRIBUTES = ['index', 'resources', 'node_selector', 'affinity', 'tolerations']

    def __init__(self,
                 index=None,
                 resources=None,
                 node_selector=None,
                 affinity=None,
                 tolerations=None,
                 ):
        self.index = index
        self.resources = resources
        self.node_selector = node_selector
        self.affinity = affinity
        self.tolerations = tolerations
