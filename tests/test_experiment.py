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
    ContainerGPUResourcesConfig,
    ContainerResourcesConfig, ExperimentJobConfig, ExperimentStatusConfig,
    ExperimentJobStatusConfig)
from polyaxon_schemas.polyaxonfile.constants import TASK_NAME


class TestExperimentConfigs(TestCase):
    def test_experiment_config(self):
        config_dict = {
            'name': 'test',
            'uuid': uuid.uuid4().hex,
            'project': uuid.uuid4().hex,
            'group': uuid.uuid4().hex,
            'last_status': 'Running',
            'num_jobs': 1,
        }
        config = ExperimentConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_experiment_with_jobs_config(self):
        config_dict = {'name': 'test',
                       'config': {},
                       'content': '',
                       'uuid': uuid.uuid4().hex,
                       'project': uuid.uuid4().hex,
                       'group': uuid.uuid4().hex,
                       'last_status': 'Running',
                       'num_jobs': 1,
                       'jobs': [ExperimentJobConfig(uuid.uuid4().hex,
                                                    uuid.uuid4().hex,
                                                    datetime.now(),
                                                    definition={}).to_dict()]}
        config = ExperimentConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

    def test_experiment_job_config(self):
        config_dict = {'uuid': uuid.uuid4().hex,
                       'experiment': uuid.uuid4().hex,
                       'created_at': datetime.now().isoformat(),
                       'definition': {}}
        config = ExperimentJobConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        config_to_dict.pop('created_at')
        config_dict.pop('created_at')
        assert config_to_dict == config_dict

    def test_experiment_status_config(self):
        config_dict = {'uuid': uuid.uuid4().hex,
                       'experiment': uuid.uuid4().hex,
                       'created_at': datetime.now().isoformat(),
                       'status': 'Running'}
        config = ExperimentStatusConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        config_to_dict.pop('created_at')
        config_dict.pop('created_at')
        assert config_to_dict == config_dict

    def test_experiment_status_config(self):
        config_dict = {'uuid': uuid.uuid4().hex,
                       'job': uuid.uuid4().hex,
                       'created_at': datetime.now().isoformat(),
                       'status': 'Running'}
        config = ExperimentJobStatusConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        config_to_dict.pop('created_at')
        config_dict.pop('created_at')
        assert config_to_dict == config_dict

    @staticmethod
    def create_pod_labels():
        project = 'test-id1'
        experiment = uuid.uuid4().hex
        task_type = 'master'
        return {'project': project,
                'experiment': experiment,
                'task_type': task_type,
                'task_idx': '0',
                'task': TASK_NAME.format(project='test-id1',
                                         experiment=experiment,
                                         task_type=task_type,
                                         task_idx='0'),
                'job_id': uuid.uuid4().hex,
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

    def test_job_state_config(self):
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

    def test_container_gpu_resources(self):
        config_dict = {
            'index': 0,
            'bus_id': '0000:00:1E.1',
            'memory_free': 1000,
            'memory_total': 12883853312,
            'memory_used': 8388608000,
            'memory_utilization': 0,
            'minor': 1,
            'name': 'GeForce GTX TITAN 0',
            'power_draw': 125,
            'power_limit': 250,
            'processes': [{'command': 'python',
                           'gpu_memory_usage': 4000,
                           'pid': 48448,
                           'username': 'user1'},
                          {'command': 'python',
                           'gpu_memory_usage': 4000,
                           'pid': 153223,
                           'username': 'user2'}],
            'serial': '0322917092147',
            'temperature_gpu': 80,
            'utilization_gpu': 76,
            'uuid': 'GPU-10fb0fbd-2696-43f3-467f-d280d906a107'
        }
        config = ContainerGPUResourcesConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert config_to_dict == config_dict

    def test_container_resources(self):
        gpu_resources = {
            'index': 0,
            'bus_id': '0000:00:1E.1',
            'memory_free': 1000,
            'memory_total': 12883853312,
            'memory_used': 8388608000,
            'memory_utilization': 0,
            'minor': 1,
            'name': 'GeForce GTX TITAN 0',
            'power_draw': 125,
            'power_limit': 250,
            'processes': [{'command': 'python',
                           'gpu_memory_usage': 4000,
                           'pid': 48448,
                           'username': 'user1'},
                          {'command': 'python',
                           'gpu_memory_usage': 4000,
                           'pid': 153223,
                           'username': 'user2'}],
            'serial': '0322917092147',
            'temperature_gpu': 80,
            'utilization_gpu': 76,
            'uuid': 'GPU-10fb0fbd-2696-43f3-467f-d280d906a107'
        }

        config_dict = {
            'job_uuid': uuid.uuid4().hex,
            'experiment_uuid': uuid.uuid4().hex,
            'container_id': '3175e88873af9077688cee20eaadc0c07746efb84d01ae696d6d17ed9bcdfbc4',
            'cpu_percentage': 0.6947691836734693,
            'percpu_percentage': [0.4564075715616173, 0.23836161211185192],
            'memory_used': 84467712,
            'memory_limit': 2096160768,
            'gpu_resources': gpu_resources
        }
        config = ContainerResourcesConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert config_to_dict == config_dict
