# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.flows.conds import CondSchema
from polyaxon_schemas.flows.deps import DepSchema
from polyaxon_schemas.flows.executable import ExecutableConfig, ExecutableSchema
from polyaxon_schemas.flows.inputs import InputSchema
from polyaxon_schemas.flows.trigger_policies import TriggerPolicy


class BaseOpSchema(ExecutableSchema):
    concurrency = fields.Int(allow_none=True)
    deps = fields.Nested(DepSchema, allow_none=True, many=True)
    inputs = fields.Nested(InputSchema, allow_none=True, many=True)
    trigger = fields.Str(allow_none=True, validate=validate.OneOf(TriggerPolicy.VALUES))
    conds = fields.Nested(CondSchema, allow_none=None)
    max_retries = fields.Int(allow_none=True)
    retry_delay = fields.Int(allow_none=True)
    retry_exponential_backoff = fields.Bool(allow_none=True)
    max_retry_delay = fields.Int(allow_none=True)
    skip_on_upstream_skip = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return BaseOpConfig


class BaseOpConfig(ExecutableConfig):
    SCHEMA = BaseOpSchema
    IDENTIFIER = 'operation'
    REDUCED_ATTRIBUTES = []

    def __init__(self,
                 concurrency=None,
                 deps=None,
                 inputs=None,
                 trigger=None,
                 conds=None,
                 max_retries=None,
                 retry_delay=None,
                 retry_exponential_backoff=None,
                 max_retry_delay=None,
                 skip_on_upstream_skip=None,
                 execute_at=None,
                 timeout=None):
        super(BaseOpConfig, self).__init__(execute_at=execute_at, timeout=timeout)
        self.concurrency = concurrency
        self.deps = deps
        self.inputs = inputs
        self.trigger = trigger
        self.conds = conds
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.retry_exponential_backoff = retry_exponential_backoff
        self.max_retry_delay = max_retry_delay
        self.skip_on_upstream_skip = skip_on_upstream_skip
