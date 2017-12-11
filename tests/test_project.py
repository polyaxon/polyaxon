# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid
from unittest import TestCase

from marshmallow import ValidationError

from polyaxon_schemas.experiment import ExperimentConfig
from polyaxon_schemas.project import ProjectConfig, ExperimentGroupConfig
from tests.utils import assert_equal_dict


class TestProjectConfigs(TestCase):
    def test_validate_project_name_config(self):
        config_dict = {'name': 'test sdf', 'description': '', 'is_public': True}
        with self.assertRaises(ValidationError):
            ProjectConfig.from_dict(config_dict)

    def test_project_config(self):
        config_dict = {'name': 'test', 'description': '', 'is_public': True}
        config = ProjectConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_project_experiments_and_groups_config(self):
        uuid_value = uuid.uuid4().hex
        config_dict = {'name': 'test',
                       'description': '',
                       'is_public': True,
                       'experiment_groups': [
                           ExperimentGroupConfig(content='name',
                                                 uuid=uuid_value,
                                                 project=uuid_value).to_dict()],
                       'experiments': [
                           ExperimentConfig(name='name',
                                            config={},
                                            uuid=uuid_value,
                                            project=uuid_value).to_dict()]}
        config = ProjectConfig.from_dict(config_dict)
        assert_equal_dict(config_dict, config.to_dict())

    def test_experiment_group_config(self):
        uuid_value = uuid.uuid4().hex
        config_dict = {'content': 'some content',
                       'uuid': uuid_value,
                       'project': uuid_value,
                       'experiments': [
                           ExperimentConfig(name='name',
                                            config={},
                                            uuid=uuid_value,
                                            group=uuid_value,
                                            project=uuid_value).to_dict()]}
        config = ExperimentGroupConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
