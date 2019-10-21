# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon.schemas.fields.ref_or_obj import RefOrObject
from polyaxon.schemas.ops.container import ContainerSchema
from polyaxon.schemas.ops.operation import BaseOpConfig, BaseOpSchema
from polyaxon.schemas.ops.service.validation import ServiceLevelSchema


class ServiceSchema(BaseOpSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("service"))
    container = fields.Nested(ContainerSchema)
    ports = RefOrObject(
        fields.List(
            fields.Int(allow_none=True),
            validate=validate.Length(min=1, max=2),
            allow_none=True,
        )
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
        parallel=None,
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
        self.ports = ports
