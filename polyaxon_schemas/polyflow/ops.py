# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.base import NAME_REGEX, BaseConfig, BaseSchema
from polyaxon_schemas.ops.build_job import BuildSchema
from polyaxon_schemas.ops.experiment.environment import ExperimentEnvironmentSchema
from polyaxon_schemas.ops.logging import LoggingSchema
from polyaxon_schemas.polyflow.conditions import ConditionSchema
from polyaxon_schemas.polyflow.template_ref import TemplateRefSchema
from polyaxon_schemas.polyflow.trigger_policies import TriggerPolicy


class OpSchema(BaseSchema):
    version = fields.Int(allow_none=True)
    kind = fields.Str(allow_none=True)
    template = fields.Nested(TemplateRefSchema, allow_none=True)
    logging = fields.Nested(LoggingSchema, allow_none=True)
    name = fields.Str(validate=validate.Regexp(regex=NAME_REGEX), allow_none=True)
    description = fields.Str(allow_none=True)
    tags = fields.List(fields.Str(), allow_none=True)
    params = fields.Raw(allow_none=True)
    environment = fields.Nested(ExperimentEnvironmentSchema, allow_none=True)
    build = fields.Nested(BuildSchema, allow_none=True)
    concurrency = fields.Int(allow_none=True)
    dependencies = fields.List(fields.Str(), allow_none=True)
    trigger = fields.Str(allow_none=True, validate=validate.OneOf(TriggerPolicy.VALUES))
    conditions = fields.Nested(ConditionSchema, allow_none=True)
    max_retries = fields.Int(allow_none=True)
    retry_delay = fields.Int(allow_none=True)
    retry_exp_backoff = fields.Bool(allow_none=True)
    max_retry_delay = fields.Int(allow_none=True)
    skip_on_upstream_skip = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return OpConfig


class OpConfig(BaseConfig):
    SCHEMA = OpSchema
    IDENTIFIER = 'op'
    REDUCED_ATTRIBUTES = [
        'version',
        'kind',
        'template',
        'logging',
        'name',
        'description',
        'tags',
        'params',
        'environment',
        'build',
        'concurrency',
        'dependencies',
        'trigger',
        'conditions',
        'max_retries',
        'retry_delay',
        'retry_exp_backoff',
        'max_retry_delay',
        'skip_on_upstream_skip',
    ]

    def __init__(self,
                 version=None,
                 kind=None,
                 template=None,
                 logging=None,
                 name=None,
                 description=None,
                 tags=None,
                 params=None,
                 environment=None,
                 build=None,
                 concurrency=None,
                 dependencies=None,
                 trigger=None,
                 conditions=None,
                 max_retries=None,
                 retry_delay=None,
                 retry_exp_backoff=None,
                 max_retry_delay=None,
                 skip_on_upstream_skip=None):
        self.version = version
        self.kind = kind
        self.template = template
        self.logging = logging
        self.name = name
        self.description = description
        self.tags = tags
        self.environment = environment
        self.params = params
        self.build = build
        self.concurrency = concurrency
        self.dependencies = dependencies
        self.trigger = trigger
        self.conditions = conditions
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.retry_exp_backoff = retry_exp_backoff
        self.max_retry_delay = max_retry_delay
        self.skip_on_upstream_skip = skip_on_upstream_skip
