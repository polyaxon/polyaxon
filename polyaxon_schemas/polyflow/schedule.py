# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields, validate

from polyaxon_schemas.base import BaseConfig, BaseOneOfSchema, BaseSchema


class IntervalScheduleSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal('interval'))
    start_at = fields.LocalDateTime(required=True)
    end_at = fields.LocalDateTime(allow_none=True)
    frequency = fields.Int(precision="microseconds", required=True)
    depends_on_past = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return IntervalScheduleConfig


class IntervalScheduleConfig(BaseConfig):
    SCHEMA = IntervalScheduleSchema
    IDENTIFIER = 'interval'

    def __init__(self, frequency, start_at, end_at=None, depends_on_past=None, kind=None):
        self.frequency = frequency
        self.start_at = start_at
        self.end_at = end_at
        self.depends_on_past = depends_on_past
        self.kind = kind


class CronScheduleSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal('cron'))
    start_at = fields.LocalDateTime(allow_none=True)
    end_at = fields.LocalDateTime(allow_none=True)
    cron = fields.String(required=True)
    depends_on_past = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return CronScheduleConfig


class CronScheduleConfig(BaseConfig):
    SCHEMA = CronScheduleSchema
    IDENTIFIER = 'cron'

    def __init__(self, cron, start_at=None, end_at=None, depends_on_past=None, kind=None):
        self.cron = cron
        self.start_at = start_at
        self.end_at = end_at
        self.depends_on_past = depends_on_past
        self.kind = kind


class ScheduleSchema(BaseOneOfSchema):
    TYPE_FIELD = 'kind'
    TYPE_FIELD_REMOVE = False
    SCHEMAS = {
        IntervalScheduleConfig.IDENTIFIER: IntervalScheduleSchema,
        CronScheduleConfig.IDENTIFIER: CronScheduleSchema,
    }
