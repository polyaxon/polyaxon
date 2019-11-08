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

# coding: utf-8
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon.schemas.base import NAME_REGEX, BaseConfig, BaseSchema
from polyaxon.schemas.fields.ref_or_obj import RefOrObject
from polyaxon.schemas.polyflow.container import ContainerSchema
from polyaxon.schemas.polyflow.environments import EnvironmentSchema
from polyaxon.schemas.polyflow.init import InitSchema
from polyaxon.schemas.polyflow.io import IOSchema
from polyaxon.schemas.polyflow.mounts import MountsSchema
from polyaxon.schemas.polyflow.recursive import RecursiveSchema
from polyaxon.schemas.polyflow.schedules import ScheduleSchema
from polyaxon.schemas.polyflow.service import ServiceSchema
from polyaxon.schemas.polyflow.termination import TerminationSchema
from polyaxon.schemas.polyflow.workflows import WorkflowSchema


class BaseComponentSchema(BaseSchema):
    version = fields.Float(allow_none=True)
    kind = fields.Str(allow_none=True)
    name = fields.Str(validate=validate.Regexp(regex=NAME_REGEX), allow_none=True)
    description = fields.Str(allow_none=True)
    tags = fields.List(fields.Str(), allow_none=True)
    profile = fields.Str(allow_none=True)
    nocache = RefOrObject(fields.Boolean(allow_none=True))
    environment = fields.Nested(EnvironmentSchema, allow_none=True)
    termination = fields.Nested(TerminationSchema, allow_none=True)
    init = fields.Nested(InitSchema, allow_none=True)
    mounts = fields.Nested(MountsSchema, allow_none=True)
    schedule = fields.Nested(ScheduleSchema, allow_none=True)
    recursive = fields.Nested(RecursiveSchema, allow_none=True)
    workflow = fields.Nested(WorkflowSchema, allow_none=True)
    service = fields.Nested(ServiceSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return BaseComponentConfig


class BaseComponentConfig(BaseConfig):
    SCHEMA = BaseComponentSchema
    REDUCED_ATTRIBUTES = [
        "version",
        "kind",
        "name",
        "description",
        "tags",
        "profile",
        "nocache",
        "environment",
        "termination",
        "init",
        "schedule",
        "mounts",
        "workflow",
        "recursive",
        "service",
    ]

    def __init__(
        self,
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
        schedule=None,
        workflow=None,
        recursive=None,
        service=None,
    ):
        self.version = version
        self.kind = kind
        self.name = name
        self.description = description
        self.tags = tags
        self.profile = profile
        self.nocache = nocache
        self.environment = environment
        self.termination = termination
        self.init = init
        self.mounts = mounts
        self.schedule = schedule
        self.workflow = workflow
        self.recursive = recursive
        self.service = service
