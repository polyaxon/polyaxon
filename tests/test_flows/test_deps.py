# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid
from unittest import TestCase

from marshmallow import ValidationError

from polyaxon_schemas.flows.deps import DepConfig


class TestDepsConfigs(TestCase):
    def test_deps(self):
        config_dict = {'name': 'bar', 'id': 'foo'}
        with self.assertRaises(ValidationError):
            DepConfig.from_dict(config_dict)

        config_dict = {'uuid': 'bar', 'id': 'foo'}
        with self.assertRaises(ValidationError):
            DepConfig.from_dict(config_dict)

        config_dict = {'uuid': 'bar'}
        with self.assertRaises(ValidationError):
            DepConfig.from_dict(config_dict)

        config_dict = {}
        with self.assertRaises(ValidationError):
            DepConfig.from_dict(config_dict)

        config_dict = {
            'id': 1,
        }
        DepConfig.from_dict(config_dict)

        config_dict = {
            'name': 'test',
        }
        DepConfig.from_dict(config_dict)

        config_dict = {
            'uuid': uuid.uuid4().hex,
        }
        DepConfig.from_dict(config_dict)
