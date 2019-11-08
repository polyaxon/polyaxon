#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# coding: utf-8
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import pytest

from polyaxon.specs import OpSpecification
from polyaxon.specs.libs.parser import Parser


@pytest.mark.polyaxonfile_mark
class TestParser(TestCase):
    def test_parse_base_expressions(self):
        data = [
            1,
            10.0,
            [1, 1],
            (1, 1),
            "string",
            ["str1", "str2"],
            {1: 2, "a": "a", "dict": {1: 1}},
        ]

        parser = Parser()
        for d in data:
            assert d == parser.parse_expression(OpSpecification, d, {})

    def test_parse_context_expression(self):
        parser = Parser()
        assert parser.parse_expression(OpSpecification, "{{ something }}", {}) == ""
        assert (
            parser.parse_expression(
                OpSpecification, "{{ something }}", {"something": 1}
            )
            == 1
        )
