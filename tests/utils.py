# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import os

from unittest import TestCase


class TestEnvVarsCase(TestCase):
    @staticmethod
    def check_empty_value(key, expected_function):
        os.environ.pop(key, None)
        assert expected_function() is None

    @staticmethod
    def check_non_dict_value(key, expected_function, value='non dict random value'):
        os.environ[key] = value
        assert expected_function() is None

    @staticmethod
    def check_valid_dict_value(key, expected_function, value):
        os.environ[key] = json.dumps(value)
        assert expected_function() == value

    @staticmethod
    def check_valid_value(key, expected_function, value):
        os.environ[key] = value
        assert expected_function() == value
