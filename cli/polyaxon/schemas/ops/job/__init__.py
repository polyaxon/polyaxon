#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon.schemas.ops.container import ContainerSchema
from polyaxon.schemas.ops.job.replicas import JobReplicaSchema
from polyaxon.schemas.ops.operation import BaseOpConfig, BaseOpSchema


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
        nocache=None,
        environment=None,
        termination=None,
        init=None,
        mounts=None,
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
            nocache=nocache,
            environment=environment,
            termination=termination,
            init=init,
            mounts=mounts,
            parallel=parallel,
            inputs=inputs,
            outputs=outputs,
        )

        self.container = container
        self.replica_spec = replica_spec
