#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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
import os

from datetime import timedelta

from marshmallow import fields

from polyaxon.env_vars.keys import POLYAXON_KEYS_INTERVALS_COMPATIBILITY_CHECK
from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.utils.tz_utils import now


class ChecksSchema(BaseSchema):
    last_check = fields.DateTime(allow_none=True)

    @staticmethod
    def schema_config():
        return ChecksConfig


class ChecksConfig(BaseConfig):
    SCHEMA = ChecksSchema
    IDENTIFIER = "checks"
    INTERVAL = 30 * 60

    def __init__(
        self, last_check=None,
    ):
        self.last_check = self.get_last_check(last_check)

    def get_interval(self, interval: int = None):
        if interval is not None:
            return interval
        interval = int(
            os.environ.get(POLYAXON_KEYS_INTERVALS_COMPATIBILITY_CHECK, self.INTERVAL)
        )
        if interval == -1:
            return interval
        return max(interval, self.INTERVAL)

    @classmethod
    def get_last_check(cls, last_check):
        return last_check or now() - timedelta(cls.INTERVAL)

    def should_check(self, interval: int = None):
        interval = self.get_interval(interval=interval)
        if interval == -1:
            return False
        if (now() - self.last_check).total_seconds() > interval:
            return True
        return False
