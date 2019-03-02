# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow import ValidationError
from polyaxon_deploy.schemas.persistence import PersistenceConfig, PersistenceEntityConfig


class TestPersistenceConfig(TestCase):
    def test_persistence_entity_config(self):
        bad_config_dicts = [
            {'existingClaim': 1},
            {'mountPath': False},
            {'hostPath': False},
            {'store': False},
            {'store': 'dfo'},
            {'bucket': False},
            {'secret': False},
            {'secretKey': 321},
            {'readOnly': 'foo'},
            {'existingClaim': 'foo', 'hostPath': 'bar'},
            {'existingClaim': 'foo', 'store': 'bar'},
            {'hostPath': 'foo', 'store': 's3'},
        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises(ValidationError):
                PersistenceEntityConfig.from_dict(config_dict)

        config_dicts = [
            {'existingClaim': 'test'},
            {'mountPath': 'test'},
            {'hostPath': 'test'},
            {'store': 'azure'},
            {'bucket': 'test'},
            {'secret': 'test'},
            {'secretKey': 'test'},
            {'readOnly': False}
        ]

        for config_dict in config_dicts:
            config = PersistenceEntityConfig.from_dict(config_dict)
            assert config.to_light_dict() == config_dict

    def test_persistence_config(self):
        bad_config_dicts = [
            {'logs': {'existingClaim': 'foo'}, 'data': {'existingClaim': False}},
            {'repos': {'hostPath': 'foo'},
             'data': {'foo': {'existingClaim': 'foo'}, 'bar': {'hostPath': False}}},
            {'repos': {'hostPath': 'foo'},
             'data': {'foo': {'existingClaim': 'foo', 'hostPath': 'foo'},
                      'bar': {'hostPath': 'foo'}}},
            {'upload': {'hostPath': 'test'},
             'data': {'hostPath': 'test'}},
            {'logs': {'hostPath': 'test'},
             'outputs': {'existingClaim': 'foo'}},
            {'logs': {'hostPath': 123},
             'outputs': {'foo': {'existingClaim': 'foo'}}},
        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises(ValidationError):
                PersistenceConfig.from_dict(config_dict)

        config_dicts = [
            {},
            {'repos': {'existingClaim': 'foo'}, 'outputs': {}},
            {'upload': {}, 'outputs': {}},
            {'logs': {}},
            {'repos': {}},
            {'upload': {}},
            {'logs': {'existingClaim': 'foo'}, 'data': {},
             'outputs': {'foo': {'existingClaim': 'foo'}, 'bar': {'hostPath': 'foo'}}},
            {'repos': {'existingClaim': 'foo'},
             'logs': {'existingClaim': 'foo'},
             'data': {'foo': {'existingClaim': 'foo'},
                      'bar': {'hostPath': 'bar', 'readOnly': True},
                      'moo': {'store': 's3'}},
             'outputs': {'foo': {'existingClaim': 'foo'}}},
        ]

        for config_dict in config_dicts:
            config = PersistenceConfig.from_dict(config_dict)
            assert config.to_light_dict() == config_dict
