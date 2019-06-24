# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow import ValidationError

from polyaxon_schemas.polyflow.conditions import (
    ConditionSchema,
    OutputsConditionConfig,
    StatusConditionConfig
)


class TestCondsConfigs(TestCase):
    def test_status_cond(self):
        config_dict = {'foo': 'bar', 'op': 'foo', 'trigger': 'done'}
        with self.assertRaises(ValidationError):
            StatusConditionConfig.from_dict(config_dict)

        config_dict = {'kind': 'foo', 'op': 'foo', 'trigger': 'done'}
        with self.assertRaises(ValidationError):
            StatusConditionConfig.from_dict(config_dict)

        config_dict = {
            'op': 'foo',
            'trigger': 'done'
        }
        StatusConditionConfig.from_dict(config_dict)

        config_dict = {
            'kind': 'status',
            'op': 'foo',
            'trigger': 'done'
        }
        StatusConditionConfig.from_dict(config_dict)

    def test_outputs_cond(self):
        config_dict = {'op': 'foo', 'exp': 'done', 'params': ['op1.done', 'foo']}
        with self.assertRaises(ValidationError):
            OutputsConditionConfig.from_dict(config_dict)

        config_dict = {'kind': 'foo',
                       'op': 'foo',
                       'exp': 'eq',
                       'params': [['op1.done', 'foo']]}
        with self.assertRaises(ValidationError):
            OutputsConditionConfig.from_dict(config_dict)

        config_dict = {'op': 'foo',
                       'exp': 'eq',
                       'params': ['op1.done', 'foo']}
        with self.assertRaises(ValidationError):
            OutputsConditionConfig.from_dict(config_dict)

        config_dict = {
            'op': 'foo',
            'exp': 'eq',
            'params': [['op1.done', 'foo']]
        }
        OutputsConditionConfig.from_dict(config_dict)

        config_dict = {
            'kind': 'outputs',
            'op': 'foo',
            'exp': 'eq',
            'params': [['op1.done', 'foo']]
        }
        OutputsConditionConfig.from_dict(config_dict)

    def test_conds(self):
        configs = [
            {
                'kind': 'status',
                'op': 'foo',
                'trigger': 'done'
            },
            {
                'kind': 'outputs',
                'op': 'foo',
                'exp': 'eq',
                'params': [['op1.done', 'foo']]
            }
        ]

        ConditionSchema().load(configs, many=True)
