# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime

from unittest import TestCase

from polyaxon_schemas.utils import humanize_timedelta, humanize_timesince, local_now, to_percentage


class HumanizeTimesinceTest(TestCase):
    """A test case for humanize timesince"""

    def test_humanize_timesince(self):
        self.assertEqual(humanize_timesince(local_now()), 'a few seconds ago')
        self.assertEqual(humanize_timesince(local_now() - datetime.timedelta(minutes=1)),
                         '1 minute ago')
        self.assertEqual(humanize_timesince(local_now() - datetime.timedelta(minutes=10)),
                         '10 minutes ago')
        self.assertEqual(humanize_timesince(local_now() - datetime.timedelta(hours=1)),
                         '1 hour ago')
        self.assertEqual(humanize_timesince(local_now() - datetime.timedelta(hours=10)),
                         '10 hours ago')
        self.assertEqual(humanize_timesince(local_now() - datetime.timedelta(hours=24)),
                         '1 day ago')
        self.assertEqual(humanize_timesince(local_now() - datetime.timedelta(hours=72)),
                         '3 days ago')
        self.assertEqual(humanize_timesince(local_now() - datetime.timedelta(hours=168)),
                         '1 week ago')
        self.assertEqual(humanize_timesince(local_now() - datetime.timedelta(weeks=1)),
                         '1 week ago')
        self.assertEqual(humanize_timesince(local_now() - datetime.timedelta(weeks=3)),
                         '3 weeks ago')
        self.assertEqual(humanize_timesince(local_now() - datetime.timedelta(weeks=53)),
                         '1 year ago')
        self.assertEqual(humanize_timesince(local_now() - datetime.timedelta(days=365)),
                         '1 year ago')
        self.assertEqual(humanize_timesince(local_now() - datetime.timedelta(days=800)),
                         '2 years ago')

    def test_humanize_times_in_the_future(self):
        self.assertEqual(humanize_timesince(local_now() + datetime.timedelta(minutes=1)),
                         'a few seconds ago')

    def test_humanize_timesince_few_seconds(self):
        self.assertEqual(u'Last update: ' + humanize_timesince(local_now()),
                         u'Last update: a few seconds ago')


class HumanizeTimeDeltaTest(TestCase):
    """A test case for the `humanize_timedelta`."""
    def test_works_as_expected_for_valid_values(self):
        test_data = [
            (7200, '2h'),
            (36, '36s'),
            (3600, '1h'),
            (3800, '1h 3m'),
            (33000, '9h 10m'),
            (720000, '8d 8h'),
            (1000000, '11d 13h 46m'),
        ]
        for value, expected in test_data:
            result = humanize_timedelta(value)
            self.assertEqual(result, expected)


class ToPercentageTest(TestCase):
    """A test case for the `to_percentage`."""
    def test_works_as_expected_for_valid_values(self):
        test_data = [
            (0, '0%'),
            (0.25, '25%'),
            (-0.25, '-25%'),
            (12, '1200%'),
            (0.123, '12.3%'),
            (0.12345, '12.35%'),
            (0.12001, '12%'),
            (0.12101, '12.1%'),
            ('0', '0%'),
            ('0.25', '25%'),
        ]
        for value, expected in test_data:
            result = to_percentage(value)
            self.assertEqual(result, expected)

    def test_raises_value_error_for_invalid_types(self):
        with self.assertRaises(ValueError):
            to_percentage('foo')
