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

# pylint:disable=protected-access
from unittest.mock import patch

from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.exceptions import PolyaxonNotificationException
from polyaxon.notifiers.discord_webhook import DiscordWebHookNotifier
from tests.test_notifiers.test_webhook_notification import TestWebHookNotification


class TestDiscordWebHookNotifier(TestWebHookNotification):
    webhook = DiscordWebHookNotifier

    def test_attrs(self):
        assert self.webhook.notification_key == V1ConnectionKind.DISCORD
        assert self.webhook.name == "Discord WebHook"

    def test_prepare(self):
        with self.assertRaises(PolyaxonNotificationException):
            self.webhook._prepare(None)
        with self.assertRaises(PolyaxonNotificationException):
            self.webhook._prepare({})

        context = {"content": "message"}
        assert self.webhook._prepare(context) == {
            "username": "Polyaxon",
            "avatar_url": context.get("avatar_url"),
            "tts": context.get("tts", False),
            "content": "message",
        }

    def test_execute(self):
        with self.assertRaises(PolyaxonNotificationException):
            self.webhook.execute(notification=self.notification)

        with patch("polyaxon.notifiers.webhook.safe_request") as mock_execute:
            self.webhook.execute(
                notification=self.notification,
                config={"url": "http://bar.com/webhook", "method": "GET"},
            )

        assert mock_execute.call_count == 1


del TestWebHookNotification
