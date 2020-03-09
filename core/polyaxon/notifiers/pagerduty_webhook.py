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

from typing import Dict

from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.notifiers.keys import INTEGRATIONS_WEBHOOKS_PAGER_DUTY
from polyaxon.notifiers.spec import NotificationSpec
from polyaxon.notifiers.webhook import WebHookNotifier


class PagerDutyWebHookNotifier(WebHookNotifier):
    notification_key = V1ConnectionKind.PAGER_DUTY
    name = "PagerDuty WebHook"
    description = "PagerDuty webhooks to send event payload to pagerduty."
    raise_empty_context = True
    config_key = INTEGRATIONS_WEBHOOKS_PAGER_DUTY
    validate_keys = ["service_key"]

    @classmethod
    def serialize_notification_to_context(cls, notification: NotificationSpec) -> Dict:
        payload = {
            "event_type": notification.get_title(),
            "description": notification.condition.reason,
            "details": notification.get_details(),
            "incident_key": "trigger",
            "client": "polyaxon",
            "client_url": cls.get_url(),
            "contexts": [],
        }

        return payload

    @classmethod
    def _prepare(cls, context: Dict) -> Dict:
        context = super()._prepare(context)

        return {
            "event_type": context.get("event_type"),
            "description": context.get("description"),
            "details": context.get("details"),
            "incident_key": context.get("incident_key"),
            "client": context.get("client", "Polyaxon"),
            "client_url": context.get("client_url", "https://polyaxon.com"),
            "contexts": context.get("contexts"),
        }

    @classmethod
    def _pre_execute_web_hook(cls, data: Dict, config: Dict) -> Dict:
        service_key = config.get("service_key")
        if service_key:
            data["service_key"] = service_key

        return data
