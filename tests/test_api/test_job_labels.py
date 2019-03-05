# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid

from unittest import TestCase

from polyaxon_schemas.api.job import JobLabelConfig


class TestSettingConfigs(TestCase):
    @staticmethod
    def create_pod_labels():
        project_name = 'user/test-id1'
        experiment_group_name = 'user/test-id1/1'
        experiment_name = 'user/test-id1/1/2'
        project_uuid = uuid.uuid4().hex
        experiment_group_uuid = uuid.uuid4().hex
        experiment_uuid = uuid.uuid4().hex
        job_uuid = uuid.uuid4().hex
        task_type = 'master'
        return {'project_name': project_name,
                'experiment_group_name': experiment_group_name,
                'experiment_name': experiment_name,
                'project_uuid': project_uuid,
                'experiment_group_uuid': experiment_group_uuid,
                'experiment_uuid': experiment_uuid,
                'task_type': task_type,
                'task_idx': '0',
                'job_uuid': job_uuid,
                'role': 'polyaxon-worker',
                'type': 'polyaxon-experiment'
                }

    def test_pod_label_config(self):
        config_dict = self.create_pod_labels()
        config = JobLabelConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict
