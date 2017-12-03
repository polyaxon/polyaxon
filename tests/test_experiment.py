# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid
from unittest import TestCase

from datetime import datetime

from polyaxon_schemas.experiment import (
    ExperimentConfig,
    JobLabelConfig,
    PodStateConfig,
    JobStateConfig,
)
from polyaxon_schemas.polyaxonfile.constants import TASK_NAME


class TestExperimentConfigs(TestCase):
    def test_experiment_config(self):
        config_dict = {'name': 'test', 'uuid': str(uuid.uuid4()), 'project': str(uuid.uuid4())}
        config = ExperimentConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    @staticmethod
    def create_pod_labels():
        project = 'test-id1'
        experiment = str(uuid.uuid4())
        task_type = 'master'
        return {'project': project,
                'experiment': experiment,
                'task_type': task_type,
                'task_idx': '0',
                'task': TASK_NAME.format(project='test-id1',
                                         experiment=experiment,
                                         task_type=task_type,
                                         task_idx='0'),
                'job_id': str(uuid.uuid4()),
                'role': 'polyaxon-worker',
                'type': 'polyaxon-experiment'
                }

    @classmethod
    def create_pod_state(cls):
        event_type = 'ADDED'
        phase = 'Running'
        labels = cls.create_pod_labels()
        deletion_timestamp = datetime.now().isoformat()
        pod_conditions = {}
        container_statuses = {}
        return {
            'event_type': event_type,
            'phase': phase,
            'labels': labels,
            'deletion_timestamp': deletion_timestamp,
            'pod_conditions': pod_conditions,
            'container_statuses': container_statuses,
        }

    def test_pod_label_config(self):
        config_dict = self.create_pod_labels()
        config = JobLabelConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_pod_state_config(self):
        config_dict = self.create_pod_state()
        config = PodStateConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        config_to_dict.pop('deletion_timestamp')
        config_dict.pop('deletion_timestamp')
        assert config_to_dict == config_dict

    def test_jpn_state_config(self):
        config_dict = {
            'status': 'Running',
            'message': 'something',
            'details': self.create_pod_state()
        }
        config = JobStateConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        config_to_dict['details'].pop('deletion_timestamp')
        config_dict['details'].pop('deletion_timestamp')
        assert config_to_dict == config_dict
