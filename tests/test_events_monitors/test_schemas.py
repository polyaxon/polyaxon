import uuid

import pytest

from monitor_statuses.schemas import JobStateConfig, PodStateConfig
from polyaxon_schemas.utils import local_now
from schemas.job_labels import JobLabelConfig
from tests.utils import BaseTest


@pytest.mark.monitors_mark
class Test(BaseTest):
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

    @classmethod
    def create_pod_state(cls):
        event_type = 'ADDED'
        phase = 'Running'
        labels = cls.create_pod_labels()
        deletion_timestamp = local_now().isoformat()
        pod_conditions = {}
        container_statuses = {}
        return {
            'event_type': event_type,
            'phase': phase,
            'labels': labels,
            'node_name': 'node1',
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
        assert config_to_dict == config_dict

        config_to_dict = config.to_dict(humanize_values=True)
        assert config_to_dict.pop('deletion_timestamp') == 'a few seconds ago'

    def test_job_state_config(self):
        config_dict = {
            'status': 'Running',
            'message': 'something',
            'details': self.create_pod_state()
        }
        config = JobStateConfig.from_dict(config_dict)
        config_to_dict = config.to_dict()
        assert config_to_dict == config_dict
