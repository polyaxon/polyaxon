# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os

from unittest import TestCase

from polystores.utils import get_from_env


class TestConstraintConfigs(TestCase):
    def test_get_from_env(self):
        assert get_from_env(keys=None) is None
        assert get_from_env(keys=[]) is None
        assert get_from_env(keys='some_random_text_foo_000') is None

        os.environ['some_random_text_foo_000'] = 'a'

        assert get_from_env(['some_random_text_foo_000']) == 'a'

        del os.environ['some_random_text_foo_000']

        os.environ['POLYAXON_some_random_text_foo_000'] = 'a'

        assert get_from_env(['some_random_text_foo_000']) == 'a'

        del os.environ['POLYAXON_some_random_text_foo_000']
