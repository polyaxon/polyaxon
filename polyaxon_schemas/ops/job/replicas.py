# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseSchema, BaseConfig
from polyaxon_schemas.ops.container import ContainerSchema
from polyaxon_schemas.ops.contexts import ContextsSchema
from polyaxon_schemas.ops.environments import EnvironmentSchema
from polyaxon_schemas.ops.termination import TerminationSchema


class OpReplicaSchema(BaseSchema):
    replicas = fields.Int(allow_none=True)
    environment = fields.Nested(EnvironmentSchema, allow_none=True)
    termination = fields.Nested(TerminationSchema, allow_none=True)
    contexts = fields.Nested(ContextsSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return OpReplicaConfig


class OpReplicaConfig(BaseConfig):
    SCHEMA = OpReplicaSchema
    IDENTIFIER = "replica"
    REDUCED_ATTRIBUTES = ["replicas", "environment", "termination", "contexts"]

    def __init__(self, replicas=None, environment=None, termination=None, refs=None):
        self.replicas = replicas
        self.environment = environment
        self.termination = termination
        self.refs = refs


class JobReplicaSchema(BaseSchema):
    replicas = fields.Int(allow_none=True)
    environment = fields.Nested(EnvironmentSchema, allow_none=True)
    termination = fields.Nested(TerminationSchema, allow_none=True)
    contexts = fields.Nested(ContextsSchema, allow_none=True)
    container = fields.Nested(ContainerSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return JobReplicaConfig


class JobReplicaConfig(BaseConfig):
    SCHEMA = JobReplicaSchema
    IDENTIFIER = "replica"
    REDUCED_ATTRIBUTES = [
        "replicas",
        "environment",
        "termination",
        "contexts",
        "container",
    ]

    def __init__(
        self,
        replicas=None,
        environment=None,
        termination=None,
        refs=None,
        container=None,
    ):
        self.replicas = replicas
        self.environment = environment
        self.termination = termination
        self.refs = refs
        self.container = container
