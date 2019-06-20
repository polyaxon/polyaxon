# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow import ValidationError
from polyaxon_deploy.schemas.security_context import SecurityContextConfig


class TestSecurityContentConfig(TestCase):

    def test_security_content_config(self):
        config_dict = {}
        config = SecurityContextConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {'enabled': True}
        SecurityContextConfig.from_dict(config_dict)

        config_dict = {'enabled': False}
        SecurityContextConfig.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            config_dict = {'user': 'foo'}
            SecurityContextConfig.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            config_dict = {'user': 120}
            SecurityContextConfig.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            config_dict = {'group': 'foo'}
            SecurityContextConfig.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            config_dict = {'group': 120}
            SecurityContextConfig.from_dict(config_dict)

        with self.assertRaises(ValidationError):
            config_dict = {'user': 'sdf', 'group': 120}
            SecurityContextConfig.from_dict(config_dict)

        config_dict = {'user': 120, 'group': 120}
        config = SecurityContextConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {'enabled': True, 'user': 120, 'group': 120}
        config = SecurityContextConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
