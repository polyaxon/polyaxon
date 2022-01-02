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

from polyaxon.utils.units import format_sizeof, to_percentage
from tests.utils import BaseTestCase


class ToPercentageTest(BaseTestCase):
    """A test case for the `to_percentage`."""

    def test_works_as_expected_for_valid_values(self):
        test_data = [
            (0, "0%"),
            (0.25, "25%"),
            (-0.25, "-25%"),
            (12, "1200%"),
            (0.123, "12.3%"),
            (0.12345, "12.35%"),
            (0.12001, "12%"),
            (0.12101, "12.1%"),
            ("0", "0%"),
            ("0.25", "25%"),
        ]
        for value, expected in test_data:
            result = to_percentage(value)
            self.assertEqual(result, expected)

    def test_raises_value_error_for_invalid_types(self):
        with self.assertRaises(ValueError):
            to_percentage("foo")

    def test_format_sizeof(self):
        assert format_sizeof(10) == "10.0B"
        assert format_sizeof(10000) == "9.8KiB"
        assert format_sizeof(100000) == "97.7KiB"
        assert format_sizeof(10000000) == "9.5MiB"
        assert format_sizeof(10000000000) == "9.3GiB"
