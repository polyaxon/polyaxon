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

import datetime

from polyaxon.utils.humanize import humanize_timedelta, humanize_timesince
from polyaxon.utils.tz_utils import local_datetime, now
from tests.utils import BaseTestCase


class HumanizeTimesinceTest(BaseTestCase):
    """A test case for humanize timesince"""

    def test_humanize_timesince(self):
        self.assertEqual(humanize_timesince(local_datetime(now())), "a few seconds ago")
        self.assertEqual(
            humanize_timesince(local_datetime(now()) - datetime.timedelta(minutes=1)),
            "1 minute ago",
        )
        self.assertEqual(
            humanize_timesince(local_datetime(now()) - datetime.timedelta(minutes=10)),
            "10 minutes ago",
        )
        self.assertEqual(
            humanize_timesince(local_datetime(now()) - datetime.timedelta(hours=1)),
            "1 hour ago",
        )
        self.assertEqual(
            humanize_timesince(local_datetime(now()) - datetime.timedelta(hours=10)),
            "10 hours ago",
        )
        self.assertEqual(
            humanize_timesince(local_datetime(now()) - datetime.timedelta(hours=24)),
            "1 day ago",
        )
        self.assertEqual(
            humanize_timesince(local_datetime(now()) - datetime.timedelta(hours=72)),
            "3 days ago",
        )
        self.assertEqual(
            humanize_timesince(local_datetime(now()) - datetime.timedelta(hours=168)),
            "1 week ago",
        )
        self.assertEqual(
            humanize_timesince(local_datetime(now()) - datetime.timedelta(weeks=1)),
            "1 week ago",
        )
        self.assertEqual(
            humanize_timesince(local_datetime(now()) - datetime.timedelta(weeks=3)),
            "3 weeks ago",
        )
        self.assertEqual(
            humanize_timesince(local_datetime(now()) - datetime.timedelta(weeks=53)),
            "1 year ago",
        )
        self.assertEqual(
            humanize_timesince(local_datetime(now()) - datetime.timedelta(days=365)),
            "1 year ago",
        )
        self.assertEqual(
            humanize_timesince(local_datetime(now()) - datetime.timedelta(days=800)),
            "2 years ago",
        )

    def test_humanize_times_in_the_future(self):
        self.assertEqual(
            humanize_timesince(local_datetime(now()) + datetime.timedelta(minutes=1)),
            "a few seconds ago",
        )

    def test_humanize_timesince_few_seconds(self):
        self.assertEqual(
            u"Last update: " + humanize_timesince(local_datetime(now())),
            u"Last update: a few seconds ago",
        )


class HumanizeTimeDeltaTest(BaseTestCase):
    """A test case for the `humanize_timedelta`."""

    def test_works_as_expected_for_valid_values(self):
        test_data = [
            (7200, "2h"),
            (36, "36s"),
            (3600, "1h"),
            (3800, "1h 3m"),
            (33000, "9h 10m"),
            (720000, "8d 8h"),
            (1000000, "11d 13h 46m"),
        ]
        for value, expected in test_data:
            result = humanize_timedelta(value)
            self.assertEqual(result, expected)
