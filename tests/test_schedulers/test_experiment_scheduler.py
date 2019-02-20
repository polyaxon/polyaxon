import uuid

import pytest

from db.models.experiment_jobs import ExperimentJob
from factories.factory_experiments import ExperimentFactory
from scheduler.experiment_scheduler import create_job, get_spawner_class, set_job_definition
from scheduler.spawners.experiment_spawner import ExperimentSpawner
from scheduler.spawners.horovod_spawner import HorovodSpawner
from scheduler.spawners.mxnet_spawner import MXNetSpawner
from scheduler.spawners.pytorch_spawner import PytorchSpawner
from scheduler.spawners.tensorflow_spawner import TensorflowSpawner
from schemas.frameworks import Frameworks
from schemas.tasks import TaskType
from tests.utils import BaseTest


@pytest.mark.scheduler_mark
class TestExperimentScheduler(BaseTest):

    def test_create_job(self):
        experiment = ExperimentFactory()
        assert ExperimentJob.objects.count() == 0

        node_selector = {'polyaxon': 'selector'}
        affinity = {
            'podAffinity': {
                'preferredDuringSchedulingIgnoredDuringExecution': [
                    {
                        'podAffinityTerm': {
                            'topologyKey': 'kubernetes.io/hostname', 'labelSelector': {
                                'matchExpressions': [
                                    {'operator': 'In',
                                     'key': 'polyaxon',
                                     'values': ['high-cpu']
                                     }]}},
                        'weight': 100
                    }
                ]
            }
        }
        tolerations = [
            {'operator': 'Equal', 'effect': 'NoSchedule', 'key': 'polyaxon', 'value': 'somevalue'}
        ]

        create_job(job_uuid=uuid.uuid4().hex,
                   experiment=experiment,
                   node_selector=node_selector,
                   affinity=affinity,
                   tolerations=tolerations)
        assert ExperimentJob.objects.count() == 1
        job = ExperimentJob.objects.last()
        assert job.role == TaskType.MASTER
        assert job.resources is None
        assert job.node_selector == node_selector
        assert job.affinity == affinity
        assert job.tolerations == tolerations

    def test_set_job_definition(self):
        experiment = ExperimentFactory()
        job_uuid = uuid.uuid4().hex
        create_job(job_uuid=job_uuid,
                   experiment=experiment)
        job = ExperimentJob.objects.last()
        assert job.role == TaskType.MASTER
        assert job.resources is None
        assert job.node_selector is None
        assert job.affinity is None
        assert job.tolerations is None
        assert job.definition == {}
        definition = {'spec': {}}
        set_job_definition(job_uuid=job_uuid, definition=definition)
        job = ExperimentJob.objects.last()
        assert job.definition == definition

    def test_get_spawner_class(self):
        assert get_spawner_class(Frameworks.TENSORFLOW) == TensorflowSpawner
        assert get_spawner_class(Frameworks.HOROVOD) == HorovodSpawner
        assert get_spawner_class(Frameworks.MXNET) == MXNetSpawner
        assert get_spawner_class(Frameworks.PYTORCH) == PytorchSpawner
        assert get_spawner_class(None) == ExperimentSpawner
