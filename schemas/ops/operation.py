# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from schemas.base import NAME_REGEX, BaseConfig, BaseSchema
from schemas.fields.ref_or_obj import RefOrObject
from schemas.ops.init import InitSchema
from schemas.ops.mounts import MountsSchema
from schemas.ops.environments import EnvironmentSchema
from schemas.ops.io import IOSchema
from schemas.ops.parallel import ParallelSchema
from schemas.ops.termination import TerminationSchema


class BaseOpSchema(BaseSchema):
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
    parallel = fields.Nested(ParallelSchema, allow_none=True)
    inputs = fields.Nested(IOSchema, allow_none=True, many=True)
    outputs = fields.Nested(IOSchema, allow_none=True, many=True)

    @staticmethod
    def schema_config():
        return BaseOpConfig


class BaseOpConfig(BaseConfig):
    SCHEMA = BaseOpSchema
    IDENTIFIER = "operation"
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
        "mounts",
        "parallel",
        "inputs",
        "outputs",
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
        parallel=None,
        inputs=None,
        outputs=None,
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
        self.parallel = parallel
        self.inputs = inputs
        self.outputs = outputs
