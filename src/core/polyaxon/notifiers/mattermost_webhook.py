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
from polyaxon.notifiers.keys import INTEGRATIONS_WEBHOOKS_MATTERMOST
from polyaxon.notifiers.spec import NotificationSpec
from polyaxon.notifiers.webhook import WebHookNotifier


class MattermostWebHookNotifier(WebHookNotifier):
    notification_key = V1ConnectionKind.MATTERMOST
    name = "Mattermost WebHook"
    description = "Mattermost webhooks to send payload to a Mattermost channel."
    raise_empty_context = True
    config_key = INTEGRATIONS_WEBHOOKS_MATTERMOST
    validate_keys = ["channel"]

    @classmethod
    def serialize_notification_to_context(cls, notification: NotificationSpec) -> Dict:
        payload = {
            "title": notification.get_title(),
            "text": notification.get_details(),
            "color": notification.get_color(),
            "fields": [],
            "author_name": "Polyaxon",
            "author_link": cls.get_url(notification),
            "author_icon": None,
        }

        return payload

    @classmethod
    def _prepare(cls, context):
        context = super()._prepare(context)

        data = {
            "pretext": context.get("pretext"),
            "title": context.get("title"),
            "text": context.get("text"),
            "color": context.get("color"),
            "fields": context.get("fields"),
            "author_name": context.get("author_name", "Polyaxon"),
            "author_link": context.get("author_link", "https://polyaxon.com"),
            "author_icon": context.get("author_icon"),
        }
        return {"attachments": [data]}

    @classmethod
    def _pre_execute_web_hook(cls, data, config):
        channel = config.get("channel")
        if channel:
            data["channel"] = channel

        return data
