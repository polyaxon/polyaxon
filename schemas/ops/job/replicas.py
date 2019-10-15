# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from schemas.base import BaseConfig, BaseSchema
from schemas.ops.container import ContainerSchema
from schemas.ops.mounts import MountsSchema
from schemas.ops.environments import EnvironmentSchema
from schemas.ops.termination import TerminationSchema


class OpReplicaSchema(BaseSchema):
    replicas = fields.Int(allow_none=True)
    environment = fields.Nested(EnvironmentSchema, allow_none=True)
    termination = fields.Nested(TerminationSchema, allow_none=True)
    mounts = fields.Nested(MountsSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return OpReplicaConfig


class OpReplicaConfig(BaseConfig):
    SCHEMA = OpReplicaSchema
    IDENTIFIER = "replica"
    REDUCED_ATTRIBUTES = ["replicas", "environment", "termination", "mounts"]

    def __init__(self, replicas=None, environment=None, termination=None, mounts=None):
        self.replicas = replicas
        self.environment = environment
        self.termination = termination
        self.mounts = mounts


class JobReplicaSchema(BaseSchema):
    replicas = fields.Int(allow_none=True)
    environment = fields.Nested(EnvironmentSchema, allow_none=True)
    termination = fields.Nested(TerminationSchema, allow_none=True)
    mounts = fields.Nested(MountsSchema, allow_none=True)
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
        "mounts",
        "container",
    ]

    def __init__(
        self,
        replicas=None,
        environment=None,
        termination=None,
        mounts=None,
        container=None,
    ):
        self.replicas = replicas
        self.environment = environment
        self.termination = termination
        self.mounts = mounts
        self.container = container
