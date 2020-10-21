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
import pytest

from dateutil import parser as dt_parser

from polyaxon.polyboard.logging.parser import (
    DATETIME_REGEX,
    ISO_DATETIME_REGEX,
    timestamp_search_regex,
)
from tests.utils import BaseTestCase


@pytest.mark.polyboard_mark
class TestLoggingUtils(BaseTestCase):
    def test_has_timestamp(self):
        log_line = "2018-12-11 10:24:57 UTC"
        log_value, ts = timestamp_search_regex(DATETIME_REGEX, log_line)
        assert ts == dt_parser.parse("2018-12-11 10:24:57 UTC")
        assert log_value == ""

    def test_log_line_has_datetime(self):
        log_line = "2018-12-11 10:24:57 UTC foo"
        log_value, ts = timestamp_search_regex(DATETIME_REGEX, log_line)

        assert ts == dt_parser.parse("2018-12-11 10:24:57 UTC")
        assert log_value == "foo"

    def test_log_line_has_iso_datetime(self):
        log_line = "2018-12-11T08:49:07.163495183Z foo"

        log_value, ts = timestamp_search_regex(ISO_DATETIME_REGEX, log_line)

        assert ts == dt_parser.parse("2018-12-11T08:49:07.163495183Z")
        assert log_value == "foo"
