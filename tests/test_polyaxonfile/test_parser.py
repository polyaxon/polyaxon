# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import pytest

from schemas.specs import JobSpecification
from schemas.specs.libs.parser import Parser


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
            assert d == parser.parse_expression(JobSpecification, d, {})

    def test_parse_context_expression(self):
        parser = Parser()
        assert parser.parse_expression(JobSpecification, "{{ something }}", {}) == ""
        assert (
            parser.parse_expression(
                JobSpecification, "{{ something }}", {"something": 1}
            )
            == 1
        )
