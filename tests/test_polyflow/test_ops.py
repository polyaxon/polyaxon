# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import pytest

from marshmallow import ValidationError

from polyaxon_schemas.polyflow.ops import OpConfig


@pytest.mark.polyflow_mark
class TestOpConfigs(TestCase):
    def test_op_raises_for_template_action_event(self):
        config_dict = {"template": {"hub": "foo", "name": "bar"}}
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        config_dict = {"template": {"path": "bar", "hub": "foo"}}
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        config_dict = {"template": {"url": "bar", "hub": "foo"}}
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

    def test_op_passes_for_template_hub(self):
        config_dict = {"template": {"hub": "bar"}}
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {"template": {"hub": "foo"}}
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {"template": {"path": "bar"}}
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {"template": {"url": "bar"}}
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {"template": {"name": "bar"}}
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_validation(self):
        config_dict = {"template": {"hub": "foo"}, "concurrency": "foo"}
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        config_dict = {"template": {"hub": "foo"}, "dependencies": "foo"}
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)

        config_dict = {
            "template": {"hub": "foo"},
            "dependencies": ["foo", "bar"],
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
        }
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {"template": {"hub": "foo"}}
        config = OpConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {
            "template": {"name": "foo"},
            "dependencies": [{"name": "foo"}, {"name": "bar"}],  # Wrong
            "params": {"param1": "foo", "param2": "bar"},
            "trigger": "all_succeeded",
        }
        with self.assertRaises(ValidationError):
            OpConfig.from_dict(config_dict)
