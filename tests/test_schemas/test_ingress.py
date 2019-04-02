# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow import ValidationError
from polyaxon_deploy.schemas.ingress import IngressConfig


class TestIngressConfig(TestCase):
    def test_ingress_config(self):
        config_dict = {
            'enabled': 'sdf',
        }

        with self.assertRaises(ValidationError):
            IngressConfig.from_dict(config_dict)

        config_dict = {
            'enabled': False,
        }

        config = IngressConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            'enabled': False,
            'tls': [{'hosts': 'bar.com'}],
            'annotations': {'a': 'b'},
        }

        config = IngressConfig.from_dict(config_dict)

        assert config.to_light_dict() == config_dict
