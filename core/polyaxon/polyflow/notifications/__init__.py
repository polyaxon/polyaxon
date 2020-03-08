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

import polyaxon_sdk

from marshmallow import fields, validate

from polyaxon.schemas.base import BaseCamelSchema, BaseConfig


class V1NotificationTrigger(polyaxon_sdk.NotificationTrigger):
    VALUES = {
        polyaxon_sdk.NotificationTrigger.SUCCEEDED,
        polyaxon_sdk.NotificationTrigger.FAILED,
        polyaxon_sdk.NotificationTrigger.STOPPED,
        polyaxon_sdk.NotificationTrigger.DONE,
    }


class NotificationSchema(BaseCamelSchema):
    connection = fields.Str(required=True)
    trigger = fields.Str(
        allow_none=True, validate=validate.OneOf(V1NotificationTrigger.VALUES)
    )

    @staticmethod
    def schema_config():
        return V1Notification


class V1Notification(BaseConfig, polyaxon_sdk.V1Notification):
    IDENTIFIER = "notification"
    SCHEMA = NotificationSchema
    REDUCED_ATTRIBUTES = [
        "connection",
        "trigger",
    ]

    def to_operator_notation(self):
        return {"connection": self.connection, "trigger": self.trigger.capitalize()}
