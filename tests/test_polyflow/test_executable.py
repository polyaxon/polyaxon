# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from hestia.tz_utils import local_now
from marshmallow import ValidationError

from polyaxon_schemas.polyflow.executable import ExecutableConfig


class TestExecutableConfigs(TestCase):
    def test_executable(self):
        config_dict = {'start_at': 'foo'}
        with self.assertRaises(ValidationError):
            ExecutableConfig.from_dict(config_dict)

        config_dict = {'execute_at': 'foo'}
        with self.assertRaises(ValidationError):
            ExecutableConfig.from_dict(config_dict)

        config_dict = {
            'timeout': 2,
            'execute_at': local_now().isoformat()
        }
        ExecutableConfig.from_dict(config_dict)

        config_dict = {
            'timeout': 2,
        }
        ExecutableConfig.from_dict(config_dict)
