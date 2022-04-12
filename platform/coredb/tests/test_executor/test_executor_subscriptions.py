#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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

from coredb import executor
from polycommon.events.registry import run


class TestExecutorsSubscriptions(TestCase):
    def setUp(self):
        super().setUp()
        executor.validate_and_setup()
        # load subscriptions
        from coredb.executor import subscriptions  # noqa

    def _assert_events_subscription(self, events):
        for event in events:
            assert executor.event_manager.knows(event)

    def _assert_events_no_subscription(self, events):
        for event in events:
            assert executor.event_manager.knows(event) is False

    def test_events_subjects_runs(self):
        subscribed_events = {
            run.RUN_CREATED,
            run.RUN_RESUMED_ACTOR,
            run.RUN_STOPPED_ACTOR,
            run.RUN_APPROVED_ACTOR,
            run.RUN_DELETED_ACTOR,
            run.RUN_DONE,
            run.RUN_NEW_ARTIFACTS,
            run.RUN_NEW_STATUS,
        }

        self._assert_events_subscription(subscribed_events)
        self._assert_events_no_subscription(run.EVENTS - subscribed_events)
