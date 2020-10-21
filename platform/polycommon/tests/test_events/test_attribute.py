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

import uuid

from datetime import datetime
from unittest import TestCase

from dateutil.tz import UTC
from polycommon.events.event import Attribute


class TestAttribute(TestCase):
    def test_name_should_not_be_instance(self):
        with self.assertRaises(AssertionError):
            Attribute(name="instance")

    def test_props(self):
        attr = Attribute(name="test")
        assert attr.name == "test"
        assert attr.attr_type == str
        assert attr.is_datetime is False
        assert attr.is_uuid is False
        assert attr.is_required is True

    def test_extract(self):
        attr = Attribute(name="test")
        assert attr.extract(value="some value") == "some value"
        assert attr.extract(value=1) == "1"

        attr = Attribute(name="test", attr_type=int)
        assert attr.extract(value=1) == 1

        attr = Attribute(name="test", is_datetime=True)
        dt = datetime(2000, 12, 12, tzinfo=UTC)
        assert attr.extract(value=dt) == 976579200.0

        attr = Attribute(name="test", is_uuid=True)
        uid = uuid.uuid4()
        assert attr.extract(value=uid) == uid.hex
