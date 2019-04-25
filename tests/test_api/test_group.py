# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid

from unittest import TestCase

from hestia.tz_utils import local_now
from tests.utils import assert_equal_dict

from polyaxon_schemas.api.experiment import ExperimentConfig
from polyaxon_schemas.api.group import GroupConfig, GroupStatusConfig


class TestGroupConfigs(TestCase):

    def test_experiment_group_config(self):
        uuid_value = uuid.uuid4().hex
        config_dict = {'id': 1,
                       'content': 'some content',
                       'uuid': uuid_value,
                       'project': 'user.name',
                       'num_experiments': 0,
                       'created_at': local_now().isoformat(),
                       'updated_at': local_now().isoformat(),
                       'started_at': local_now().isoformat(),
                       'finished_at': local_now().isoformat(),
                       'group_type': 'study',
                       'backend': 'native',
                       'is_managed': True,
                       'search_algorithm': None,
                       'last_status': None,
                       'has_tensorboard': False,
                       'tags': ['tests'],
                       'experiments': [
                           ExperimentConfig(uuid=uuid_value,
                                            experiment_group=uuid_value,
                                            project=uuid_value).to_dict()]}
        config = GroupConfig.from_dict(config_dict)
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
        config_to_dict.pop('total_run', None)
        assert config_to_dict == config_dict

        config_dict.pop('content')
        config_dict.pop('uuid')
        config_dict.pop('project')
        config_dict.pop('updated_at')
        config_dict.pop('id')
        config_dict.pop('experiments')
        config_dict.pop('has_tensorboard')
        config_dict.pop('tags')
        config_dict.pop('backend')
        config_dict.pop('is_managed')
        config_dict.pop('num_experiments', None)
        config_dict.pop('num_failed_experiments', None)
        config_dict.pop('num_pending_experiments', None)
        config_dict.pop('num_running_experiments', None)
        config_dict.pop('num_scheduled_experiments', None)
        config_dict.pop('num_stopped_experiments', None)
        config_dict.pop('num_succeeded_experiments', None)
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
