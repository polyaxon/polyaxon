# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.ops.container import ContainerSchema
from polyaxon_schemas.ops.job.replicas import JobReplicaSchema
from polyaxon_schemas.ops.operation import BaseOpConfig, BaseOpSchema


class JobSchema(BaseOpSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("job"))
    container = fields.Nested(ContainerSchema)
    replica_spec = fields.Dict(
        keys=fields.Str(), values=fields.Nested(JobReplicaSchema), allow_none=True
    )

    @staticmethod
    def schema_config():
        return JobConfig


class JobConfig(BaseOpConfig):
    SCHEMA = JobSchema
    IDENTIFIER = "job"
    REDUCED_ATTRIBUTES = BaseOpConfig.REDUCED_ATTRIBUTES + ["replica_spec"]

    def __init__(
        self,
        container,
        version=None,
        kind=None,
        name=None,
        description=None,
        tags=None,
        profile=None,
        environment=None,
        termination=None,
        contexts=None,
        inputs=None,
        outputs=None,
        parallel=None,
        replica_spec=None,
    ):
        super(JobConfig, self).__init__(
            version=version,
            kind=kind,
            name=name,
            description=description,
            tags=tags,
            profile=profile,
            environment=environment,
            termination=termination,
            contexts=contexts,
            parallel=parallel,
            inputs=inputs,
            outputs=outputs,
        )

        self.container = container
        self.replica_spec = replica_spec
