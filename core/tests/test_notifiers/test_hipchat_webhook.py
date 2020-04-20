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
from tests.test_notifiers.test_webhook_notification import TestWebHookNotification

from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.exceptions import PolyaxonNotificationException
from polyaxon.notifiers.hipchat_webhook import HipChatWebHookNotifier


class TestHipChatWebHookNotifier(TestWebHookNotification):
    webhook = HipChatWebHookNotifier

    def test_attrs(self):
        assert self.webhook.notification_key == V1ConnectionKind.HIPCHAT
        assert self.webhook.name == "HipChat WebHook"

    def test_prepare(self):
        with self.assertRaises(PolyaxonNotificationException):
            self.webhook._prepare(None)
        with self.assertRaises(PolyaxonNotificationException):
            self.webhook._prepare({})

        context = {"message": "message"}
        assert self.webhook._prepare(context) == {
            "message": context.get("message"),
            "message_format": context.get("message_format", "html"),
            "color": context.get("color"),
            "from": "Polyaxon",
            "attach_to": context.get("attach_to"),
            "notify": context.get("notify", False),
            "card": context.get("card"),
        }


del TestWebHookNotification
