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

import pytest

from mock import patch

from polyaxon.cli.check import check
from tests.test_cli.utils import BaseCommandTestCase


@pytest.mark.cli_mark
class TestCliCheck(BaseCommandTestCase):
    @patch("polyaxon.cli.check.check_polyaxonfile")
    def test_check_file(self, check_polyaxonfile):
        self.runner.invoke(check)
        assert check_polyaxonfile.call_count == 1

    @patch("polyaxon.cli.check.check_polyaxonfile")
    @patch("polyaxon.cli.check.Printer.decorate_format_value")
    def test_check_file_version(self, decorate_format_value, check_polyaxonfile):
        self.runner.invoke(check, ["--version"])
        assert check_polyaxonfile.call_count == 1
        assert decorate_format_value.call_count == 1
