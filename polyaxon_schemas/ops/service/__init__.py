# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.ops.container import ContainerSchema
from polyaxon_schemas.ops.operation import BaseOpConfig, BaseOpSchema
from polyaxon_schemas.ops.service.validation import ServiceLevelSchema


class ServiceSchema(BaseOpSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("service"))
    container = fields.Nested(ContainerSchema, allow_none=True)
    ports = fields.List(
        fields.Int(allow_none=True),
        validate=validate.Length(min=1, max=2),
        allow_none=True,
    )

    @staticmethod
    def schema_config():
        return ServiceConfig


class ServiceConfig(BaseOpConfig):
    IDENTIFIER = "service"
    SCHEMA = ServiceSchema
    REDUCED_ATTRIBUTES = BaseOpConfig.REDUCED_ATTRIBUTES + ["container", "ports"]

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
        parallel=None,
        container=None,
        ports=None,
        inputs=None,
        outputs=None,
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
            parallel=parallel,
            inputs=inputs,
            outputs=outputs,
        )
        self.container = container
        self.ports = ports
