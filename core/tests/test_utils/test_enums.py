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

from enum import Enum

from polyaxon.utils.enums_utils import enum_to_choices, enum_to_set, values_to_choices
from tests.utils import BaseTestCase


class Dummy1Enum(Enum):
    A = 1
    B = 2


class Dummy2Enum(Enum):
    A = "A"
    B = "B"


class TestEnums(BaseTestCase):
    def test_enum_to_choices(self):
        assert enum_to_choices(Dummy1Enum) == ((1, 1), (2, 2))
        assert enum_to_choices(Dummy2Enum) == (("A", "A"), ("B", "B"))

    def test_values_to_choices(self):
        assert values_to_choices({1, 2}) == ((1, 1), (2, 2))
        assert values_to_choices(["A", "B"]) == (("A", "A"), ("B", "B"))

    def test_enum_to_set(self):
        assert enum_to_set(Dummy1Enum) == {1, 2}
        assert enum_to_set(Dummy2Enum) == {"A", "B"}
