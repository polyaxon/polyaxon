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
import uuid

from unittest.mock import patch

from polyaxon_sdk import V1StatusCondition
from tests.utils import BaseTestCase

from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.exceptions import PolyaxonNotificationException
from polyaxon.lifecycle import V1Statuses
from polyaxon.notifiers.spec import NotificationSpec
from polyaxon.notifiers.webhook import WebHookNotifier
from polyaxon.utils.tz_utils import now


class TestWebHookNotification(BaseTestCase):
    webhook = WebHookNotifier

    def setUp(self):
        super().setUp()
        self.notification = NotificationSpec(
            kind=self.webhook.notification_key,
            owner="onwer",
            project="project",
            uuid=uuid.uuid4().hex,
            name="test",
            condition=V1StatusCondition(
                type=V1Statuses.FAILED,
                reason="reason",
                message="message",
                last_update_time=now(),
                last_transition_time=now(),
            ),
        )

    def test_attrs(self):
        assert self.webhook.notification_key == V1ConnectionKind.WEBHOOK
        assert self.webhook.name == "WebHook"

    def test_validate_empty_config(self):
        assert self.webhook._validate_config({}) == []
        assert self.webhook._validate_config([]) == []
        assert self.webhook._validate_config({"foo": "bar"}) == []

    def test_validate_config_raises_for_wrong_configs(self):
        with self.assertRaises(PolyaxonNotificationException):
            self.webhook._validate_config({"url": "bar"})

        with self.assertRaises(PolyaxonNotificationException):
            self.webhook._validate_config(
                {"url": "http://foo.com/webhook", "method": 1}
            )

        with self.assertRaises(PolyaxonNotificationException):
            self.webhook._validate_config(
                {"url": "http://foo.com/webhook", "method": "foo"}
            )

    def test_validate_config(self):
        assert self.webhook._validate_config(
            {"url": "http://foo.com/webhook", "method": "post"}
        ) == [{"url": "http://foo.com/webhook", "method": "POST"}]

        assert self.webhook._validate_config(
            [
                {"url": "http://foo.com/webhook", "method": "post"},
                {"url": "http://bar.com/webhook", "method": "GET"},
            ]
        ) == [
            {"url": "http://foo.com/webhook", "method": "POST"},
            {"url": "http://bar.com/webhook", "method": "GET"},
        ]

    def test_get_empty_config(self):
        with self.assertRaises(PolyaxonNotificationException):
            self.webhook.get_config()
        with self.assertRaises(PolyaxonNotificationException):
            self.webhook.get_config({})
        assert self.webhook.get_config({"foo": "bar"}) == []

    def test_get_config(self):
        assert self.webhook.get_config(
            {"url": "http://foo.com/webhook", "method": "post"}
        ) == [{"url": "http://foo.com/webhook", "method": "POST"}]
        assert self.webhook.get_config(
            [
                {"url": "http://foo.com/webhook", "method": "post"},
                {"url": "http://bar.com/webhook", "method": "GET"},
            ]
        ) == [
            {"url": "http://foo.com/webhook", "method": "POST"},
            {"url": "http://bar.com/webhook", "method": "GET"},
        ]

    def test_prepare(self):
        assert self.webhook._prepare(None) is None
        assert self.webhook._prepare({}) == {}
        assert self.webhook._prepare({"foo": "bar"}) == {"foo": "bar"}

    def test_execute_empty_payload(self):
        with self.assertRaises(PolyaxonNotificationException):
            self.webhook.execute(notification=self.notification)

    def test_execute_empty_payload_with_config(self):
        with self.assertRaises(PolyaxonNotificationException):
            self.webhook.execute(
                notification=None,
                config={"url": "http://bar.com/webhook", "method": "GET"},
            )

    def test_execute_payload_with_config(self):
        with patch("polyaxon.notifiers.webhook.safe_request") as mock_execute:
            self.webhook.execute(
                notification=self.notification,
                config={"url": "http://bar.com/webhook", "method": "GET"},
            )

        assert mock_execute.call_count == 1

    def test_execute(self):
        with self.assertRaises(PolyaxonNotificationException):
            self.webhook.execute(notification=self.notification)

        with patch("polyaxon.notifiers.webhook.safe_request") as mock_execute:
            self.webhook.execute(
                notification=self.notification,
                config={"url": "http://bar.com/webhook", "method": "GET"},
            )

        assert mock_execute.call_count == 1
