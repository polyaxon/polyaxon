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
from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.exceptions import PolyaxonNotificationException
from polyaxon.notifiers.pagerduty_webhook import PagerDutyWebHookNotifier
from tests.test_notifiers.test_webhook_notification import TestWebHookNotification


class TestPagerDutyWebHook(TestWebHookNotification):
    webhook = PagerDutyWebHookNotifier

    def test_attrs(self):
        assert self.webhook.notification_key == V1ConnectionKind.PAGERDUTY
        assert self.webhook.name == "PagerDuty WebHook"

    def test_validate_config(self):
        assert self.webhook._validate_config(
            {
                "url": "http://pagerduty.com/webhook/foo",
                "method": "post",
                "service_key": "foo",
            }
        ) == [
            {
                "url": "http://pagerduty.com/webhook/foo",
                "method": "POST",
                "service_key": "foo",
            }
        ]

        assert self.webhook._validate_config(
            [
                {
                    "url": "http://pagerduty.com/webhook/foo",
                    "method": "post",
                    "service_key": "foo",
                },
                {"url": "http://pagerduty.com/webhook/bar", "method": "GET"},
            ]
        ) == [
            {
                "url": "http://pagerduty.com/webhook/foo",
                "method": "POST",
                "service_key": "foo",
            },
            {"url": "http://pagerduty.com/webhook/bar", "method": "GET"},
        ]

    def test_get_config(self):
        assert self.webhook.get_config(
            {"url": "http://foo.com/webhook", "method": "post", "service_key": "foo"}
        ) == [{"url": "http://foo.com/webhook", "method": "POST", "service_key": "foo"}]
        assert self.webhook.get_config(
            [
                {
                    "url": "http://foo.com/webhook",
                    "method": "post",
                    "service_key": "foo",
                },
                {
                    "url": "http://bar.com/webhook",
                    "method": "GET",
                    "service_key": "bar",
                },
            ]
        ) == [
            {"url": "http://foo.com/webhook", "method": "POST", "service_key": "foo"},
            {"url": "http://bar.com/webhook", "method": "GET", "service_key": "bar"},
        ]

    def test_prepare(self):
        with self.assertRaises(PolyaxonNotificationException):
            self.webhook._prepare(None)
        with self.assertRaises(PolyaxonNotificationException):
            self.webhook._prepare({})

        context = {"title": "title", "text": "text"}
        assert self.webhook._prepare(context) == {
            "event_type": context.get("event_type"),
            "description": context.get("description"),
            "details": context.get("details"),
            "incident_key": context.get("incident_key"),
            "client": "Polyaxon",
            "client_url": "https://polyaxon.com",
            "contexts": context.get("contexts"),
        }


del TestWebHookNotification
