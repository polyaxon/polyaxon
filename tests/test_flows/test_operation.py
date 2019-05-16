# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from hestia.tz_utils import local_now
from marshmallow import ValidationError

from polyaxon_schemas.ops.operation import BaseOpConfig


class TestBaseOpConfigs(TestCase):
    def test_operation(self):
        config_dict = {'concurrency': 'foo'}
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

        config_dict = {'deps': 'foo'}
        with self.assertRaises(ValidationError):
            BaseOpConfig.from_dict(config_dict)

        config_dict = {
            'concurrency': 2,
        }
        BaseOpConfig.from_dict(config_dict)

        config_dict = {
            'concurrency': 2,
            'deps': ['foo', 'bar'],
            'inputs': [['param1', 'foo.outputs1'], ['param2', 'bar.outputs1']],
            'trigger': 'all_succeeded',
            'max_retries': 4,
            'execute_at': local_now().isoformat(),
            'timeout': 1000
        }
        BaseOpConfig.from_dict(config_dict)
