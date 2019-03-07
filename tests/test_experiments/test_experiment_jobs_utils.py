import uuid

import pytest

import conf

from constants.experiment_jobs import get_experiment_job_container_name, get_experiment_job_uuid
from schemas.experiments import ExperimentBackend, ExperimentFramework
from tests.utils import BaseTest


@pytest.mark.experiments_mark
class TestExperimentJobsUtils(BaseTest):
    def test_get_experiment_job_uuid(self):
        uuid1 = uuid.uuid4()
        uuid2 = uuid.uuid4().hex
        uuid3 = str(uuid.uuid4())
        data = {
            uuid1: uuid.uuid5(uuid1, 'worker-0').hex,
            uuid2: uuid.uuid5(uuid.UUID(uuid2), 'worker-1').hex,
            uuid3: uuid.uuid5(uuid.UUID(uuid3), 'worker-2').hex,
        }
        for i, kd in enumerate(data.keys()):
            assert get_experiment_job_uuid(experiment_uuid=kd,
                                           task_type='worker',
                                           task_index=i) == data[kd]

    def test_get_experiment_job_container_name(self):
        assert conf.get('CONTAINER_NAME_EXPERIMENT_JOB') == get_experiment_job_container_name(
            backend=None,
            framework=None,
        )

        assert conf.get('CONTAINER_NAME_EXPERIMENT_JOB') == get_experiment_job_container_name(
            backend=None,
            framework='foo',
        )

        assert conf.get('CONTAINER_NAME_EXPERIMENT_JOB') == get_experiment_job_container_name(
            backend='foo',
            framework='foo',
        )

        assert conf.get('CONTAINER_NAME_EXPERIMENT_JOB') == get_experiment_job_container_name(
            backend='foo',
            framework=None,
        )

        assert conf.get('CONTAINER_NAME_EXPERIMENT_JOB') == get_experiment_job_container_name(
            backend=ExperimentBackend.KUBEFLOW,
            framework='foo',
        )

        assert conf.get('CONTAINER_NAME_TF_JOB') == get_experiment_job_container_name(
            backend=ExperimentBackend.KUBEFLOW,
            framework=ExperimentFramework.TENSORFLOW,
        )

        assert conf.get('CONTAINER_NAME_PYTORCH_JOB') == get_experiment_job_container_name(
            backend=ExperimentBackend.KUBEFLOW,
            framework=ExperimentFramework.PYTORCH,
        )
