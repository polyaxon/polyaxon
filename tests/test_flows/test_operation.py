# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from hestia.tz_utils import local_now
from marshmallow import ValidationError

from polyaxon_schemas.flows.operation import OperationConfig


class TestOperationConfigs(TestCase):
    def test_operation(self):
        config_dict = {'concurrency': 'foo'}
        with self.assertRaises(ValidationError):
            OperationConfig.from_dict(config_dict)

        config_dict = {'upstream_operations': 'foo'}
        with self.assertRaises(ValidationError):
            OperationConfig.from_dict(config_dict)

        config_dict = {
            'concurrency': 2,
        }
        OperationConfig.from_dict(config_dict)

        config_dict = {
            'concurrency': 2,
            'upstream_operations': ['foo', 'bar'],
            'inputs': [['param1', 'foo.outputs1'], ['param2', 'bar.outputs1']],
            'trigger': 'all_succeeded',
            'max_retries': 4,
            'execute_at': local_now().isoformat(),
            'timeout': 1000
        }
        OperationConfig.from_dict(config_dict)
