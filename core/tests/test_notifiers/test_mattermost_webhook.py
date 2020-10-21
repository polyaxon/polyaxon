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
# pylint:disable=protected-access
from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.exceptions import PolyaxonNotificationException
from polyaxon.notifiers.mattermost_webhook import MattermostWebHookNotifier
from tests.test_notifiers.test_webhook_notification import TestWebHookNotification


class TestMattermostWebHookNotifier(TestWebHookNotification):
    webhook = MattermostWebHookNotifier

    def test_attrs(self):
        assert self.webhook.notification_key == V1ConnectionKind.MATTERMOST
        assert self.webhook.name == "Mattermost WebHook"

    def test_validate_config(self):
        assert self.webhook._validate_config(
            {
                "url": "http://mattermost.com/webhook/foo",
                "method": "post",
                "channel": "foo",
            }
        ) == [
            {
                "url": "http://mattermost.com/webhook/foo",
                "method": "POST",
                "channel": "foo",
            }
        ]

        assert self.webhook._validate_config(
            [
                {
                    "url": "http://mattermost.com/webhook/foo",
                    "method": "post",
                    "channel": "foo",
                },
                {"url": "http://mattermost.com/webhook/bar", "method": "GET"},
            ]
        ) == [
            {
                "url": "http://mattermost.com/webhook/foo",
                "method": "POST",
                "channel": "foo",
            },
            {"url": "http://mattermost.com/webhook/bar", "method": "GET"},
        ]

    def test_get_config(self):
        assert self.webhook.get_config(
            {"url": "http://foo.com/webhook", "method": "post", "channel": "foo"}
        ) == [{"url": "http://foo.com/webhook", "method": "POST", "channel": "foo"}]
        assert self.webhook.get_config(
            [
                {"url": "http://foo.com/webhook", "method": "post", "channel": "foo"},
                {"url": "http://bar.com/webhook", "method": "GET", "channel": "bar"},
            ]
        ) == [
            {"url": "http://foo.com/webhook", "method": "POST", "channel": "foo"},
            {"url": "http://bar.com/webhook", "method": "GET", "channel": "bar"},
        ]

    def test_prepare(self):
        with self.assertRaises(PolyaxonNotificationException):
            self.webhook._prepare(None)
        with self.assertRaises(PolyaxonNotificationException):
            self.webhook._prepare({})

        context = {"title": "title", "text": "text"}
        assert self.webhook._prepare(context) == {
            "attachments": [
                {
                    "pretext": context.get("pretext"),
                    "title": context.get("title"),
                    "text": context.get("text"),
                    "color": context.get("color"),
                    "fields": None,
                    "author_name": "Polyaxon",
                    "author_link": "https://polyaxon.com",
                    "author_icon": None,
                }
            ]
        }


del TestWebHookNotification
