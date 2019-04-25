# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid

from unittest import TestCase

from hestia.tz_utils import local_now

from polyaxon_schemas.api.job import (
    BuildJobConfig,
    JobConfig,
    JobStatusConfig,
    TensorboardJobConfig
)


class TestJobConfigs(TestCase):
    def test_job_config(self):
        config_dict = {
            'uuid': uuid.uuid4().hex,
            'project': 'name.name',
            'build_job': 'name.name',
            'unique_name': 'user.proj.1',
            'pod_id': 'job_1',
            'last_status': 'Running',
            'description': 'description',
            'content': "{'k': 'v'}",
            'is_managed': False,
            'backend': 'other',
            'tags': ['test'],
            'definition': None,
            'created_at': local_now().isoformat(),
            'updated_at': local_now().isoformat(),
            'started_at': local_now().isoformat(),
            'finished_at': local_now().isoformat(),
        }
        config = JobConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        config_to_dict.pop('is_clone')
        config_to_dict.pop('resources')
        config_to_dict.pop('id')
        config_to_dict.pop('total_run')
        config_to_dict.pop('user')
        config_to_dict.pop('name')
        config_to_dict.pop('ttl')
        assert config_to_dict == config_dict

        config_to_dict = config.to_light_dict()
        config_dict.pop('uuid')
        config_dict.pop('description')
        config_dict.pop('content')
        config_dict.pop('project')
        config_dict.pop('build_job')
        config_dict.pop('updated_at')
        config_dict.pop('definition')
        config_dict.pop('tags')
        config_dict.pop('pod_id')
        config_dict.pop('is_managed')
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
        config_dict = {'id': 1,
                       'uuid': uuid.uuid4().hex,
                       'job': 1,
                       'created_at': local_now().isoformat(),
                       'status': 'Running',
                       'message': None,
                       'traceback': None,
                       'details': None}
        config = JobStatusConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert config_to_dict == config_dict

        config_dict.pop('job', None)
        config_dict.pop('uuid', None)
        config_dict.pop('details', None)
        config_dict.pop('traceback', None)
        config_to_dict = config.to_light_dict()
        assert config_to_dict == config_dict

        config_to_dict = config.to_dict(humanize_values=True)
        assert config_to_dict.pop('created_at') == 'a few seconds ago'


class TestBuildJobConfigs(TestCase):
    def test_build_job_config(self):
        config_dict = {
            'uuid': uuid.uuid4().hex,
            'project': 'name.name',
            'build_job': 'name.name',
            'unique_name': 'user.proj.1',
            'pod_id': 'job_1',
            'last_status': 'Running',
            'description': 'description',
            'content': "{'k': 'v'}",
            'is_managed': False,
            'tags': ['test'],
            'definition': None,
            'dockerfile': 'some container',
            'backend': 'kaniko',
            'created_at': local_now().isoformat(),
            'updated_at': local_now().isoformat(),
            'started_at': local_now().isoformat(),
            'finished_at': local_now().isoformat(),
        }
        config = BuildJobConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        config_to_dict.pop('is_clone')
        config_to_dict.pop('resources')
        config_to_dict.pop('id')
        config_to_dict.pop('total_run')
        config_to_dict.pop('user')
        config_to_dict.pop('name')
        config_to_dict.pop('ttl')
        assert config_to_dict == config_dict

        config_to_dict = config.to_light_dict()
        config_dict.pop('uuid')
        config_dict.pop('description')
        config_dict.pop('content')
        config_dict.pop('project')
        config_dict.pop('build_job')
        config_dict.pop('updated_at')
        config_dict.pop('definition')
        config_dict.pop('tags')
        config_dict.pop('pod_id')
        config_dict.pop('is_managed')
        config_dict.pop('dockerfile')
        config_to_dict.pop('id')
        config_to_dict.pop('total_run')
        config_to_dict.pop('user')
        assert config_to_dict == config_dict

        config_to_dict = config.to_light_dict(humanize_values=True)
        assert config_to_dict.pop('total_run') == '0s'
        assert config_to_dict.pop('created_at') == 'a few seconds ago'
        assert config_to_dict.pop('started_at') == 'a few seconds ago'
        assert config_to_dict.pop('finished_at') == 'a few seconds ago'


class TestTensorboardJobConfigs(TestCase):
    def test_tensorboard_job_config(self):
        config_dict = {
            'uuid': uuid.uuid4().hex,
            'project': 'name.name',
            'experiment': 1,
            'experiment_group': 1,
            'unique_name': 'user.proj.1',
            'pod_id': 'job_1',
            'last_status': 'Running',
            'tags': ['test'],
            'is_managed': False,
            'created_at': local_now().isoformat(),
            'updated_at': local_now().isoformat(),
            'started_at': local_now().isoformat(),
            'finished_at': local_now().isoformat(),
        }
        config = TensorboardJobConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        config_to_dict.pop('is_clone')
        config_to_dict.pop('resources')
        config_to_dict.pop('id')
        config_to_dict.pop('total_run')
        config_to_dict.pop('user')
        config_to_dict.pop('name')
        config_to_dict.pop('build_job')
        config_to_dict.pop('content')
        config_to_dict.pop('definition')
        config_to_dict.pop('description')
        config_to_dict.pop('ttl')
        assert config_to_dict == config_dict

        config_to_dict = config.to_light_dict()
        config_dict.pop('uuid')
        config_dict.pop('project')
        config_dict.pop('updated_at')
        config_dict.pop('tags')
        config_dict.pop('is_managed')
        config_to_dict.pop('id')
        config_to_dict.pop('total_run')
        config_to_dict.pop('user')
        assert config_to_dict == config_dict

        config_to_dict = config.to_light_dict(humanize_values=True)
        assert config_to_dict.pop('total_run') == '0s'
        assert config_to_dict.pop('created_at') == 'a few seconds ago'
        assert config_to_dict.pop('started_at') == 'a few seconds ago'
        assert config_to_dict.pop('finished_at') == 'a few seconds ago'

    def test_tensorboard_status_config(self):
        config_dict = {'id': 1,
                       'uuid': uuid.uuid4().hex,
                       'job': 1,
                       'created_at': local_now().isoformat(),
                       'status': 'Running',
                       'message': None,
                       'traceback': None,
                       'details': None}
        config = JobStatusConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert config_to_dict == config_dict

        config_dict.pop('job', None)
        config_dict.pop('uuid', None)
        config_dict.pop('details', None)
        config_dict.pop('traceback', None)
        config_to_dict = config.to_light_dict()
        assert config_to_dict == config_dict

        config_to_dict = config.to_dict(humanize_values=True)
        assert config_to_dict.pop('created_at') == 'a few seconds ago'
