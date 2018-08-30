# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_cli.utils.validation import validate_tags


class TestValidation(TestCase):
    def test_validate_tags(self):
        assert ['foo', 'bar'] == validate_tags('foo,bar')
        assert ['foo', 'bar'] == validate_tags('  , foo,    bar,   ')
        assert ['foo', 'bar'] == validate_tags(['foo', 'bar'])
        assert ['foo', 'bar'] == validate_tags(['foo', 'bar', 1, 2])
        assert [] == validate_tags([{}, {}, 1, 2])
