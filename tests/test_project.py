# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid
from unittest import TestCase

from marshmallow import ValidationError

from polyaxon_schemas.experiment import ExperimentConfig
from polyaxon_schemas.project import ProjectConfig, ExperimentGroupConfig
from polyaxon_schemas.utils import local_now
from tests.utils import assert_equal_dict


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
            'num_experiments': 0,
            'num_experiment_groups': 0,
            'created_at': local_now().isoformat(),
            'updated_at': local_now().isoformat()
        }
        config = ProjectConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
        config_dict.pop('description')
        assert config.to_light_dict() == config_dict

        config_to_dict = config.to_dict(humanize_values=True)
        assert config_to_dict.pop('created_at') == 'a few seconds ago'
        assert config_to_dict.pop('updated_at') == 'a few seconds ago'

        config_to_dict = config.to_light_dict(humanize_values=True)
        assert config_to_dict.pop('created_at') == 'a few seconds ago'
        assert config_to_dict.pop('updated_at') == 'a few seconds ago'

    def test_project_experiments_and_groups_config(self):
        uuid_value = uuid.uuid4().hex
        config_dict = {'name': 'test',
                       'description': '',
                       'is_public': True,
                       'experiment_groups': [
                           ExperimentGroupConfig(content='content',
                                                 uuid=uuid_value,
                                                 project=uuid_value).to_dict()],
                       'experiments': [
                           ExperimentConfig(config={},
                                            uuid=uuid_value,
                                            project=uuid_value).to_dict()]}
        config = ProjectConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

        config_dict.pop('description')
        assert_equal_dict(config_dict, config.to_light_dict())

    def test_experiment_group_config(self):
        uuid_value = uuid.uuid4().hex
        config_dict = {'sequence': 1,
                       'content': 'some content',
                       'uuid': uuid_value,
                       'project': uuid_value,
                       'project_name': 'user.name',
                       'num_experiments': 0,
                       'created_at': local_now().isoformat(),
                       'updated_at': local_now().isoformat(),
                       'experiments': [
                           ExperimentConfig(config={},
                                            uuid=uuid_value,
                                            group=uuid_value,
                                            project=uuid_value).to_dict()]}
        config = ExperimentGroupConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict.pop('content')
        assert_equal_dict(config_dict, config.to_light_dict())

        config_to_dict = config.to_dict(humanize_values=True)
        assert config_to_dict.pop('created_at') == 'a few seconds ago'
        assert config_to_dict.pop('updated_at') == 'a few seconds ago'

        config_to_dict = config.to_light_dict(humanize_values=True)
        assert config_to_dict.pop('created_at') == 'a few seconds ago'
        assert config_to_dict.pop('updated_at') == 'a few seconds ago'
