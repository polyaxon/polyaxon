# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid

from unittest import TestCase

from hestia.tz_utils import local_now
from marshmallow import ValidationError
from tests.utils import assert_equal_dict

from polyaxon_schemas.api.experiment import ExperimentConfig
from polyaxon_schemas.api.group import GroupConfig
from polyaxon_schemas.api.project import ProjectConfig


class TestProjectConfigs(TestCase):
    def test_validate_project_name_config(self):
        config_dict = {'name': 'test sdf', 'description': '', 'is_public': True}
        with self.assertRaises(ValidationError):
            ProjectConfig.from_dict(config_dict)

    def test_project_config(self):
        config_dict = {
            'name': 'test',
            'description': '',
            'is_public': True,
            'has_code': True,
            'has_tensorboard': True,
            'tags': ['foo'],
            'num_experiments': 0,
            'num_independent_experiments': 0,
            'num_experiment_groups': 0,
            'num_jobs': 0,
            'num_builds': 0,
            'created_at': local_now().isoformat(),
            'updated_at': local_now().isoformat()
        }
        config = ProjectConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        config_to_dict.pop('id', None)
        config_to_dict.pop('experiment_groups', None)
        config_to_dict.pop('experiments', None)
        config_to_dict.pop('has_notebook', None)
        config_to_dict.pop('unique_name', None)
        config_to_dict.pop('user', None)
        config_to_dict.pop('owner', None)
        config_to_dict.pop('uuid', None)
        assert config_to_dict == config_dict
        config_dict.pop('description')
        config_dict.pop('updated_at')
        config_dict.pop('has_code')
        config_to_dict = config.to_light_dict()
        config_to_dict.pop('has_notebook', None)
        config_to_dict.pop('unique_name', None)
        assert config_to_dict == config_dict

        config_to_dict = config.to_dict(humanize_values=True)
        assert config_to_dict.pop('created_at') == 'a few seconds ago'
        assert config_to_dict.pop('updated_at') == 'a few seconds ago'

        config_to_dict = config.to_light_dict(humanize_values=True)
        assert config_to_dict.pop('created_at') == 'a few seconds ago'

    def test_project_experiments_and_groups_config(self):
        uuid_value = uuid.uuid4().hex
        config_dict = {'name': 'test',
                       'description': '',
                       'is_public': True,
                       'experiment_groups': [
                           GroupConfig(content='content',
                                                 uuid=uuid_value,
                                                 project=uuid_value).to_dict()],
                       'experiments': [
                           ExperimentConfig(uuid=uuid_value,
                                            project=uuid_value).to_dict()]}
        config = ProjectConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        config_dict.pop('description')
        config_dict.pop('experiment_groups')
        config_dict.pop('experiments')
        assert_equal_dict(config_dict, config.to_light_dict())
