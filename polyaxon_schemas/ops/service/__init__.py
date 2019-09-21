# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.ops.operation import BaseOpConfig, BaseOpSchema
from polyaxon_schemas.ops.service.validation import ServiceLevelSchema


class ServiceSchema(BaseOpSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("service"))
    ports = fields.List(
        fields.Int(allow_none=True),
        validate=validate.Range(min=1, max=2),
        allow_none=True,
    )

    @staticmethod
    def schema_config():
        return ServiceConfig


class ServiceConfig(BaseOpConfig):
    IDENTIFIER = "service"
    SCHEMA = ServiceSchema
    REDUCED_ATTRIBUTES = BaseOpConfig.REDUCED_ATTRIBUTES + ["ports"]

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
        inputs=None,
        outputs=None,
        ports=None,
    ):
        super(ServiceConfig, self).__init__(
            version=version,
            kind=kind,
            name=name,
            description=description,
            tags=tags,
            environment=environment,
            termination=termination,
            contexts=contexts,
            container=container,
            inputs=inputs,
            outputs=outputs,
        )
        self.ports = ports
