# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.base import NAME_REGEX, BaseConfig, BaseSchema
from polyaxon_schemas.ops.contexts import ContextsSchema
from polyaxon_schemas.ops.environments import EnvironmentSchema
from polyaxon_schemas.ops.job.replicas import OpReplicaSchema
from polyaxon_schemas.ops.parallel import ParallelSchema
from polyaxon_schemas.ops.termination import TerminationSchema
from polyaxon_schemas.polyflow.conditions import ConditionSchema
from polyaxon_schemas.polyflow.template_ref import TemplateRefSchema
from polyaxon_schemas.polyflow.trigger_policies import TriggerPolicy


class OpSchema(BaseSchema):
    version = fields.Float(allow_none=True)
    kind = fields.Str(allow_none=True, validate=validate.Equal("op"))
    template = fields.Nested(TemplateRefSchema, allow_none=True)
    name = fields.Str(validate=validate.Regexp(regex=NAME_REGEX), allow_none=True)
    description = fields.Str(allow_none=True)
    tags = fields.List(fields.Str(), allow_none=True)
    params = fields.Raw(allow_none=True)
    profile = fields.Str(allow_none=True)
    environment = fields.Nested(EnvironmentSchema, allow_none=True)
    termination = fields.Nested(TerminationSchema, allow_none=True)
    contexts = fields.Nested(ContextsSchema, allow_none=True)
    replica_spec = fields.Dict(
        keys=fields.Str(), values=fields.Nested(OpReplicaSchema), allow_none=True
    )
    dependencies = fields.List(fields.Str(), allow_none=True)
    trigger = fields.Str(allow_none=True, validate=validate.OneOf(TriggerPolicy.VALUES))
    conditions = fields.Nested(ConditionSchema, allow_none=True)
    skip_on_upstream_skip = fields.Bool(allow_none=True)
    _template = fields.Nested("TemplateSchema", allow_none=True)

    @staticmethod
    def schema_config():
        return OpConfig


class OpConfig(BaseConfig):
    SCHEMA = OpSchema
    IDENTIFIER = "op"
    REDUCED_ATTRIBUTES = [
        "version",
        "kind",
        "template",
        "name",
        "description",
        "tags",
        "profile",
        "params",
        "environment",
        "termination",
        "contexts",
        "replica_spec",
        "dependencies",
        "trigger",
        "conditions",
        "skip_on_upstream_skip",
        "_template",
    ]

    def __init__(
        self,
        version=None,
        kind=None,
        template=None,
        name=None,
        description=None,
        tags=None,
        profile=None,
        params=None,
        environment=None,
        termination=None,
        contexts=None,
        replica_spec=None,
        build=None,
        dependencies=None,
        trigger=None,
        conditions=None,
        skip_on_upstream_skip=None,
        _template=None,
    ):
        self.version = version
        self.kind = kind
        self.template = template
        self.name = name
        self.description = description
        self.tags = tags
        self.profile = profile
        self.environment = environment
        self.termination = termination
        self.contexts = contexts
        self.replica_spec = replica_spec
        self.params = params
        self.build = build
        self.dependencies = dependencies
        self.trigger = trigger
        self.conditions = conditions
        self.skip_on_upstream_skip = skip_on_upstream_skip
        self._template = _template
