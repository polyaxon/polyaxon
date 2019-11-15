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

from marshmallow import fields

from polyaxon.schemas.base import BaseConfig, BaseSchema


class IntervalsSchema(BaseSchema):
    runsScheduler = fields.Int(default=None)
    operationsDefaultRetryDelay = fields.Int(default=None)
    operationsMaxRetryDelay = fields.Int(default=None)

    @staticmethod
    def schema_config():
        return IntervalsConfig


class IntervalsConfig(BaseConfig):
    SCHEMA = IntervalsSchema
    REDUCED_ATTRIBUTES = [
        "runsScheduler",
        "operationsDefaultRetryDelay",
        "operationsMaxRetryDelay",
    ]

    def __init__(
        self,  # noqa
        runsScheduler=None,
        operationsDefaultRetryDelay=None,
        operationsMaxRetryDelay=None,
    ):
        self.runsScheduler = runsScheduler
        self.operationsDefaultRetryDelay = operationsDefaultRetryDelay
        self.operationsMaxRetryDelay = operationsMaxRetryDelay
