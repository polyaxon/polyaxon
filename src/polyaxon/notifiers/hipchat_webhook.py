#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
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
from polyaxon.notifiers.keys import INTEGRATIONS_WEBHOOKS_HIPCHAT
from polyaxon.notifiers.spec import NotificationSpec
from polyaxon.notifiers.webhook import WebHookNotifier


class HipChatWebHookNotifier(WebHookNotifier):
    notification_key = V1ConnectionKind.HIPCHAT
    name = "HipChat WebHook"
    description = "HipChat webhooks to send payload to a hipchat room."
    raise_empty_context = True
    config_key = INTEGRATIONS_WEBHOOKS_HIPCHAT

    @classmethod
    def serialize_notification_to_context(cls, notification: NotificationSpec) -> Dict:
        payload = {
            "message": notification.get_details(),
            "message_format": "text",
            "color": notification.get_color(),
            "from": "Polyaxon",
        }

        return payload

    @classmethod
    def _prepare(cls, context: Dict) -> Dict:
        context = super()._prepare(context)

        return {
            "message": context.get("message"),
            "message_format": context.get("message_format", "html"),
            "color": context.get("color"),
            "from": context.get("from", "Polyaxon"),
            "attach_to": context.get("attach_to"),
            "notify": context.get("notify", False),
            "card": context.get("card"),
        }
