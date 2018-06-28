# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid

from unittest import TestCase

from marshmallow import ValidationError
from tests.utils import assert_equal_dict

from polyaxon_schemas.experiment import ExperimentConfig
from polyaxon_schemas.project import ExperimentGroupConfig, GroupStatusConfig, ProjectConfig
from polyaxon_schemas.utils import local_now


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
        config_dict.pop('experiment_groups')
        config_dict.pop('experiments')
        assert_equal_dict(config_dict, config.to_light_dict())

    def test_experiment_group_config(self):
        uuid_value = uuid.uuid4().hex
        config_dict = {'id': 1,
                       'content': 'some content',
                       'uuid': uuid_value,
                       'project': 'user.name',
                       'num_experiments': 0,
                       'created_at': local_now().isoformat(),
                       'updated_at': local_now().isoformat(),
                       'last_status': None,
                       'has_tensorboard': False,
                       'tags': ['tests'],
                       'experiments': [
                           ExperimentConfig(config={},
                                            uuid=uuid_value,
                                            experiment_group=uuid_value,
                                            project=uuid_value).to_dict()]}
        config = ExperimentGroupConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        config_to_dict.pop('concurrency', None)
        config_to_dict.pop('description', None)
        config_to_dict.pop('num_failed_experiments', None)
        config_to_dict.pop('num_pending_experiments', None)
        config_to_dict.pop('num_running_experiments', None)
        config_to_dict.pop('num_scheduled_experiments', None)
        config_to_dict.pop('num_stopped_experiments', None)
        config_to_dict.pop('num_succeeded_experiments', None)
        config_to_dict.pop('unique_name', None)
        config_to_dict.pop('user', None)
        config_to_dict.pop('name', None)
        assert config_to_dict == config_dict

        config_dict.pop('content')
        config_dict.pop('uuid')
        config_dict.pop('project')
        config_dict.pop('updated_at')
        config_dict.pop('id')
        config_dict.pop('experiments')
        config_dict.pop('has_tensorboard')
        config_dict.pop('tags')
        assert_equal_dict(config_dict, config.to_light_dict())

        config_to_dict = config.to_dict(humanize_values=True)
        assert config_to_dict.pop('created_at') == 'a few seconds ago'
        assert config_to_dict.pop('updated_at') == 'a few seconds ago'

        config_to_dict = config.to_light_dict(humanize_values=True)
        assert config_to_dict.pop('created_at') == 'a few seconds ago'

    def test_group_status_config(self):
        config_dict = {'id': 1,
                       'uuid': uuid.uuid4().hex,
                       'experiment_group': 1,
                       'created_at': local_now().isoformat(),
                       'status': 'Running',
                       'message': None,
                       'details': None}
        config = GroupStatusConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert config_to_dict == config_dict

        config_dict.pop('experiment_group', None)
        config_dict.pop('uuid', None)
        config_dict.pop('details', None)
        config_to_dict = config.to_light_dict()
        assert config_to_dict == config_dict

        config_to_dict = config.to_dict(humanize_values=True)
        assert config_to_dict.pop('created_at') == 'a few seconds ago'
