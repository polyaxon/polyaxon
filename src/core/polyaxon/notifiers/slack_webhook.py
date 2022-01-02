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
from polyaxon.notifiers.keys import INTEGRATIONS_WEBHOOKS_SLACK
from polyaxon.notifiers.spec import NotificationSpec
from polyaxon.notifiers.webhook import WebHookNotifier
from polyaxon.utils.date_utils import to_timestamp


class SlackWebHookNotifier(WebHookNotifier):
    notification_key = V1ConnectionKind.SLACK
    name = "Slack WebHook"
    description = "Slack webhooks to send payload to Slack Incoming Webhooks."
    raise_empty_context = True
    config_key = INTEGRATIONS_WEBHOOKS_SLACK
    validate_keys = ["channel", "icon_url"]

    @classmethod
    def serialize_notification_to_context(cls, notification: NotificationSpec) -> Dict:
        logo_url = "https://cdn.polyaxon.com/static/v1/images/logo_small.png"
        fields = []  # Use build_field

        payload = {
            "fallback": notification.condition.type,
            "title": notification.get_title(),
            "title_link": cls.get_url(notification),
            "text": notification.get_details(),
            "fields": fields,
            "mrkdwn_in": ["text"],
            "footer_icon": logo_url,
            "footer": "Polyaxon",
            "color": notification.get_color(),
            "ts": to_timestamp(notification.condition.last_transition_time),
        }

        return payload

    @classmethod
    def _prepare(cls, context):
        context = super()._prepare(context)

        data = {
            "fallback": context.get("fallback"),
            "title": context.get("title"),
            "title_link": context.get("title_link"),
            "text": context.get("text"),
            "fields": context.get("fields"),
            "mrkdwn_in": context.get("mrkdwn_in"),
            "footer_icon": context.get("footer_icon"),
            "footer": context.get("footer", "Polyaxon"),
            "color": context.get("color"),
        }
        return {"attachments": [data]}

    @classmethod
    def _pre_execute_web_hook(cls, data, config):
        channel = config.get("channel")
        icon_url = config.get("channel")
        if channel:
            data["channel"] = channel

        if icon_url:
            data["icon_url"] = icon_url

        return data
