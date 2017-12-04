# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid
from datetime import datetime
from unittest import TestCase

from polyaxon_schemas.data import DataDetailsConfig, DataConfig, DatasetConfig


class TestDataConfigs(TestCase):
    def test_data_details_config(self):
        config_dict = {
            'state': 'state',
            'size': 1.4,
            'uri': 'http://www.foo.com/data'
        }
        config = DataDetailsConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_data_config(self):
        config_dict = {
            'uuid': uuid.uuid4().hex,
            'name': 'foo',
            'created_at': datetime.now().isoformat(),
            'description': 'foo data',
            'details': DataDetailsConfig(
                state='state', size=1.4, uri='http://www.foo.com/data').to_dict(),
            'version': None,
            'resource_id': '1'
        }
        config = DataConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        # assert config_to_dict.pop('created_at') == config_dict.pop('created_at')
        config_to_dict.pop('created_at')
        config_dict.pop('created_at')
        assert config_to_dict == config_dict

    def test_dataset_config(self):
        config_dict = {
            'uuid': uuid.uuid4().hex,
            'name': 'foo',
            'description': 'foo data',
            'is_public': True
        }
        config = DatasetConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
