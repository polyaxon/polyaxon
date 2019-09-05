# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.base import BaseOneOfSchema
from polyaxon_schemas.ops.job import JobConfig, JobSchema
from polyaxon_schemas.ops.service import ServiceConfig, ServiceSchema


class TemplateSchema(BaseOneOfSchema):
    TYPE_FIELD = "kind"
    TYPE_FIELD_REMOVE = False
    SCHEMAS = {JobConfig.IDENTIFIER: JobSchema, ServiceConfig.IDENTIFIER: ServiceSchema}
