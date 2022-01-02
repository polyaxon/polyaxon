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

from unittest import TestCase

from polycommon import auditor
from polycommon.events.registry import run


class TestEventsSubscriptions(TestCase):
    def setUp(self):
        super().setUp()
        auditor.validate_and_setup()
        # load subscriptions
        from polycommon.events import auditor_subscriptions  # noqa

    def _assert_events_subscription(self, events):
        for event in events:
            assert auditor.event_manager.knows(event)

    def test_events_subjects_runs(self):
        self._assert_events_subscription(run.EVENTS)
