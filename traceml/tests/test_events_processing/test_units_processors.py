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

import pytest

from unittest import TestCase

from traceml.processors.units_processors import (
    format_sizeof,
    number_percentage_format,
    to_percentage,
)


@pytest.mark.processors_mark
class ToPercentageTest(TestCase):
    """A test case for the `to_percentage`."""

    def test_number_format_works_as_expected(self):
        float_nums = [
            (123.123, "123.12"),
            (123.1243453, "123.12"),
            (213213213.123, "213,213,213.12"),
        ]
        int_nums = [(213214, "213,214"), (123213.00, "123,213")]

        for num, expected in float_nums:
            self.assertEqual(
                number_percentage_format(num, precision=2, use_comma=True), expected
            )

        for num, expected in int_nums:
            self.assertEqual(
                number_percentage_format(num, precision=2, use_comma=True), expected
            )

    def test_get_percentage_works_as_expected(self):
        float_nums = [
            (0.123, "12.30%"),
            (3.1243453, "312.43%"),
            (213.12312, "21,312.31%"),
        ]

        int_nums = [(0.14, "14%"), (1.300, "130%")]

        for num, expected in float_nums:
            self.assertEqual(
                to_percentage(num, rounding=2, precision=2, use_comma=True), expected
            )

        for num, expected in int_nums:
            self.assertEqual(
                to_percentage(num, rounding=2, precision=2, use_comma=True), expected
            )

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
            (3.1243453, "312.43%"),
            (213.12312, "21312.31%"),
            (0.14, "14%"),
            (1.300, "130%"),
        ]
        for value, expected in test_data:
            result = to_percentage(value)
            self.assertEqual(result, expected)

    def test_works_as_expected_for_precision(self):
        test_data = [
            (0, "0%"),
            (0.25, "25%"),
            (-0.25, "-25%"),
            (12, "1200%"),
            (0.123, "12.300%"),
            (0.12345, "12.345%"),
            (0.12001, "12.001%"),
            (0.12101, "12.101%"),
            ("0", "0%"),
            ("0.25", "25%"),
            (3.1243453, "312.435%"),
            (213.12312, "21,312.312%"),
            (0.14, "14%"),
            (1.300, "130%"),
        ]
        for value, expected in test_data:
            result = to_percentage(value, rounding=3, precision=3, use_comma=True)
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
