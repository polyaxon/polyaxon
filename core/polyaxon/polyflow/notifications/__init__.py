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
    pass


class NotificationSchema(BaseCamelSchema):
    connections = fields.List(fields.Str(), required=True)
    trigger = fields.Str(
        allow_none=True, validate=validate.OneOf(V1NotificationTrigger.allowable_values)
    )

    @staticmethod
    def schema_config():
        return V1Notification


class V1Notification(BaseConfig, polyaxon_sdk.V1Notification):
    """You can configure Polyaxon to send notifications to users about event changes in the platform.

    Polyaxon can send notifications when a run reaches a final status:

     * succeeded
     * failed
     * stopped
     * done

     Args:
         connections: List[str]
         trigger: str

    ## YAML usage

    ```yaml
    >>> notification:
    >>>   connections: [slack-connection, discord-connection]
    >>>   trigger: failed
    ```

    ## Python usage

    ```python
    >>> from polyaxon.polyflow import V1Notification, V1NotificationTrigger
    >>> notification = V1Notification(
    >>>     connections=["slack-connection", "discord-connection"],
    >>>     trigger=V1NotificationTrigger.FAILED,
    >>> )
    ```

    ## Fields

    ### connections

    The connections to notify, these [connections](/docs/setup/connections/)
    must be configured at deployment time.

    ```yaml
    >>> notification:
    >>>   connections: [slack-connection, discord-connection]
    ```

    ### trigger

    The trigger represents the status condition to check before sending the notification.

    ```yaml
    >>> notification:
    >>>   trigger: succeeded
    ```

    In this example, the notification will be sent if the run succeeds.
    """

    IDENTIFIER = "notification"
    SCHEMA = NotificationSchema
    REDUCED_ATTRIBUTES = [
        "connections",
        "trigger",
    ]

    def to_operator(self):
        self.trigger = self.trigger.capitalize()
        return super().to_dict()
