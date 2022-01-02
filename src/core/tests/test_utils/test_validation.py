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

from polyaxon.utils.validation import validate_tags
from tests.utils import BaseTestCase


class TestValidation(BaseTestCase):
    def test_validate_tags(self):
        assert ["foo", "bar"] == validate_tags("foo,bar")
        assert ["foo", "bar"] == validate_tags("  , foo,    bar,   ")
        assert ["foo", "bar"] == validate_tags(["foo", "bar"])
        assert ["foo", "bar"] == validate_tags(["foo", "bar", 1, 2])
        assert [] == validate_tags([{}, {}, 1, 2])
