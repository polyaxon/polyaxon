# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.ops.job.replicas import JobReplicaSchema
from polyaxon_schemas.ops.operation import BaseOpConfig, BaseOpSchema
from polyaxon_schemas.ops.parallel import ParallelSchema


class JobSchema(BaseOpSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("job"))
    parallel = fields.Nested(ParallelSchema, allow_none=True)
    replica_spec = fields.Dict(
        keys=fields.Str(), values=fields.Nested(JobReplicaSchema), allow_none=True
    )

    @staticmethod
    def schema_config():
        return JobConfig


class JobConfig(BaseOpConfig):
    SCHEMA = JobSchema
    IDENTIFIER = "job"
    REDUCED_ATTRIBUTES = BaseOpConfig.REDUCED_ATTRIBUTES + ["parallel", "replica_spec"]

    def __init__(
        self,
        version=None,
        kind=None,
        name=None,
        description=None,
        tags=None,
        environment=None,
        termination=None,
        contexts=None,
        container=None,
        params=None,
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
            environment=environment,
            termination=termination,
            contexts=contexts,
            container=container,
            params=params,
            inputs=inputs,
            outputs=outputs,
        )

        self.parallel = parallel
        self.replica_spec = replica_spec
