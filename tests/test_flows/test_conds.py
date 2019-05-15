# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow import ValidationError

from polyaxon_schemas.flows.conds import OutputsCondConfig, StatusCondConfig, CondSchema


class TestCondsConfigs(TestCase):
    def test_status_cond(self):
        config_dict = {'foo': 'bar', 'operation': 'foo', 'trigger': 'done'}
        with self.assertRaises(ValidationError):
            StatusCondConfig.from_dict(config_dict)

        config_dict = {'kind': 'foo', 'operation': 'foo', 'trigger': 'done'}
        with self.assertRaises(ValidationError):
            StatusCondConfig.from_dict(config_dict)

        config_dict = {
            'operation': 'foo',
            'trigger': 'done'
        }
        StatusCondConfig.from_dict(config_dict)

        config_dict = {
            'kind': 'status_cond',
            'operation': 'foo',
            'trigger': 'done'
        }
        StatusCondConfig.from_dict(config_dict)

    def test_outputs_cond(self):
        config_dict = {'operation': 'foo', 'exp': 'done', 'params': ['op1.done', 'foo']}
        with self.assertRaises(ValidationError):
            OutputsCondConfig.from_dict(config_dict)

        config_dict = {'kind': 'foo',
                       'operation': 'foo',
                       'exp': 'eq',
                       'params': [['op1.done', 'foo']]}
        with self.assertRaises(ValidationError):
            OutputsCondConfig.from_dict(config_dict)

        config_dict = {'operation': 'foo',
                       'exp': 'eq',
                       'params': ['op1.done', 'foo']}
        with self.assertRaises(ValidationError):
            OutputsCondConfig.from_dict(config_dict)

        config_dict = {
            'operation': 'foo',
            'exp': 'eq',
            'params': [['op1.done', 'foo']]
        }
        OutputsCondConfig.from_dict(config_dict)

        config_dict = {
            'kind': 'outputs_cond',
            'operation': 'foo',
            'exp': 'eq',
            'params': [['op1.done', 'foo']]
        }
        OutputsCondConfig.from_dict(config_dict)

    def test_conds(self):
        configs = [
            {
                'kind': 'status_cond',
                'operation': 'foo',
                'trigger': 'done'
            },
            {
                'kind': 'outputs_cond',
                'operation': 'foo',
                'exp': 'eq',
                'params': [['op1.done', 'foo']]
            }
        ]

        CondSchema().load(configs, many=True)
