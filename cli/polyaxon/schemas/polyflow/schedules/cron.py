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

from polyaxon.schemas.base import BaseConfig, BaseSchema


class CronScheduleSchema(BaseSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal("cron"))
    start_at = fields.LocalDateTime(allow_none=True)
    end_at = fields.LocalDateTime(allow_none=True)
    cron = fields.String(required=True)
    depends_on_past = fields.Bool(allow_none=True)

    @staticmethod
    def schema_config():
        return CronScheduleConfig


class CronScheduleConfig(BaseConfig):
    SCHEMA = CronScheduleSchema
    IDENTIFIER = "cron"

    def __init__(
        self, cron, start_at=None, end_at=None, depends_on_past=None, kind=IDENTIFIER
    ):
        self.cron = cron
        self.start_at = start_at
        self.end_at = end_at
        self.depends_on_past = depends_on_past
        self.kind = kind
