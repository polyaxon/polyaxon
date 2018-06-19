# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid

from unittest import TestCase

from polyaxon_schemas.job import JobConfig, JobStatusConfig
from polyaxon_schemas.utils import local_now


class TestJobConfigs(TestCase):
    def test_job_config(self):
        config_dict = {
            'uuid': uuid.uuid4().hex,
            'project': uuid.uuid4().hex,
            'project_name': 'name.name',
            'unique_name': 'user.proj.1',
            'last_status': 'Running',
            'description': 'description',
            'config': {'k': 'v'},
            'definition': None,
            'created_at': local_now().isoformat(),
            'updated_at': local_now().isoformat(),
            'started_at': local_now().isoformat(),
            'finished_at': local_now().isoformat(),
        }
        config = JobConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        config_to_dict.pop('is_clone')
        config_to_dict.pop('is_done')
        config_to_dict.pop('is_running')
        config_to_dict.pop('resources')
        config_to_dict.pop('id')
        config_to_dict.pop('total_run')
        config_to_dict.pop('user')
        assert config_to_dict == config_dict

        config_to_dict = config.to_light_dict()
        config_dict.pop('uuid')
        config_dict.pop('description')
        config_dict.pop('config')
        config_dict.pop('project')
        config_dict.pop('updated_at')
        config_dict.pop('project_name')
        config_dict.pop('definition')
        config_to_dict.pop('is_done')
        config_to_dict.pop('is_running')
        config_to_dict.pop('id')
        config_to_dict.pop('total_run')
        config_to_dict.pop('user')
        assert config_to_dict == config_dict

        config_to_dict = config.to_light_dict(humanize_values=True)
        assert config_to_dict.pop('total_run') == '0s'
        assert config_to_dict.pop('created_at') == 'a few seconds ago'
        assert config_to_dict.pop('started_at') == 'a few seconds ago'
        assert config_to_dict.pop('finished_at') == 'a few seconds ago'

    def test_job_status_config(self):
        config_dict = {'uuid': uuid.uuid4().hex,
                       'job': uuid.uuid4().hex,
                       'created_at': local_now().isoformat(),
                       'status': 'Running',
                       'message': None,
                       'details': None}
        config = JobStatusConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert config_to_dict == config_dict

        config_dict.pop('job', None)
        config_dict.pop('uuid', None)
        config_to_dict = config.to_light_dict()
        assert config_to_dict == config_dict

        config_to_dict = config.to_dict(humanize_values=True)
        assert config_to_dict.pop('created_at') == 'a few seconds ago'
