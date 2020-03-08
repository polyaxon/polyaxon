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
from polyaxon.exceptions import PolyaxonNotificationException
from polyaxon.notifiers.keys import INTEGRATIONS_WEBHOOKS_DISCORD
from polyaxon.notifiers.spec import NotificationSpec
from polyaxon.notifiers.webhook import WebHookNotifier


class DiscordWebHookNotifier(WebHookNotifier):
    notification_key = V1ConnectionKind.DISCORD
    name = "Discord WebHook"
    description = "Discord webhooks to send payload to a discord room."
    raise_empty_context = True
    config_key = INTEGRATIONS_WEBHOOKS_DISCORD

    @classmethod
    def serialize_notification_to_context(cls, notification: NotificationSpec) -> Dict:
        logo_url = ""

        payload = {"content": notification.get_details(), "avatar_url": logo_url}

        return payload

    @classmethod
    def _prepare(cls, context: Dict) -> Dict:
        context = super()._prepare(context)

        payload = {
            "username": "Polyaxon",
            "avatar_url": context.get("avatar_url"),
            "tts": context.get("tts", False),
        }
        content = context.get("content")
        if content and len(content) <= 2000:
            payload["content"] = content
        else:
            raise PolyaxonNotificationException(
                "Discord content must non null and 2000 or fewer characters."
            )

        proxy = context.get("proxy")
        if proxy:
            payload["https"] = proxy
        return payload
