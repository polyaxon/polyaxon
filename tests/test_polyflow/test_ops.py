# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow import ValidationError

from polyaxon_schemas.polyflow.ops import OpConfig


class TestOpConfigs(TestCase):
    def test_op_raises_for_template_action_event(self):
        config_dict = {'template': {'action': 'foo', 'event': 'bar'}}
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        config_dict = {'template': {'path': 'bar', 'action': 'foo', }}
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        config_dict = {'template': {'url': 'bar', 'action': 'foo'}}
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

    def test_op_passes_for_template_action_event(self):
        config_dict = {'template': {'event': 'bar'}}
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {'template': {'action': 'foo'}}
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {'template': {'path': 'bar'}}
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {'template': {'url': 'bar'}}
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {'template': {'name': 'bar'}}
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_validation(self):
        config_dict = {'template': {'action': 'foo'}, 'concurrency': 'foo'}
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        config_dict = {'template': {'action': 'foo'}, 'dependencies': 'foo'}
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        config_dict = {
            'template': {'action': 'foo'},
            'concurrency': 2,
            'dependencies': ['foo', 'bar'],
            'params': {'param1': 'foo', 'param2': 'bar'},
            'trigger': 'all_succeeded',
            'max_retries': 4,
        }
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {
            'template': {'event': 'foo'},
            'concurrency': 2,
        }
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {
            'template': {'name': 'foo'},
            'concurrency': 2,
            'dependencies': [{'name': 'foo'}, {'name': 'bar'}],  # Wrong
            'params': {'param1': 'foo', 'param2': 'bar'},
            'trigger': 'all_succeeded',
            'max_retries': 4,
        }
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)
