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


class TerminationSchema(BaseSchema):
    max_retries = fields.Int(allow_none=True)
    restart_policy = fields.Str(allow_none=True)
    ttl = fields.Int(allow_none=True)
    timeout = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return TerminationConfig


class TerminationConfig(BaseConfig):
    """
    Termination config: defines how to handle failures, job runtime, and cleanup policy.

    Args:
        max_retries: `int`.
        timeout: `dict`.
        restart_policy: `dict`.
        ttl: `list(dict)`.
    """

    IDENTIFIER = "termination"
    SCHEMA = TerminationSchema
    REDUCED_ATTRIBUTES = ["max_retries", "timeout", "restart_policy", "ttl"]

    def __init__(self, max_retries=None, timeout=None, restart_policy=None, ttl=None):
        self.max_retries = max_retries
        self.timeout = timeout
        self.restart_policy = restart_policy
        self.ttl = ttl
